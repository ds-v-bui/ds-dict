<template>
    <div class="header">
        <md-content>
            <md-button class="brand" to="/">
                <img alt="branding logo and text" src="/logo_new.svg"/>
            </md-button>
            <div class="icons">
                <md-button @click="toggleLogin" v-if="user === undefined || user === null"
                           class="md-icon-button"
                           to="">
                    <md-tooltip>
                        Đăng nhập - Đăng kí
                    </md-tooltip>
                    <md-icon>account_circle</md-icon>
                </md-button>
                <md-button v-else class="md-icon-button" to="/profile">
                    <md-tooltip>
                        {{user.username}}
                    </md-tooltip>
                    <md-avatar class="md-avatar-icon">
                        {{user.username[0]}}
                    </md-avatar>
                </md-button>
            </div>
        </md-content>
        <div class="login">
            <md-dialog :md-active.sync="showLogin">
                <md-dialog-title>
                    Đăng nhập
                </md-dialog-title>

                <md-dialog-content>
                    <md-field>
                        <label>Email</label>
                        <md-input ref="email" autocomplete="email" name="email" type="email" required
                                  v-model="loginForm.email"
                                  @keypress.enter="login"/>
                        <span class="md-error" v-if="loginForm.email">
                            Email bắt buộc
                        </span>
                    </md-field>
                    <md-field>
                        <label>Password</label>
                        <md-input autocomplete="current-password" name="password" required type="password"
                                  v-model="loginForm.password"
                                  @keypress.enter="login"/>
                        <span class="md-error">
                            Password bắt buộc
                        </span>
                    </md-field>
                </md-dialog-content>

                <md-dialog-actions>
                    <md-button @click="showLogin = false" class="md-primary">
                        Đóng
                    </md-button>
                    <md-button @click="toggleRegister" class="md-primary">
                        Đăng kí
                    </md-button>
                    <md-button @click="login" class="md-primary">
                        Đăng nhập
                    </md-button>
                </md-dialog-actions>
            </md-dialog>
            <md-dialog :md-active.sync="showRegister">
                <md-dialog-title>
                    Đăng kí
                </md-dialog-title>

                <md-dialog-content>
                    <md-field>
                        <label>Username</label>
                        <md-input autocomplete="password" name="username" type="text" required
                                  v-model="registerForm.username"/>
                        <span class="md-error" v-if="registerForm.username">
                            Username bắt buộc
                        </span>
                    </md-field>
                    <md-field>
                        <label>Email</label>
                        <md-input autocomplete="email" name="email" type="email" required v-model="registerForm.email"/>
                        <span class="md-error" v-if="registerForm.email">
                            Email bắt buộc
                        </span>
                    </md-field>
                    <md-field>
                        <label>Password</label>
                        <md-input autocomplete="new-password" name="password" type="password" required
                                  v-model="registerForm.password"/>
                        <span class="md-error" v-if="registerForm.password">
                            Password bắt buộc
                        </span>
                    </md-field>
                </md-dialog-content>

                <md-dialog-actions>
                    <md-button @click="showRegister = false" class="md-primary">
                        Đóng
                    </md-button>
                    <md-button @click="register" class="md-primary">
                        Đăng kí
                    </md-button>
                </md-dialog-actions>
            </md-dialog>
        </div>
        <md-snackbar md-position="center" :md-active.sync="showSnackbar" md-persistent>
            <span v-if="user != null">Chào {{user.username}}!</span>
        </md-snackbar>
    </div>
</template>

<style scoped lang="scss">
    @import '~vue-material/dist/theme/engine';

    .header {
        position: relative;
        background-color: aqua;

        .brand {
            img {
                display: inline-block;
                width: 95px;
                height: auto;
            }
        }

        p {
            display: inline-block;
            padding: 0;
            margin-top: 20px;
            margin-bottom: 0;
        }

        .icons {
            position: absolute;
            top: 50%;
            transform: translate(0, -50%);
            right: 10px;
        }

        @media screen and (max-width: 768px) {
            .md-button {
                margin: 1px;
            }

            .brand {
                img {
                    display: inline-block;
                    width: auto;
                    height: 30px;
                }
            }

            p {
                display: none;
            }
        }
    }
</style>

<style lang="scss">
    @media screen and (max-width: 768px) {
        .header {
            .content {
                min-height: 50%;
                max-height: 50%;
            }

            .md-tabs-navigation .md-button {
                font-size: 10px;
            }

            .md-layout .md-layout-item {
                .md-chip {
                    margin: 0 0 5px 0;
                }

                padding: 0 !important;
                min-width: 100%;
                max-width: 100%;
            }
        }
    }
</style>

<script>
    export default {
        name: "Header",

        methods: {

            toggleLogin() {
                this.showLogin = !this.showLogin;
            },

            toggleRegister() {
                this.showLogin = false;
                this.showRegister = true;
            },

            async login() {
                await this.$store.dispatch('getToken', this.loginForm);
                this.$store.dispatch('getUser')
                    .then(() => {
                        this.showLogin = false;
                        this.showSnackbar = true;
                    });
            },

            register() {
                this.$store.dispatch('register', this.registerForm)
                .then(() => {
                    this.showRegister = false;
                });
            }
        },

        data: () => ({
            showLogin: false,
            showRegister: false,
            showSnackbar: false,
            loginForm: {
                email: "",
                password: ""
            },
            registerForm: {
                username: "",
                email: "",
                password: ""
            }
        }),

        computed: {
            user() {
                return this.$store.getters.getUser;
            }
        }
    }
</script>
