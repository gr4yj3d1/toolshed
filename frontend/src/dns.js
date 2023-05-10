import {query} from 'dns-query';

class FallBackResolver {
    constructor() {
        this._servers = ['1.1.1.1', '8.8.8.8'];
        this._cache = JSON.parse(localStorage.getItem('dns-cache')) || {};
    }

    async query(domain, type) {
        const key = domain + ':' + type;
        if (key in this._cache && this._cache[key].time > Date.now() - 1000 * 60 * 60) {
            const age_seconds = Math.ceil(Date.now() / 1000 - this._cache[key].time / 1000);
            console.log('cache hit', key, this._cache[key].ttl - age_seconds);
            return [this._cache[key].data];
        }
        const result = await query(
            {question: {type: type, name: domain}},
            {
                endpoints: this._servers,
            }
        )
        const first = result.answers[0];
        this._cache[key] = {time: Date.now(), ...first}; // TODO hadle multiple answers
        localStorage.setItem('dns-cache', JSON.stringify(this._cache));
        console.log('cache miss', key, first.ttl);
        return [first.data];
    }
}

export default FallBackResolver;