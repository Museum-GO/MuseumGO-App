<template>
  <div>
    <AppHeader />
    <router-view />
  </div>
</template>

<script>
import AppHeader from "@/components/AppHeader.vue";

export default {
  name: "MainLayout",
  components: {
    AppHeader,
  },
};
</script>

<style>
/* Styles for the shared layout */
</style>
