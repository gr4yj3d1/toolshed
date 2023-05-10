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
                                Sign in to your account to continue
                            </p>
                        </div>
                        <div class="card">
                            <div class="card-body">
                                <div class="m-sm-4">
                                    <form role="form" @submit.prevent="do_login">

                                        <div class="mb-3">
                                            <label class="form-label">Username</label>
                                            <input class="form-control form-control-lg" type="text"
                                                   name="username" placeholder="Enter your username"
                                                   v-model="username"/>
                                        </div>
                                        <div class="mb-3">
                                            <label class="form-label">Password</label>
                                            <input class="form-control form-control-lg" type="password"
                                                   name="password" placeholder="Enter your password"
                                                   v-model="password"/>
                                        </div>
                                        <div>
                                            <label class="form-check">
                                                <input class="form-check-input" type="checkbox" value="remember-me"
                                                       name="remember-me" checked v-model="remember"
                                                       @change="setRemember(remember)">
                                                <span class="form-check-label">
												Remember me next time
												</span>
                                            </label>
                                        </div>
                                        <div class="text-center mt-3">
                                            <button type="submit" name="login" class="btn btn-lg btn-primary">Login
                                            </button>
                                        </div>
                                    </form>
                                    <br/>
                                    <div class="text-center">
                                        <p class="mb-0 text-muted">
                                            Don’t have an account?
                                            <router-link to="/register">Sign up</router-link>
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
import {mapActions, mapMutations} from 'vuex';

export default {
    name: 'Login',
    data() {
        return {
            msg: 'Welcome to Your Vue.js App',
            username: '',
            password: '',
            remember: false
        }
    },
    methods: {
        ...mapActions(['login']),
        ...mapMutations(['setRemember']),
        async do_login(e) {
            e.preventDefault();
            if (!await this.login({username: this.username, password: this.password, remember: this.remember})) {
                this.msg = 'Invalid username or password';
            }

        },

    }
}
</script>

<style scoped>

</style>