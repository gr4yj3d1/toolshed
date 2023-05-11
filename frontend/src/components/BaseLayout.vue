<template>
    <div class="wrapper">
        <Sidebar/>
        <div class="main">
            <nav class="navbar navbar-expand navbar-light navbar-bg">
                <a class="sidebar-toggle d-flex">
                    <i class="hamburger align-self-center"></i>
                </a>
                <form class="d-none d-sm-inline-block">
                    <div class="input-group input-group-navbar">
                        <input type="text" class="form-control" placeholder="Search…" aria-label="Search">
                        <button class="btn" type="button">
                            <b-icon-search class="bi-valign-middle"></b-icon-search>
                        </button>
                    </div>
                </form>
                <div class="navbar-collapse collapse">
                    <ul class="navbar-nav navbar-align">
                        <Notifications :notifications="notifications"/>
                        <Messages :messages="messages"/>
                        <UserDropdown/>
                    </ul>
                </div>
            </nav>
            <slot></slot>
            <Footer/>
        </div>
    </div>
</template>

<script>
import {mapGetters, mapMutations, mapState} from 'vuex';
import * as BIcons from "bootstrap-icons-vue";
import Notifications from "@/components/Notifications.vue";
import Messages from "@/components/Messages.vue";
import Footer from "@/components/Footer.vue";
import Sidebar from "@/components/Sidebar.vue";
import UserDropdown from "@/components/UserDropdown.vue";

export default {
    name: 'BaseLayout',
    components: {
        UserDropdown,
        Sidebar,
        Footer,
        Messages,
        Notifications,
        ...BIcons
    },
    computed: {
        ...mapState(['messages']),
        ...mapGetters(['notifications']),
        username() {
            return this.$route.params.username
        },
    },
    methods: {
        ...mapMutations(['logout'])
    },
    async mounted() {
    }
}
</script>

<style scoped>

</style>