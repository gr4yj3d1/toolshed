<template>
    <div class="wrapper">
        <Sidebar/>
        <div class="main">
            <nav class="navbar navbar-expand navbar-light navbar-bg">
                <a class="sidebar-toggle d-flex">
                    <i class="hamburger align-self-center"></i>
                </a>
                <SearchBox/>
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
import Notifications from "@/components/Notifications.vue";
import Messages from "@/components/Messages.vue";
import Footer from "@/components/Footer.vue";
import Sidebar from "@/components/Sidebar.vue";
import UserDropdown from "@/components/UserDropdown.vue";
import SearchBox from "@/components/SearchBox.vue";

export default {
    name: 'BaseLayout',
    components: {
        SearchBox,
        UserDropdown,
        Sidebar,
        Footer,
        Messages,
        Notifications
    },
    computed: {
        ...mapState(['messages']),
        ...mapGetters(['notifications'])
    },
    async mounted() {
    }
}
</script>

<style scoped>

</style>