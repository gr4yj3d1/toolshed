import {createStore} from 'vuex';
import router from '@/router';
import FallBackResolver from "@/dns";
import NeighborsCache from "@/neigbors";


export default createStore({
    state: {
        user: null,
        token: null,
        keypair: null,
        remember: false,
        friends: [],
        item_map: {},
        resolver: new FallBackResolver(),
        unreachable_neighbors: new NeighborsCache(),
        /*wk: new Wellknown({
            update: true, // Will load latest definitions from updateURL.
            updateURL: new URL(), // URL to load the latest definitions. (default: project URL)
            persist: false, // True to persist the loaded definitions (nodejs: in filesystem, browser: localStorage)
            localStoragePrefix: 'dnsquery_', // Prefix for files persisted.
            maxAge: 300000, // Max age of persisted data to be used in ms.
            timeout: 5000 // Timeout when loading updates.
        })*/
    },
    mutations: {
        setUser(state, user) {
            state.user = user;
            if (state.remember)
                localStorage.setItem('user', user);
        },
        setToken(state, token) {
            state.token = token;
            if (state.remember)
                localStorage.setItem('token', token);
        },
        setKey(state, keypair) {
            state.keypair = nacl.crypto_sign_keypair_from_seed(nacl.from_hex(keypair))
            if (state.remember)
                localStorage.setItem('keypair', nacl.to_hex(state.keypair.signSk).slice(0, 64))
        },
        setRemember(state, remember) {
            state.remember = remember;
            if (!remember) {
                localStorage.removeItem('user');
                localStorage.removeItem('token');
                localStorage.removeItem('keypair');
            }
            localStorage.setItem('remember', remember);
        },
        setInventoryItems(state, {url, items}) {
            state.item_map[url] = items;
        },
        logout(state) {
            state.user = null;
            state.token = null;
            state.keypair = null;
            localStorage.removeItem('user');
            localStorage.removeItem('token');
            localStorage.removeItem('keypair');
            router.push('/login');
        },
        init(state) {
            const remember = localStorage.getItem('remember');
            const user = localStorage.getItem('user');
            const token = localStorage.getItem('token');
            const keypair = localStorage.getItem('keypair');
            if (user && token) {
                this.commit('setUser', user);
                this.commit('setToken', token);
                if (keypair) {
                    this.commit('setKey', keypair)
                } else {
                }
                router.push('/');
            }
        }
    },
    actions: {
        async login({commit, dispatch, state}, {username, password, remember}) {
            //this.setRemember(remember)
            this.commit('setRemember', remember);
            /*const response = await fetch('http://10.23.42.128:8000/auth/token/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: username, password: password
                })
            })*/
            const data = await dispatch('apiLocalPost', {
                target: '/token/', data: {
                    username: username, password: password
                }
            })
            if (data.token) {
                commit('setToken', data.token);
                commit('setUser', username + '@example.com');
                const j = await dispatch('apiLocalGet', {target: '/keys/'})
                const k = j.key
                this.commit('setKey', k)
                await router.push({path: '/'});
                return true;
            } else {
                return false;
            }

        },
        async getFriends(state) {
            return ['jedi@j3d1.de', 'foobar@example.com', 'foobaz@example.eleon'];
        },
        async getFriendServer({state}, {username}) {
            const domain = username.split('@')[1]
            if (domain === 'example.eleon')
                return ['10.23.42.186:8000'];
            if (domain === 'localhost')
                return ['127.0.0.1:8000'];
            if (domain === 'example.com')
                return ['10.23.42.128:8000'];
            const request = '_toolshed-server._tcp.' + domain + '.'
            return await state.resolver.query(request, 'SRV').then(
                (result) => result.map(
                    (answer) => answer.target + ':' + answer.port))
        },
        async apiFederatedGet({state}, url) {
            if (state.unreachable_neighbors.queryUnreachable(url)) {
                throw new Error('unreachable neighbor')
            }
            const signature = nacl.crypto_sign_detached(nacl.encode_utf8(url), state.keypair.signSk)
            const auth = 'Signature ' + state.user + ':' + nacl.to_hex(signature)
            return await fetch(url, {
                method: 'GET',
                headers: {
                    'Authorization': auth
                }
            }).catch( err => state.unreachable_neighbors.unreachable(url)
            ).then(response => response.json())
        },
        async apiFederatedPost({state}, {url, data}) {
            if (state.unreachable_neighbors.queryUnreachable(url)) {
                throw new Error('unreachable neighbor')
            }
            const json = JSON.stringify(data)
            const signature = nacl.crypto_sign_detached(nacl.encode_utf8(url + json), state.keypair.signSk)
            const auth = 'Signature ' + state.user + ':' + nacl.to_hex(signature)
            return await fetch(url, {
                method: 'POST',
                headers: {
                    'Authorization': auth,
                    'Content-Type': 'application/json'
                },
                body: json
            }).catch( err => state.unreachable_neighbors.unreachable(url)
            ).then(response => response.json())
        },
        async apiLocalGet({state}, {target}) {
            const auth = state.token ? {'Authorization': 'Token ' + state.token} : {}
            return await fetch('http://10.23.42.128:8000/auth' + target, {
                method: 'GET',
                headers: auth
            }).then(response => response.json())
        },
        async apiLocalPost({state}, {target, data}) {
            const auth = state.token ? {'Authorization': 'Token ' + state.token} : {}
            return await fetch('http://10.23.42.128:8000/auth' + target, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    ...auth
                },
                body: JSON.stringify(data)
            }).then(response => response.json())
        }
    },
    getters: {
        isLoggedIn(state) {
            return state.user !== null && state.token !== null;
        },
        inventory_items(state) {
            return Object.entries(state.item_map).reduce((acc, [url, items]) => {
                return acc.concat(items)
            }, [])
        }
    }
})