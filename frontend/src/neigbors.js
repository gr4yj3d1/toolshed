class NeighborsCache {
    constructor() {
        //this._max_age = 1000 * 60 * 60; // 1 hour
        this._max_age = 1000 * 60 * 5; // 5 minutes
        this._cache = JSON.parse(localStorage.getItem('neighbor-cache')) || {};
    }

    reachable(domain) {
        console.log('reachable neighbor ' + domain)
        if (domain in this._cache) {
            delete this._cache[domain];
            localStorage.setItem('neighbor-cache', JSON.stringify(this._cache));
        }
    }

    unreachable(domain) {
        console.log('unreachable neighbor ' + domain)
        this._cache[domain] = {time: Date.now()};
        localStorage.setItem('neighbor-cache', JSON.stringify(this._cache));
    }

    queryUnreachable(domain) {
        //return false if unreachable
        if (domain in this._cache) {
            if (this._cache[domain].time > Date.now() - this._max_age) {
                console.log('skip unreachable neighbor ' + domain + ' ' + Math.ceil(
                    Date.now()/1000 - this._cache[domain].time/1000) + 's/' + Math.ceil(this._max_age/1000) + 's')
                return true
            } else {
                delete this._cache[domain];
                localStorage.setItem('neighbor-cache', JSON.stringify(this._cache));
            }
        }
        return false;
    }

    list() {
        return Object.entries(this._cache).map(([domain, elem]) => {
            return {
                domain: domain,
                time: elem.time
            }
        })
    }
}

export default NeighborsCache;