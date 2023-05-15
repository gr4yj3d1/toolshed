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
                                    <th>Name</th>
                                    <th class="d-none d-md-table-cell" style="width:25%">Server</th>
                                    <th style="width: 16em">
                                        <a @click="fetchContent" class="align-middle">
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
                                    <td>{{ friend.username }}</td>
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
                    <div class="col-12 col-xl-6">
                        <div class="card">
                            <div class="card-header">
                                <h5 class="card-title">Requests</h5>
                                <h6 class="card-subtitle text-muted">Bar <code>baz</code>.</h6>
                            </div>
                            <table class="table table-striped">
                                <thead>
                                <tr>
                                    <th>Name</th>
                                    <th class="d-none d-md-table-cell" style="width:25%">Key</th>
                                    <th style="width: 16em">
                                        <a @click="fetchContent" class="align-middle">
                                            <b-icon-arrow-clockwise></b-icon-arrow-clockwise>
                                            Refresh
                                        </a>
                                    </th>
                                </tr>
                                </thead>
                                <tbody>
                                <tr v-for="request in requests" :key="request.befriender">
                                    <td>{{ request.befriender }}</td>
                                    <td class="d-none d-md-table-cell">
                                        {{ request.befriender_public_key.slice(0, 32) }}...
                                    </td>
                                    <td class="table-action">
                                        <button class="btn btn-sm btn-success" @click="tryAcceptFriend(request)">
                                            <b-icon-check></b-icon-check>
                                            Accept
                                        </button> &nbsp;
                                        <button class="btn btn-sm btn-danger" @click="tryRejectFriend(request)">
                                            <b-icon-x></b-icon-x>
                                            Decline
                                        </button>
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
            newfriend: "",
            requests: []
        }
    },
    computed: {
        username() {
            return this.$route.params.username
        },
        friendslist() {
            return Object.entries(this.friends).map(([_, friend]) => friend)
        }
    },
    methods: {
        ...mapActions(['fetchFriends', "lookupServer", "requestFriend", "acceptFriend", "fetchFriendRequests", "declineFriend"]),
        fetchContent() {
            this.fetchFriends().then((friends) => {
                friends.map((friend) => {
                    this.lookupServer(friend).then((server) => {
                        this.friends[friend.username] = {...friend, server: server}
                    })
                })
            })
            this.fetchFriendRequests().then((requests) => {
                this.requests = requests
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
                    this.fetchContent()
                }
            }).catch(() => {
            })
        },
        tryAcceptFriend(request) {
            this.acceptFriend({id: request.id, secret: request.secret, befriender: request.befriender}).then((ok) => {
                if (ok) {
                    this.fetchContent()
                }
            }).catch(() => {
            })
        },
        tryRejectFriend(friend) {
            this.declineFriend({username: friend}).then((ok) => {
                if (ok) {
                    this.fetchContent()
                }
            }).catch(() => {
            })
        }
    },
    mounted() {
        this.fetchContent()
    }
}
</script>

<style scoped>

</style>