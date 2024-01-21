import { createRouter, createWebHistory } from "vue-router";

const routes = [
  {
    path: "/",
    component: () => import("../layouts/MainLayout.vue"),
    children: [
      {
        name: "Home",
        path: "",
        component: () => import("../views/HomeView.vue"),
      },
      {
        name: "about",
        path: "/about",
        component: () => import("../views/AboutView.vue"),
      }, {
        name: "artwork",
        path: "/artwork",
        component: () => import("../views/ArtworkView.vue"),
      }
    ],
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
