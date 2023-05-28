<template>
    <BaseLayout>
        <main class="content">
            <div class="row">
                <div class="col">
                    <div class="card">
                        <div class="card-header">Edit Item</div>
                        <div class="card-body">
                            <div class="mb-3">
                                <span class="badge bg-dark" v-for="(tag, index) in item.tags" :key="index">
                                    {{ tag }}
                                </span>
                            </div>
                            <div class="mb-3">
                                <span class="badge bg-dark" v-for="(property, index) in item.properties" :key="index">
                                    {{ property.name }}={{ property.value }}
                                </span>
                            </div>
                            <div class="mb-3">
                                <label for="name" class="form-label">Name</label>
                                <input type="text" class="form-control" id="name" name="name"
                                       placeholder="Enter item name" v-model="item.name">
                            </div>
                            <div class="mb-3">
                                <label for="description" class="form-label">Description</label>
                                <textarea class="form-control" id="description" name="description"
                                          placeholder="Enter description" v-model="item.description"></textarea>
                            </div>
                            <div class="mb-3">
                                <label for="quantity" class="form-label">Quantity</label>
                                <input type="number" class="form-control" id="quantity" name="quantity"
                                       placeholder="Enter quantity" v-model="item.quantity">
                            </div>
                            <div class="mb-3">
                                <label for="price" class="form-label">Price</label>
                                <input type="number" class="form-control" id="price" name="price"
                                       placeholder="Enter price" v-model="item.price">
                            </div>
                            <div class="mb-3">
                                <label for="image" class="form-label">Image</label>
                                <input type="text" class="form-control" id="image" name="image"
                                       placeholder="Enter image" v-model="item.image">
                            </div>
                        </div>
                        <!--div class="card">
                            <button type="submit" class="btn btn-primary" @click="updateInventoryItem(item)">Update
                            </button>
                        </div-->
                    </div>
                </div>
            </div>
        </main>
    </BaseLayout>
</template>

<script>
import * as BIcons from "bootstrap-icons-vue";
import BaseLayout from "@/components/BaseLayout.vue";
import TagField from "@/components/TagField.vue";
import PropertyField from "@/components/PropertyField.vue";

export default {
    name: "InventoryDetail",
    data() {
        return {
            item: {
                name: "",
                description: "",
                quantity: 0,
                price: 0,
                image: "",
                tags: [],
                properties: []
            }
        }
    },
    components: {
        PropertyField, TagField,
        BaseLayout,
        ...BIcons
    },
}
</script>

<style scoped>

</style>