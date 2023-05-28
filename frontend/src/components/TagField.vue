<template>
    <div class="input-group">
        <div class="taglist form-control">
            <span class="badge bg-dark" v-for="(tag, index) in value" :key="index">
                {{ tag }}
                <i class="bi bi-x-circle-fill" @click="removeTag(index)"></i>
            </span>
        </div>
        <select class="form-select" id="tag" name="tag" v-model="tag">
            <option v-for="tag in availableTags" :key="tag" :value="tag">{{ tag }}</option>
        </select>
        <button class="btn btn-outline-secondary" type="button" @click="addTag">Add</button>
    </div>
</template>

<style scoped>
.taglist {
    display: flex;
    flex-wrap: wrap;
    gap: 0.3rem;
}
</style>

<script>
import * as BIcons from "bootstrap-icons-vue";
import {mapActions, mapState} from "vuex";

export default {
    name: "TagField",
    data() {
        return {
            tag: ""
        }
    },
    components: {
        ...BIcons
    },
    props: {
        value: {
            type: Array,
            required: true
        }
    },
    model: {
        prop: "value",
        event: "input"
    },
    computed: {
        ...mapState(["tags"]),
        availableTags() {
            return this.tags.filter(tag => !this.localValue.includes(tag));
        },
        localValue: {
            get() {
                return this.value;
            },
            set(value) {
                this.$emit("input", value);
                console.log("set", value);
            }
        }
    },
    methods: {
        ...mapActions(["fetchTags"]),
        addTag() {
            if (this.tag !== "") {
                this.localValue.push(this.tag);
                this.tag = "";
            }
        },
        removeTag(index) {
            this.localValue.splice(index, 1);
        }
    },
    mounted() {
        this.fetchTags();
    }
}
</script>