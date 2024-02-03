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
        name: "Map",
        path: "/map",
        component: () => import("../views/mapView/MapView.vue"),
      },
      {
        name: "about",
        path: "/about",
        component: () => import("../views/AboutView.vue"),
      },
      {
        name: "artwork",
        path: "/artwork/:id_artwork",
        component: () => import("../views/ArtworkView.vue"),
      },
      {
        name: "artwork_list",
        path: "/artwork",
        component: () => import("../views/Artwork_list.vue"),
      },
      {
        name: "null",
        path: "/:pathMatch(.*)*",
        component: () => import("../views/nullView.vue"),
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
