<template>
    <div class="input-group">
        <div class="taglist form-control form-control-lg">
            <span class="badge bg-dark" v-for="(property, index) in value" :key="index">
                {{ property.name }} =
                <input type="number" class="form-control form-control-inline form-control-sm form-control-xsm bg-dark text-light border-dark"
                       id="propertyValue" name="propertyValue" placeholder="Enter value"
                       v-model="property.value">
                <i class="bi bi-x-circle-fill" @click="removeProperty(index)"></i>
            </span>
        </div>
        <select class="form-select form-control form-control-lg" id="property" name="property" v-model="property">
            <option v-for="(property, index) in availableProperties" :key="index" :value="property">{{ property }}</option>
        </select>
        <button class="btn btn-outline-secondary" type="button" @click="addProperty">Add</button>
    </div>
</template>

<style scoped>
.form-control-inline {
    display: inline;
    width: auto;
}

.taglist {
    display: flex;
    flex-wrap: wrap;
    gap: 0.3rem;
}

.form-control-xsm {
    min-height: calc(.6rem);
    padding: .0rem .5rem;
    font-size: .6rem;
    border-radius: .1rem;
}

input[type=number].form-control-xsm{
    padding: 0 0 0 .5rem;
}
</style>

<script>
import * as BIcons from "bootstrap-icons-vue";
import {mapActions, mapState} from "vuex";

export default {
    name: "PropertyField",
    data() {
        return {
            property: ""
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
        ...mapState(["properties"]),
        availableProperties() {
            return this.properties.filter(property => !this.localValue.map(p => p.name).includes(property));
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
        ...mapActions(["fetchProperties"]),
        addProperty() {
            if (this.property !== "") {
                this.localValue.push({name: this.property, value: 0});
                this.property = "";
            }
        },
        removeProperty(index) {
            this.localValue.splice(index, 1);
        }
    },
    mounted() {
        this.fetchProperties();
    }
}
</script>