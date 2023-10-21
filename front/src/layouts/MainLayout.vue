<template>
  <div>
    <AppHeader />
    <router-view />
  </div>
</template>

<script>
import AppHeader from "@/components/AppHeader.vue";

export default {
  components: {
    AppHeader,
  },
  name: "MainLayout",
};
</script>

<style>
/* Styles for the shared layout */
</style>
