import Vue from 'vue'

import VueMaterial from 'vue-material'
import 'vue-material/dist/vue-material.min.css'
import 'ant-design-vue/dist/antd.css';
import './themes/light.scss'
import './themes/dark.scss'

import App from './App.vue'
import Home from './components/Home.vue'
import MissingPage from './components/MissingPage.vue'
import Profile from "./components/Profile";
import VueRouter from "vue-router";
import Vuex from 'vuex'
import VueCookies from 'vue-cookies'
import axios from 'axios'
import qs from 'querystring'

Vue.config.productionTip = false;

Vue.prototype.$hostname = 'http://127.0.0.1:8000';

Vue.use(VueMaterial);
Vue.use(VueRouter);
Vue.use(Vuex);
Vue.use(VueCookies);

VueCookies.config(-1);

const router = new VueRouter({
    mode: 'history',
    routes: [
        {path: '/', name: '/', component: Home},
        {path: '/profile', name: 'profile', component: Profile},
        {path: '*', component: MissingPage}
    ]
});

const store = new Vuex.Store({
    strict: process.env.NODE_ENV !== 'production',

    state: {
        isDark: VueCookies.get("isDark") === "true",
        user: null
    },

    getters: {
        isDark: (state) => {
            return state.isDark;
        },

        getUser: (state) => {
            return state.user;
        }
    },

    mutations: {
        toggleTheme(state) {
            if (state.isDark)
                Vue.material.theming.theme = "light";
            else
                Vue.material.theming.theme = "dark";

            state.isDark = !state.isDark;
            VueCookies.set("isDark", state.isDark);
        },
        setUser(state, user) {
            state.user = user;
        }
    },

    actions: {
        getUser(store) {
            return axios.get(
                Vue.prototype.$hostname + '/users',
                {
                    withCredentials: true
                })
                .then(response => {
                    store.commit('setUser', response.data);
                })
                .catch(() => {
                })
        },

        getToken(store, form) {
            return axios.post(
                Vue.prototype.$hostname + '/users/login',
                qs.stringify(form),
                {
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    },
                    withCredentials: true
                })
                .then(res => {
                    if (res.status === 200)
                        store.dispatch('getUser');
                })
                .catch(() => alert("Lỗi!"));
        },

        register(store, form) {
            return axios.post(
                Vue.prototype.$hostname + '/users/create',
                qs.stringify(form),
                {
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    }
                })
                .then(res => {
                    if (res.status === 201)
                        store.dispatch(
                            'getToken',
                            {
                                email: form.email,
                                password: form.password
                            }
                        );
                })
                .catch(() => alert("Tài khoản tồn tại"));
        }
    }
});

store.dispatch('getUser').then(() => {
}).catch(() => {
});

if (store.getters.isDark)
    Vue.material.theming.theme = "dark";
else
    Vue.material.theming.theme = "light";

new Vue({
    components: {App},
    router,
    store,
    render: h => h(App)
}).$mount('#app');
