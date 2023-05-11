<template>
    <nav id="sidebar" class="sidebar">
        <div class="sidebar-content js-simplebar">
            <router-link to="/" class="sidebar-brand">
                <span class="align-middle">Toolshed</span>
            </router-link>
            <ul class="sidebar-nav">
                <li class="sidebar-header">
                    Tools & Components
                </li>
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
</template>

<script>

export default {
    name: "Sidebar"
}
</script>

<style scoped>

</style>