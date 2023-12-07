import { createRouter, createWebHashHistory } from "vue-router";
import Home from "@/pages/Home.vue";
import Banner from "@/pages/Banner.vue";
import Comment from "@/pages/Comment.vue";
import Post from "@/pages/Post.vue";
import User from "@/pages/User";


const routes = [{
    path: "/", component: Home, name: "home"
}, { path: "/banner", component: Banner, name: "banner" },
{ path: "/comment", component: Comment, name: "comment" },
{ path: "/post", component: Post, name: "post" },
{ path: "/user", component: User, name: "user" }
];


const router = createRouter({
    // 4. 内部提供了 history 模式的实现。为了简单起见，我们在这里使用 hash 模式。
    history: createWebHashHistory(),
    routes, // `routes: routes` 的缩写
});


export default router;