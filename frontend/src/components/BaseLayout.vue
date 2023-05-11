<template>
    <div class="wrapper">
        <nav id="sidebar" class="sidebar">
            <div class="sidebar-content js-simplebar">
                <router-link to="/" class="sidebar-brand">
                    <span class="align-middle">Toolshed</span>
                </router-link>
                <ul class="sidebar-nav">
                    <li class="sidebar-header">
                        Tools & Components
                    </li>
                    <!--
                    <li class="sidebar-item {% if 'icons' in segment %} active {% endif %}">
                        <a class="sidebar-link" href="{% url 'inventory' %}">
                            {% bs_icon 'archive' extra_classes="bi-valign-middle" %}
                            <span class="align-middle">Inventory</span>
                        </a>
                    </li>
                    -->
                    <li class="sidebar-item">
                        <router-link to="/inventory" class="sidebar-link">
                            <b-icon-archive class="bi-valign-middle"></b-icon-archive>
                            <span class="align-middle">Inventory</span>
                        </router-link>
                    </li>
                    <li class="sidebar-item">
                        <router-link to="/friends" class="sidebar-link">
                            <b-icon-people class="bi-valign-middle"></b-icon-people>
                            <span class="align-middle">Friends</span>
                        </router-link>
                    </li>
                </ul>
            </div>
        </nav>
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
                        <li class="nav-item dropdown">
                            <a class="nav-icon dropdown-toggle" href="#" id="messagesDropdown" data-toggle="dropdown">
                                <div class="position-relative">
                                    <b-icon-chat-left class="bi-valign-middle"></b-icon-chat-left>
                                </div>
                            </a>
                            <div class="dropdown-menu dropdown-menu-lg dropdown-menu-right py-0"
                                 aria-labelledby="messagesDropdown">
                                <div class="dropdown-menu-header">
                                    <div class="position-relative">
                                        4 New Messages
                                    </div>
                                </div>
                                <div class="list-group">
                                    <a href="#" class="list-group-item">
                                        <div class="row g-0 align-items-center">
                                            <div class="col-2">
                                                <!--<img src="/static/assets/img/avatars/avatar-5.png"
                                                     class="avatar img-fluid rounded-circle" alt="Vanessa Tucker">-->
                                            </div>
                                            <div class="col-10 pl-2">
                                                <div class="text-dark">Vanessa Tucker</div>
                                                <div class="text-muted small mt-1">Nam pretium turpis et arcu. Duis arcu
                                                    tortor.
                                                </div>
                                                <div class="text-muted small mt-1">15m ago</div>
                                            </div>
                                        </div>
                                    </a>
                                    <a href="#" class="list-group-item">
                                        <div class="row g-0 align-items-center">
                                            <div class="col-2">
                                                <!--<img src="/static/assets/img/avatars/avatar-2.png"
                                                     class="avatar img-fluid rounded-circle" alt="William Harris">-->
                                            </div>
                                            <div class="col-10 pl-2">
                                                <div class="text-dark">William Harris</div>
                                                <div class="text-muted small mt-1">Curabitur ligula sapien euismod
                                                    vitae.
                                                </div>
                                                <div class="text-muted small mt-1">2h ago</div>
                                            </div>
                                        </div>
                                    </a>
                                    <a href="#" class="list-group-item">
                                        <div class="row g-0 align-items-center">
                                            <div class="col-2">
                                                <!--<img src="/static/assets/img/avatars/avatar-4.png"
                                                     class="avatar img-fluid rounded-circle" alt="Christina Mason">-->
                                            </div>
                                            <div class="col-10 pl-2">
                                                <div class="text-dark">Christina Mason</div>
                                                <div class="text-muted small mt-1">Pellentesque auctor neque nec urna.
                                                </div>
                                                <div class="text-muted small mt-1">4h ago</div>
                                            </div>
                                        </div>
                                    </a>
                                   <!-- {% for messege in top_messages %}-->
                                    <a href="#" class="list-group-item">
                                        <div class="row g-0 align-items-center">
                                            <div class="col-2">
                                                <!--<img src="/static/assets/img/avatars/avatar-3.png"
                                                     class="avatar img-fluid rounded-circle" alt="Sharon Lessman">-->
                                            </div>
                                            <div class="col-10 pl-2">
                                                <div class="text-dark">Sharon Lessman</div>
                                                <div class="text-muted small mt-1">Aenean tellus metus, bibendum sed,
                                                    posuere ac,
                                                    mattis non.
                                                </div>
                                                <div class="text-muted small mt-1">5h ago</div>
                                            </div>
                                        </div>
                                    </a>
                                    <!--{% endfor %}-->
                                </div>
                                <div class="dropdown-menu-footer">
                                    <a href="#" class="text-muted">Show all messages</a>
                                </div>
                            </div>
                        </li>
                        <li class="nav-item dropdown">
                            <a class="nav-icon dropdown-toggle d-inline-block d-sm-none" href="#"
                               data-toggle="dropdown">
                                <i class="align-middle" data-feather="settings"></i>
                                <b-icon-chat-left class="bi-valign-middle"></b-icon-chat-left>
                            </a>

                            <a class="nav-link dropdown-toggle d-none d-sm-inline-block" href="#"
                               data-toggle="dropdown">
                                <!--<img src="/static/assets/img/avatars/avatar.png" class="avatar img-fluid rounded mr-1"
                                     alt="Charles Hall"/>-->
                                <span class="text-dark">
                        <!--{{ request.user.username }}-->
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
                    </ul>
                </div>
            </nav>
            <slot></slot>
            <footer class="footer">
                <div class="container-fluid">
                    <div class="row text-muted">
                        <div class="col-6 text-left">
                            <p class="mb-0">
                                <a target="_blank" href="https://www.gnu.org/licenses/gpl-3.0.de.html"
                                   class="text-muted">
                                    License: <strong>GPL-3.0</strong>
                                </a>
                            </p>
                        </div>
                        <div class="col-6 text-right">
                            <ul class="list-inline">
                                <li class="list-inline-item">
                                    <a class="text-muted"
                                       target="_blank" href="https://github.com/gr4yj3d1/toolshed">Dev Docs</a>
                                </li>
                                <li class="list-inline-item">
                                    <a class="text-muted"
                                       target="_blank" href="https://github.com/gr4yj3d1/toolshed">Sources</a>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
            </footer>
        </div>
    </div>
</template>

<script>
import {mapGetters, mapMutations, mapState} from 'vuex';
import * as BIcons from "bootstrap-icons-vue";
import Notifications from "@/components/Notifications.vue";

export default {
    name: 'BaseLayout',
    components: {
        Notifications,
        ...BIcons
    },
    computed: {
        //...mapState(['notifications']),
        ...mapGetters(['notifications']),
        username() {
            return this.$route.params.username
        },
        top_notifications() {
            return this.notifications.slice(0, 5)
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