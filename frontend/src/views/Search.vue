<template>
    <BaseLayout>
        <main class="content">
            <div class="container-fluid p-0">
                <h1 class="h3 mb-3">Blank Page</h1>
                <div class="row">
                    <div class="col-12">
                        <div class="card">
                            <div class="card-header">
                                <h5 class="card-title mb-0">Empty card</h5>
                            </div>
                            <div class="card-body">
                                <div class="logo">
                                    <img src="/src/assets/icons/toolshed-48x48.png" alt="Toolshed logo">
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </main>
    </BaseLayout>
</template>

<script>
import {mapGetters, mapMutations} from 'vuex';
import * as BIcons from "bootstrap-icons-vue";
import BaseLayout from "@/components/BaseLayout.vue";

export default {
    name: 'Search',
    components: {
        ...BIcons,
        BaseLayout
    },
}
</script>

<style scoped>

</style>