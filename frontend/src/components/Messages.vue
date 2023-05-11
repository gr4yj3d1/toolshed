<template>
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
                            <img src="/assets/img/avatars/avatar-5.png"
                                 class="avatar img-fluid rounded-circle" alt="Vanessa Tucker">
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
                            <img src="/assets/img/avatars/avatar-2.png"
                                 class="avatar img-fluid rounded-circle" alt="William Harris">
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
                            <img src="/assets/img/avatars/avatar-4.png"
                                 class="avatar img-fluid rounded-circle" alt="Christina Mason">
                        </div>
                        <div class="col-10 pl-2">
                            <div class="text-dark">Christina Mason</div>
                            <div class="text-muted small mt-1">Pellentesque auctor neque nec urna.
                            </div>
                            <div class="text-muted small mt-1">4h ago</div>
                        </div>
                    </div>
                </a>
                <a href="#" class="list-group-item">
                    <div class="row g-0 align-items-center">
                        <div class="col-2">
                            <img src="/assets/img/avatars/avatar-3.png"
                                 class="avatar img-fluid rounded-circle" alt="Sharon Lessman">
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
            </div>
            <div class="dropdown-menu-footer">
                <a href="#" class="text-muted">Show all messages</a>
            </div>
        </div>
    </li>
</template>

<script>
import {mapGetters, mapMutations} from 'vuex';
import * as BIcons from "bootstrap-icons-vue";

export default {
    name: "Messages",
    components: {
        ...BIcons
    },
    props: {
        messages: {
            type: Array,
            default: () => []
        }
    },
    computed: {
        top_messages() {
            return this.messages.slice(0, 4);
        }
    }
}
</script>

<style scoped>

</style>