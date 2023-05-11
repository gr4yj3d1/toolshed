<template>
    <li class="nav-item dropdown">
        <a class="nav-icon dropdown-toggle d-inline-block d-sm-none" href="#"
           data-toggle="dropdown">
            <i class="align-middle" data-feather="settings"></i>
            <b-icon-chat-left class="bi-valign-middle"></b-icon-chat-left>
        </a>

        <a class="nav-link dropdown-toggle d-none d-sm-inline-block" href="#"
           data-toggle="dropdown">
            <img src="/assets/img/avatars/avatar.png" class="avatar img-fluid rounded mr-1"
                 alt="Charles Hall"/>
            <span class="text-dark">
                        {{ username }}
                    </span>
        </a>

        <div class="dropdown-menu dropdown-menu-right">
            <router-link to="/profile" class="dropdown-item">
                <b-icon-person class="bi-valign-middle mr-1"></b-icon-person>
                Profile
            </router-link>
            <router-link to="/settings" class="dropdown-item">
                <b-icon-sliders class="bi-valign-middle mr-1"></b-icon-sliders>
                Settings &
                Privacy
            </router-link>
            <div class="dropdown-divider"></div>
            <a class="dropdown-item" href="#" @click="logout"> Log out</a>
        </div>
    </li>
</template>

<script>
import * as BIcons from "bootstrap-icons-vue";
import {mapMutations} from "vuex";

export default {
    name: "UserDropdown",
    components: {
        ...BIcons
    },
    methods: {
        ...mapMutations(['logout'])
    },
    computed: {
        username() {
            return this.$route.params.username
        },
    }
}
</script>

<style scoped>

</style>