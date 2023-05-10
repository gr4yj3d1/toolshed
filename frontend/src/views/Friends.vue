<template>
    <BaseLayout>
        <main class="content">
            <div class="container-fluid p-0">
                <h1 class="h3 mb-3">Friends</h1>
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
                                    <th class="d-none d-md-table-cell" style="width:25%">Server</th>
                                    <th>Actions</th>
                                </tr>
                                </thead>
                                <tbody>
                                <tr v-for="friend in friends" :key="friend.name">
                                    <td>{{ friend.name }}</td>
                                    <td class="d-none d-md-table-cell">{{ friend.server.join(', ') }}</td>
                                    <td class="table-action">
                                        <a href="#">
                                            <b-icon-pencil-square></b-icon-pencil-square>
                                        </a>
                                        <a href="#">
                                            <b-icon-trash></b-icon-trash>
                                        </a>
                                    </td>
                                </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </main>
    </BaseLayout>
</template>

<script>
import {mapActions, mapGetters} from "vuex";
import * as BIcons from "bootstrap-icons-vue";
import BaseLayout from "@/components/BaseLayout.vue";

export default {
    name: 'Inventory',
    components: {
        BaseLayout,
        ...BIcons
    },
    data() {
        return {
            friends: [],
        }
    },
    computed: {
        username() {
            return this.$route.params.username
        },
        inventory_items() {
            return this.local_items.concat(this.eleon_items)
        }
    },
    methods: {
        ...mapActions(['getFriends', "getFriendServer"]),
    },
    mounted() {
        this.getFriends().then((friends) => {
            friends.map((friend) => {
                this.getFriendServer({username: friend}).then((server) => {
                    this.friends.push({
                        name: friend,
                        server: server
                    })
                })
            })
        })
    }
}
</script>

<style scoped>

</style>