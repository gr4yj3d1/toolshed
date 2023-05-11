<template>
    <main class="d-flex w-100">
        <div class="container d-flex flex-column">
            <div class="row vh-100">
                <div class="col-sm-10 col-md-8 col-lg-6 mx-auto d-table h-100">
                    <div class="d-table-cell align-middle">
                        <div class="text-center mt-4">
                            <h1 class="h2">
                                Toolshed
                            </h1>

                            <p class="lead" v-if="msg">
                                {{ msg }}
                            </p>
                            <p class="lead" v-else>
                                Create an account to get started
                            </p>
                        </div>
                        <div class="card">
                            <div class="card-body">
                                <div class="m-sm-4">
                                    <form role="form" method="post" @submit.prevent="do_register">
                                        <div :class="errors.username||errors.domain?['mb-3','is-invalid']:['mb-3']">
                                            <label class="form-label">Username</label>
                                            <div class="input-group">
                                                <input class="form-control form-control-lg"
                                                       type="text" v-model="form.username" id="validationCustomUsername"
                                                       placeholder="Enter your username" required/>

                                                <div class="input-group-prepend">
                                                    <span class="input-group-text form-control form-control-lg">@</span>
                                                </div>
                                                <select class="form-control form-control-lg"
                                                        id="exampleFormControlSelect1"
                                                        placeholder="Domain" v-model="form.domain" required>
                                                    <option v-for="domain in domains">{{ domain }}</option>
                                                </select>
                                            </div>
                                            <div class="invalid-feedback">
                                                {{ errors.username }}{{ errors.domain }}
                                            </div>
                                        </div>

                                        <div :class="errors.email?['mb-3','is-invalid']:['mb-3']">
                                            <label class="form-label">Email</label>
                                            <input class="form-control form-control-lg" type="email"
                                                   v-model="form.email" placeholder="Enter your email"/>
                                            <div class="invalid-feedback">{{ errors.email }}</div>
                                        </div>

                                        <div :class="errors.password?['mb-3','is-invalid']:['mb-3']">
                                            <label class="form-label">Password</label>
                                            <input class="form-control form-control-lg" type="password"
                                                   v-model="form.password" placeholder="Enter your password"/>
                                            <div class="invalid-feedback">{{ errors.password }}</div>
                                        </div>

                                        <div :class="errors.password2?['mb-3','is-invalid']:['mb-3']">
                                            <label class="form-label">Password Check</label>
                                            <input class="form-control form-control-lg" type="password"
                                                   v-model="password2" placeholder="Enter your password again"/>
                                            <div class="invalid-feedback">{{ errors.password2 }}</div>
                                        </div>

                                        <div class="text-center mt-3">
                                            <button type="submit" class="btn btn-lg btn-primary">
                                                Register
                                            </button>
                                        </div>
                                    </form>
                                    <br/>
                                    <div class="text-center">
                                        <p class="mb-0 text-muted">
                                            Already have an account?
                                            <router-link to="/login">Login</router-link>
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </main>
</template>

<script>
export default {
    name: 'Register',
    data() {
        return {
            msg: 'Register',
            password2: '',
            form: {
                username: '',
                domain: '',
                email: '',
                password: '',
            },
            errors: {
                username: null,
                domain: null,
                email: null,
                password: null,
                password2: null,
            },
            domains: []
        }
    },
    methods: {
        do_register() {
            console.log('do_register');
            console.log(this.form);
            if (this.form.password !== this.password2) {
                this.errors.password2 = 'Passwords do not match';
                return;
            } else {
                this.errors.password2 = null;
            }
            fetch('/auth/register/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(this.form)
            })
                .then(response => response.json())
                .then(data => {
                    if (data.errors) {
                        console.error('Error:', data.errors);
                        this.errors = data.errors;
                        return;
                    }
                    console.log('Success:', data);
                    this.msg = 'Success';
                    this.$router.push('/login');
                })
                .catch((error) => {
                    console.error('Error:', error);
                    this.msg = 'Error';
                });
        }
    },
    mounted() {
        fetch('/api/domains/')
            .then(response => response.json())
            .then(data => {
                this.domains = data;
            });
    }
}
</script>

<style scoped>
.is-invalid input, .is-invalid select {
    border: 1px solid var(--bs-danger);
}

.is-invalid .invalid-feedback {
    display: block;
}
</style>