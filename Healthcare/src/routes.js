import Vue from "vue";
import Router from "vue-router";

Vue.use(Router);

const router = new Router({
    mode: 'history',
    routes: [
        {
            path: "/",
            name: "Users",
            component: () => import("./components/RegisterPage"),
        },
        {
            path: "/users",
            name: "Users",
            component: () => import("./components/RegisterPage"),
        },
        {
            path: "/user/:id",
            name: "User",
            component: () => import("./components/RegisterPage"),
        },
        
    ]
});

export default router;
