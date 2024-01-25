<template>
    <div class="container">
    <img class="image" src="../assets/test.jpeg" alt="Nom de l'oeuvre" >
    <div class="overlay">
        <h3 class="title">{{title}}</h3>
        <p class="location">{{location}}</p>
    </div>
    </div>
</template>

<script>
export default {
  name: "ArtworkCard",
  props: {
    id: {
      type: Number,
      required: true
    },
    title: {
      type: String, // Correction : le type doit être "String" avec une majuscule
      required: true
    },
    location: {
      type: String,
      required: true
    }
  }
}
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