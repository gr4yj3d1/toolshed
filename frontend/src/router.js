import {createRouter, createWebHistory} from 'vue-router'
import Index from '@/views/Index.vue';
import Login from '@/views/Login.vue';
import Register from '@/views/Register.vue';
import store from '@/store';
import Profile from '@/views/Profile.vue';
import Settings from '@/views/Settings.vue';
import Inventory from '@/views/Inventory.vue';
import Friends from "@/views/Friends.vue";
import InventoryNew from "@/views/InventoryNew.vue";
import InventoryEdit from "@/views/InventoryEdit.vue";
import InventoryDetail from "@/views/InventoryDetail.vue";


const routes = [
    {path: '/', component: Index, meta: {requiresAuth: true}},
    {path: '/profile', component: Profile, meta: {requiresAuth: true}},
    {path: '/settings', component: Settings, meta: {requiresAuth: true}},
    {path: '/inventory', component: Inventory, meta: {requiresAuth: true}},
    {path: '/inventory/:id', component: InventoryDetail, meta: {requiresAuth: true}},
    {path: '/inventory/:id/edit', component: InventoryEdit, meta: {requiresAuth: true}},
    {path: '/inventory/new', component: InventoryNew, meta: {requiresAuth: true}},
    {path: '/friends', component: Friends, meta: {requiresAuth: true}},
    {path: '/login', component: Login, meta: {requiresAuth: false}},
    {path: '/register', component: Register, meta: {requiresAuth: false}},
]

const router = createRouter({
    // 4. Provide the history implementation to use. We are using the hash history for simplicity here.
    history: createWebHistory(),
    linkActiveClass: "active",
    routes, // short for `routes: routes`
})

router.beforeEach((to, from) => {
    // instead of having to check every route record with
    // to.matched.some(record => record.meta.requiresAuth)
    if (to.meta.requiresAuth && !store.getters.isLoggedIn) {
        // this route requires auth, check if logged in
        // if not, redirect to login page.
        return {
            path: '/login',
            // save the location we were at to come back later
            query: {redirect: to.fullPath},
        }
    }
})

export default router