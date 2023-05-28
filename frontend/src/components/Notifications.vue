<template>
    <li class="nav-item dropdown">
        <a class="nav-icon dropdown-toggle" href="#" id="alertsDropdown" data-toggle="dropdown">
            <div class="position-relative">
                <b-icon-bell class="bi-valign-middle"></b-icon-bell>
                <span :class="['indicator', notificationsColor(top_notifications)]">{{
                    top_notifications.length
                    }}</span>
            </div>
        </a>
        <div class="dropdown-menu dropdown-menu-lg dropdown-menu-right py-0"
             aria-labelledby="alertsDropdown">
            <div class="dropdown-menu-header">
                {{ top_notifications.length }} New Notifications
            </div>
            <div class="list-group">
                <a href="#" class="list-group-item" v-for="notification in top_notifications" :key="notification.id">
                    <div class="row g-0 align-items-center">
                        <div class="col-2">
                            <b-icon-exclamation-circle class="bi-valign-middle text-danger"
                                                       v-if="notification.type === 'error'"></b-icon-exclamation-circle>
                            <b-icon-info-circle class="bi-valign-middle text-info"
                                                v-else-if="notification.type === 'info'"></b-icon-info-circle>
                            <b-icon-check-circle class="bi-valign-middle text-success"
                                                 v-else-if="notification.type === 'success'"></b-icon-check-circle>
                            <b-icon-bell class="bi-valign-middle text-warning"
                                         v-else-if="notification.type === 'warning'"></b-icon-bell>
                            <b-icon-house class="bi-valign-middle text-primary"
                                          v-else-if="notification.type === 'login'"></b-icon-house>
                            <b-icon-person-plus class="bi-valign-middle text-success"
                                                v-else-if="notification.type === 'friend'"></b-icon-person-plus>
                        </div>
                        <div class="col-10">
                            <div class="text-dark">{{ notification.title }}</div>
                            <div class="text-muted small mt-1" v-if="notification.msg">{{ notification.msg }}</div>
                            <div class="text-muted small mt-1">{{ humanizeTime(notification.time) }}</div>
                        </div>
                    </div>
                </a>
            </div>
            <div class="dropdown-menu-footer">
                <a href="#" class="text-muted">Show all notifications</a>
            </div>
        </div>
    </li>
</template>

<script>
import {mapGetters, mapMutations} from 'vuex';
import * as BIcons from "bootstrap-icons-vue";
import moment from 'moment';

export default {
    name: 'Notifications',
    components: {
        ...BIcons
    },
    props: {
        notifications: {
            type: Array,
            default: () => []
        }
    },
    computed: {
        top_notifications() {
            return this.notifications.sort((a, b) => {
                return new Date(b.time) - new Date(a.time);
            }).slice(0, 8);
        },
    },
    methods: {
        ...mapMutations([]),
        humanizeTime(time) {
            return moment(time).fromNow();
        },
        notificationsColor(notifications) {
            if (notifications.length === 0) {
                return 'invisible';
            }
            if (notifications.filter(n => n.type === 'error').length > 0) {
                return 'bg-danger';
            }
            if (notifications.filter(n => n.type === 'warning').length > 0) {
                return 'bg-warning';
            }
            return 'bg-primary';
        }
    },
    async mounted() {
    }
}
</script>

<style scoped>

</style>