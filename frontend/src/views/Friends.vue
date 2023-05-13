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
                                    <th>
                                        <a @click="fetchFriends" class="align-middle">
                                            <b-icon-arrow-clockwise></b-icon-arrow-clockwise>
                                            Refresh
                                        </a>
                                        <a @click="showNewFriend" class="align-middle">
                                            <b-icon-plus></b-icon-plus>
                                            Add Friend
                                        </a>
                                    </th>
                                </tr>
                                </thead>
                                <tbody>
                                <tr v-if="show_newfriend">
                                    <td colspan="2">
                                        <input type="text" class="form-control" placeholder="user@domain"
                                               v-model="newfriend">
                                    </td>
                                    <td>
                                        <button class="btn btn-primary" @click="tryRequestFriend">Send Request</button>
                                    </td>
                                </tr>
                                <tr v-for="friend in friendslist" :key="friend.name">
                                    <td>{{ friend.name }}</td>
                                    <td class="d-none d-md-table-cell">{{ friend.server.join(', ') }}</td>
                                    <td class="table-action">
                                        <a href="#" class="align-middle">
                                            <b-icon-pencil-square></b-icon-pencil-square>
                                            Edit
                                        </a>
                                        <a href="#" class="align-middle">
                                            <b-icon-trash></b-icon-trash>
                                            Delete
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
            friends: {},
            show_newfriend: false,
            newfriend: ""
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
        ...mapActions(['getFriends', "getFriendServer", "requestFriend"]),
        fetchFriends() {
            this.getFriends().then((friends) => {
                friends.map((friend) => {
                    this.getFriendServer({username: friend}).then((server) => {
                        this.friends[friend] = server
                    })
                })
            })
        },
        showNewFriend() {
            this.show_newfriend = true
        },
        tryRequestFriend() {
            this.requestFriend({username: this.newfriend}).then((ok) => {
                if (ok) {
                    this.show_newfriend = false
                    this.newfriend = ""
                    this.fetchFriends()
                }
            }).catch(() => {})
        }
    },
    mounted() {
        this.fetchFriends()
    }
}
</script>

<style scoped>

</style>