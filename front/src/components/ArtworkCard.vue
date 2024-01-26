<template>
  <div class="container">
    <router-link :to="/artwork/ + id">
      <img class="image" :src="image" alt="IMAGE" />
      <div class="overlay">
        <h3 class="title">{{ title }}</h3>
        <p class="location">{{ location }}</p>
      </div>
    </router-link>
  </div>
</template>

<script>
export default {
  name: "ArtworkCard",
  props: {
    id: {
      type: Number,
      required: true,
    },
    title: {
      type: String,
      required: true,
    },
    location: {
      type: String,
      required: true,
    },
    image: {
      type: String,
      required: true,
    },
  },
};
</script>

<style lang="scss" scoped>
.container {
  width: 200px;
  height: 200px;
  position: relative;
  overflow: hidden;
}

.image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: rgba(0, 0, 0, 0.7);
  color: #fff;
  padding: 10px;
}

.title {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 5px;
}

.location {
  font-size: 14px;
}
</style>
