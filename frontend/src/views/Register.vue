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
                                    <form role="form" method="post" action="">
                                        <!--{% csrf_token %}-->
                                        <div class="mb-3">
                                            <label class="form-label">Username</label>
                                            <input class="form-control form-control-lg" type="text"
                                                   name="username" placeholder="Enter your username"/>
                                        </div>
                                        <span class="text-error">{{ form.username.errors }}</span>
                                        <div class="mb-3">
                                            <label class="form-label">Email</label>
                                            <input class="form-control form-control-lg" type="email"
                                                   name="email" placeholder="Enter your email"/>
                                        </div>
                                        <span class="text-error">{{ form.email.errors }}</span>
                                        <div class="mb-3">
                                            <label class="form-label">Password</label>
                                            <input class="form-control form-control-lg" type="password"
                                                   name="password1" placeholder="Enter your password"/>
                                        </div>
                                        <span class="text-error">{{ form.password1.errors }}</span>
                                        <div class="mb-3">
                                            <label class="form-label">Password Check</label>
                                            <input class="form-control form-control-lg" type="password"
                                                   name="password2" placeholder="Enter your password again"/>
                                        </div>
                                        <span class="text-error">{{ form.password2.errors }}</span>
                                        <div class="text-center mt-3">
                                            <button type="submit" name="register" class="btn btn-lg btn-primary">
                                                Register
                                            </button>
                                        </div>
                                    </form>
                                    <br/>
                                    <div class="text-center">
                                        <p class="mb-0 text-muted">
                                            Already have an account? <router-link to="/login">Login</router-link>
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
            form: {
                username: '',
                email: '',
                password1: '',
                password2: '',}
        }
    }
}
</script>

<style scoped>

</style>