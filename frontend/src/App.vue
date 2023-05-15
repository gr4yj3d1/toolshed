<script setup>
</script>

<template>
    <router-view></router-view>
    <!-- TODO UI für Freunde liste, add, remove -->
</template>

<script>


import {mapMutations} from 'vuex';
import store from '@/store';

export default {
    name: 'App',
    methods: {
        ...mapMutations(['init']),
    },
    beforeCreate () {
        store.commit('load_local')
    }
}
</script>

<style scoped>

</style>
