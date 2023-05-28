import {createStore} from 'vuex';
import router from '@/router';
import FallBackResolver from "@/dns";
import NeighborsCache from "@/neigbors";
import {createSignAuth, createTokenAuth, createNullAuth, ServerSet} from "@/federation";


export default createStore({
    state: {
        local_loaded: false,
        last_load: {},
        user: null,
        token: null,
        keypair: null,
        remember: false,
        friends: [],
        item_map: {},
        //notifications: [],
        messages: [],
        home_servers: null,
        all_friends_servers: null,
        resolver: new FallBackResolver(),
        unreachable_neighbors: new NeighborsCache(),
        tags: [],
        properties: [],
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
            console.log('setInventoryItems', url, items)
            state.item_map[url] = items;
        },
        setFriends(state, friends) {
            state.friends = friends;
        },
        setHomeServers(state, home_servers) {
            console.log('setHomeServer', home_servers)
            state.home_servers = home_servers;
        },
        setAllFriendsServers(state, servers) {
            console.log('setAllFriendsServers', servers)
            state.all_friends_servers = servers;
        },
        setTags(state, tags) {
            console.log('setTags', tags)
            state.tags = tags;
        },
        setProperties(state, properties) {
            console.log('setProperties', properties)
            state.properties = properties;
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
        load_local(state) {
            if (state.local_loaded)
                return;
            const remember = localStorage.getItem('remember');
            const user = localStorage.getItem('user');
            const token = localStorage.getItem('token');
            const keypair = localStorage.getItem('keypair');
            if (user && token) {
                this.commit('setUser', user);
                this.commit('setToken', token);
                if (keypair) {
                    this.commit('setKey', keypair)
                }
            }
            state.cache_loaded = true;
        }
    },
    actions: {
        async login({commit, dispatch, state}, {username, password, remember}) {
            commit('setRemember', remember);
            const data = await fetch('/auth/token/', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({username: username, password: password}),
                credentials: 'omit'
            }).then(r => r.json())
            if (data.token) {
                commit('setToken', data.token);
                commit('setUser', username);
                const j = await fetch('/auth/keys/', {
                    method: 'GET',
                    headers: {'Authorization': 'Token ' + data.token},
                    credentials: 'omit'
                }).then(r => r.json())
                const k = j.key
                commit('setKey', k)
                const s = await dispatch('lookupServer', {username}).then(servers => new ServerSet(servers, state.unreachable_neighbors))
                commit('setHomeServers', s)
                return true;
            } else {
                return false;
            }
        },
        async lookupServer({state}, {username}) {
            const domain = username.split('@')[1]
            if (domain === 'example.eleon')
                return ['10.23.42.186:8000'];
            if (domain === 'localhost')
                return ['127.0.0.1:8000'];
            if (domain === 'example.com')
                return ['10.23.42.128:8000'];
            if (domain === 'example.jedi')
                return ['10.23.42.128:8000'];
            if (domain === 'example2.com')
                return ['10.23.42.128:9000'];
            const request = '_toolshed-server._tcp.' + domain + '.'
            return await state.resolver.query(request, 'SRV').then(
                (result) => result.map(
                    (answer) => answer.target + ':' + answer.port))
        },
        async getHomeServers({state, dispatch, commit}) {
            if (state.home_servers)
                return state.home_servers
            const promise = dispatch('lookupServer', {username: state.user}).then(servers => new ServerSet(servers, state.unreachable_neighbors))
            commit('setHomeServers', promise)
            return promise
        },
        async getAllFriendsServers({state, dispatch, commit}) {
            if (state.all_friends_servers)
                return state.all_friends_servers
            const promise = (async () => {
                const servers = new ServerSet([], state.unreachable_neighbors)
                for (const friend of state.friends) {
                    const s = await dispatch('lookupServer', {username: friend})
                    servers.add(s)
                }
                return servers
            })()
            commit('setAllFriendsServers', promise)
            return promise
        },
        async getFriendServers({state, dispatch, commit}, {username}) {
            return dispatch('lookupServer', {username}).then(servers => new ServerSet(servers, state.unreachable_neighbors))
        },
        async fetchInventoryItems({commit, dispatch, getters}) {
            const servers = await dispatch('getHomeServers')
            const items = await servers.get(getters.signAuth, '/api/inventory_items/')
            commit('setInventoryItems', {url: '/', items})
            return items
        },
        async searchInventories({state, dispatch, getters}, {query}) {
            const servers = await dispatch('getAllFriendsServers')
            return await servers.get(getters.signAuth, '/api/inventory/search/?q=' + query)
        },
        async createInventoryItem({state, dispatch, getters}, {item}) {
            const servers = await dispatch('getHomeServers')
            return await servers.post(getters.signAuth, '/api/inventory_items/', item)
        },
        async updateInventoryItem({state, dispatch, getters}, {item}) {
            const servers = await dispatch('getHomeServers')
            return await servers.patch(getters.signAuth, '/api/inventory_items/' + item.id + '/', item)
        },
        async deleteInventoryItem({state, dispatch, getters}, {item}) {
            const servers = await dispatch('getHomeServers')
            return await servers.delete(getters.signAuth, '/api/inventory_items/' + item.id + '/')
        },
        /*async searchInventoryItems() {
            try {
                const servers = await this.fetchFriends().then(friends => friends.map(friend => this.lookupServer({username: friend.name})))
                const urls = servers.map(server => server.then(s => {
                    return {host: s, target: "/api/inventory_items/"}
                }))
                urls.map(url => url.then(u => this.apiFederatedGet(u).then(items => {
                    this.setInventoryItems({url: u.domain, items})
                }).catch(e => {
                }))) // TODO: handle error
            } catch (e) {
                console.error(e)
            }
        },*/
        async fetchFriends({commit, dispatch, getters, state}) {
            const servers = await dispatch('getHomeServers')
            const data = await servers.get(getters.signAuth, '/api/friends/')
            commit('setFriends', data)
            return data
        },
        async fetchFriendRequests({state, dispatch, getters}) {
            const servers = await dispatch('getHomeServers')
            return await servers.get(getters.signAuth, '/api/friendrequests/')
        },
        async requestFriend({state, dispatch, getters}, {username}) {
            if (username in state.friends) {
                return true;
            }
            const home_servers = await dispatch('getHomeServers')
            const home_reply = home_servers.post(getters.signAuth, '/api/friendrequests/', {
                befriender: state.user,
                befriendee: username
            })
            if (home_reply.status !== 'pending' || !home_reply.secret)
                return false;

            const befriendee_servers = await dispatch('getFriendServers', {username})
            const ext_reply = befriendee_servers.post(getters.signAuth, '/api/friendrequests/', {
                befriender: state.user,
                befriendee: username,
                befriender_key: nacl.to_hex(state.keypair.signPk),
                secret: home_reply.secret
            })
            return true;
        },
        async acceptFriend({state, dispatch, getters}, {id, secret, befriender}) {
            const home_servers = await dispatch('getHomeServers')
            const home_reply = await home_servers.post(getters.signAuth, '/api/friends/', {
                friend_request_id: id, secret: secret
            })
            const ext_servers = await dispatch('getFriendServers', {username: befriender})
            const ext_reply = await ext_servers.post(getters.signAuth, '/api/friendrequests/', {
                befriender: state.user,
                befriendee: befriender,
                befriender_key: nacl.to_hex(state.keypair.signPk),
                secret: secret
            })
            return true
        },
        async declineFriend({state, dispatch}, args) {
            // TODO implement
            console.log('declining friend ' + args)
        },
        async fetchTags({state, commit, dispatch, getters}) {
            if(state.last_load.tags > Date.now() - 1000 * 60 * 60 * 24) {
                return state.tags
            }
            const servers = await dispatch('getHomeServers')
            const data = await servers.get(getters.signAuth, '/api/tags/')
            commit('setTags', data)
            state.last_load.tags = Date.now()
            return data
        },
        async fetchProperties({state, commit, dispatch, getters}) {
            if(state.last_load.properties > Date.now() - 1000 * 60 * 60 * 24) {
                return state.properties
            }
            const servers = await dispatch('getHomeServers')
            const data = await servers.get(getters.signAuth, '/api/properties/')
            commit('setProperties', data)
            state.last_load.properties = Date.now()
            return data
        }
    },
    getters: {
        isLoggedIn(state) {
            if (!state.local_loaded) {
                state.remember = localStorage.getItem('remember') === 'true'
                state.user = localStorage.getItem('user')
                state.token = localStorage.getItem('token')
                const keypair = localStorage.getItem('keypair')
                if (keypair)
                    state.keypair = nacl.crypto_sign_keypair_from_seed(nacl.from_hex(keypair))
                state.local_loaded = true
            }

            return state.user !== null && state.token !== null;
        },
        signAuth(state) {
            console.log('signAuth', state.user, state.keypair.signSk)
            return createSignAuth(state.user, state.keypair.signSk)
        },
        tokenAuth(state) {
            console.log('tokenAuth', state.token)
            return createTokenAuth(state.token)
        },
        nullAuth(state) {
            return createNullAuth({})
        },
        inventory_items(state) {
            return Object.entries(state.item_map).reduce((acc, [url, items]) => {
                return acc.concat(items)
            }, [])
        },
        notifications(state) {
            // supported types: error, warning, info, login, success, friend
            const u = state.unreachable_neighbors.list().map(elem => {
                return {
                    type: 'error',
                    title: elem.domain + ' unreachable',
                    msg: 'The neighbor ' + elem.domain + ' is currently unreachable. Please try again later.',
                    time: elem.time
                }
            })
            return [...u, {
                type: 'info',
                title: 'Welcome to the Toolshed',
                msg: 'This is a federated social network. You can add friends from other servers and share items with them.',
                time: Date.now()
            }, {
                type: 'warning',
                title: 'Lorem ipsum',
                msg: 'Aliquam ex eros, imperdiet vulputate hendrerit et.',
                time: Date.now() - 1000 * 60 * 60 * 2
            }, {
                type: 'login',
                title: 'Login from 192.186.1.8',
                time: Date.now() - 1000 * 60 * 60 * 5
            }, {
                type: 'friend',
                title: 'New connection',
                msg: 'Christina accepted your request.',
                time: Date.now() - 1000 * 60 * 60 * 14
            }, {
                type: 'success',
                title: 'Lorem ipsum',
                msg: 'Aliquam ex eros, imperdiet vulputate hendrerit et.',
                time: Date.now() - 1000 * 60 * 60 * 24
            }]
        },
    }
})