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
                                <tr v-for="friend in friendslist" :key="friend.name">
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
                        <div class="card">
                            <button class="btn" @click="fetchFriends">Refresh</button>
                            <router-link to="/inventory/new" class="btn btn-primary">Add</router-link>
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
            friends: {},
        }
    },
    computed: {
        username() {
            return this.$route.params.username
        },
        friendslist() {
            return Object.keys(this.friends).map((friend) => {
                return {
                    name: friend,
                    server: this.friends[friend]
                }
            })
        }
    },
    methods: {
        ...mapActions(['getFriends', "getFriendServer"]),
        fetchFriends() {
            this.getFriends().then((friends) => {
                friends.map((friend) => {
                    this.getFriendServer({username: friend}).then((server) => {
                        this.friends[friend] = server
                    })
                })
            })
        }
    },
    mounted() {
        this.fetchFriends()
    }
}
</script>

<style scoped>

</style>