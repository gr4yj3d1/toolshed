<template>
    <form class="d-none d-sm-inline-block">
        <div class="input-group input-group-navbar">
            <input type="text" class="form-control" placeholder="Search…" aria-label="Search" v-model="query" id="searchText">
            <button class="btn" type="button" @click.prevent="search">
                <b-icon-search class="bi-valign-middle"></b-icon-search>
            </button>
        </div>
    </form>
</template>

<script>

import * as BIcons from "bootstrap-icons-vue";

export default {
    name: "SearchBox",
    components: {
        ...BIcons
    },
    data() {
        return {
            query: ""
        }
    },
    methods: {
        search() {
            if(this.query.length > 0)
                this.$router.push("/search/" + encodeURIComponent(this.query));
            else
                document.getElementById("searchText").focus();
        }
    },
    mounted() {
        console.log(this.$route)
        console.log(this.$route.params.query)
        this.query = decodeURIComponent(this.$route.params.query || encodeURIComponent(""));
    }
}
</script>

<style scoped>

</style>