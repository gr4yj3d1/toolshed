<template>
    <BaseLayout>
        <main class="content">
            <div class="container-fluid p-0">
                <h1 class="h3 mb-3">Inventory Own & Friends"</h1>
                <div class="row">
                    <div class="col-12 col-xl-6">
                        <div class="card">
                            <div class="card-header">
                                <h5 class="card-title">Foo</h5>
                                <h6 class="card-subtitle text-muted">Bar <code>baz</code>.</h6>
                            </div>
                            <table class="table table-striped">
                                <thead>
                                <tr>
                                    <th style="width:40%;">Name</th>
                                    <th style="width:25%">Owner</th>
                                    <th class="d-none d-md-table-cell" style="width:25%">Amount</th>
                                    <th>Actions</th>
                                </tr>
                                </thead>
                                <tbody>
                                <tr v-for="item in inventory_items" :key="item.id">
                                    <td>
                                        <router-link :to="`/inventory/${item.id}`">{{ item.name }}</router-link>
                                    </td>
                                    <td>{{ item.owner }}</td>
                                    <td class="d-none d-md-table-cell">{{ item.owned_amount }}</td>
                                    <td class="table-action">
                                        <router-link :to="`/inventory/${item.id}/edit`">
                                            <b-icon-pencil-square></b-icon-pencil-square>
                                        </router-link>
                                        <a :href="`/inventory/${item.id}/delete`" @click.prevent="deleteItem(item.id)">
                                            <b-icon-trash></b-icon-trash>
                                        </a>
                                    </td>
                                </tr>
                                </tbody>
                            </table>
                        </div>
                        <div class="card">
                            <button class="btn" @click="getInventoryItems">Refresh</button>
                            <router-link to="/inventory/new" class="btn btn-primary">Add</router-link>
                        </div>
                    </div>
                </div>
            </div>
        </main>
    </BaseLayout>
</template>

<script>
import {mapActions, mapGetters, mapMutations, mapState} from "vuex";
import * as BIcons from "bootstrap-icons-vue";
import BaseLayout from "@/components/BaseLayout.vue";

export default {
    name: "Inventory",
    components: {
        BaseLayout,
        ...BIcons
    },
    computed: {
        ...mapGetters(["inventory_items"]),
        username() {
            return this.$route.params.username
        }
    },
    methods: {
        ...mapActions(["apiFederatedGet", "getFriends", "getFriendServer"]),
        ...mapMutations(["setInventoryItems"]),
        async getInventoryItems() {
            try {
                const servers = await this.getFriends().then(friends => friends.map(friend => this.getFriendServer({username: friend})))
                const urls = servers.map(server => server.then(s => {
                    return {host: `http://${s}`, target: "/api/inventory_items/"}
                }))
                urls.map(url => url.then(u => this.apiFederatedGet(u).then(items => {
                    this.setInventoryItems({url: u.domain, items})
                }).catch(e => {
                }))) // TODO: handle error
            } catch (e) {
                console.error(e)
            }
        },
    },
    async mounted() {
        await this.getInventoryItems()
    }
}
</script>

<style scoped>

</style>