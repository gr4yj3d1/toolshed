class ServerSet {
    constructor(servers, unreachable_neighbors) {
        if (!servers || !Array.isArray(servers)) {
            throw new Error('no servers')
        }
        if (!unreachable_neighbors || typeof unreachable_neighbors.queryUnreachable !== 'function' || typeof unreachable_neighbors.unreachable !== 'function') {
            throw new Error('no unreachable_neighbors')
        }
        this.servers = servers;
        this.unreachable_neighbors = unreachable_neighbors;
    }

    add(server) {
        this.servers.push(server);
    }

    async post(auth, target, data) {
        if (!auth || typeof auth.buildAuthHeader !== 'function') {
            throw new Error('no auth')
        }
        for (const server of this.servers) {
            try {
                if (this.unreachable_neighbors.queryUnreachable(server)) {
                    continue
                }
                const url = "http://" + server + target // TODO https
                return await fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        ...auth.buildAuthHeader(url)
                    },
                    credentials: 'omit',
                    body: JSON.stringify(data)
                }).catch(err => this.unreachable_neighbors.unreachable(server)
                ).then(response => response.json())
            } catch (e) {
                console.error('post to server failed', server, e)
            }
        }
        throw new Error('all servers failed')
    }

    async get(auth, target) {
        if (!auth || typeof auth.buildAuthHeader !== 'function') {
            throw new Error('no auth')
        }
        for (const server of this.servers) {
            try {
                if (this.unreachable_neighbors.queryUnreachable(server)) {
                    continue
                }
                const url = "http://" + server + target // TODO https
                return await fetch(url, {
                    method: 'GET',
                    headers: {
                        ...auth.buildAuthHeader(url)
                    },
                    credentials: 'omit'
                }).catch(err => this.unreachable_neighbors.unreachable(server)
                ).then(response => response.json())
            } catch (e) {
                console.error('get from server failed', server, e)
            }
        }
        throw new Error('all servers failed')
    }
}

class authMethod {
    constructor(method, auth) {
        this.method = method;
        this.auth = auth;
    }

    buildAuthHeader(url, data) {
        return this.method(this.auth, {url, data})
    }

}

function createSignAuth(username, signKey) {
    const context = {username, signKey}
    if (!context.signKey || !context.username || typeof context.username !== 'string'
        || !(context.signKey instanceof Uint8Array) || context.signKey.length !== 64) {
        throw new Error('no signKey or username')
    }
    return new authMethod(({signKey, username}, {url, data}) => {
        const json = JSON.stringify(data)
        const signature = nacl.crypto_sign_detached(nacl.encode_utf8(url + (data ? json : "")), signKey)
        return {'Authorization': 'Signature ' + username + ':' + nacl.to_hex(signature)}
    }, context)
}

function createTokenAuth(token) {
    const context = {token}
    if (!context.token) {
        throw new Error('no token')
    }
    return new authMethod(({token}, {url, data}) => {
        return {'Authorization': 'Token ' + token}
    }, context)
}

export {ServerSet, createSignAuth, createTokenAuth}


