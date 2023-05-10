import {createApp} from 'vue'
//import { BootstrapVue, BootstrapVueIcons } from 'bootstrap-vue'
import { BootstrapIconsPlugin } from 'bootstrap-icons-vue';
import App from './App.vue'

import './assets/css/toolshed.css'
import './assets/js/app.js'

import router from './router'
import store from './store';

import _nacl from 'js-nacl';

const app = createApp(App).use(router).use(store).use(BootstrapIconsPlugin);

_nacl.instantiate((nacl) => {
    window.nacl = nacl
    app.mount('#app')
});
