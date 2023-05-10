<script setup>

</script>

<template>
    <BaseLayout :username="username">
        <main class="container">
            <div class="row">
                <div class="col">
                    <div class="card">
                        <div class="card-header">Inventory</div>
                        <div class="card-body">
                            <table class="table table-striped">
                                <thead>
                                <tr>
                                    <th>Item</th>
                                    <th>Quantity</th>
                                    <th>Owner</th>
                                    <th>Actions</th>
                                </tr>
                                </thead>
                                <tbody>
                                <tr v-for="item in inventory_items" :key="item.id">
                                    <td>{{ item.name }}</td>
                                    <td>{{ item.quantity }}</td>
                                    <td>{{ item.owner }}</td>
                                    <td>
                                        <a href="#">
                                            <b-icon-pencil-square></b-icon-pencil-square>
                                        </a>
                                        <a href="#">
                                            <b-icon-trash></b-icon-trash>
                                        </a>
                                    </td>
                                </tr>
                                </tbody>
                            </table>
                        </div>
                        <div class="card">
                            <button class="btn" @click="getInventoryItems">Refresh</button>
                            <router-link to="/inventory/new" class="btn btn-primary">Add</router-link>
                        </div>
                    </div>
                </div>
            </div>
        </main>
    </BaseLayout>
</template>

<script>
import * as BIcons from "bootstrap-icons-vue";
import BaseLayout from "@/components/BaseLayout.vue";

export default {
    name: "InventoryEdit",
    components: {
        BaseLayout,
        ...BIcons
    },
}
</script>

<style scoped>

</style>