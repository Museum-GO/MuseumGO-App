<template>
  <div class="about">
    <div class="container">
      <div class="square" v-for="(art, index) in artwork_list" :key="index">
        <ArtWorkCard
          :id="art.id"
          :title="art.name"
          :location="art.location.name"
          :image="art.image"
        />
      </div>
    </div>
  </div>
</template>

<script>
import ArtWorkCard from "@/components/ArtworkCard.vue";
import artworkData_list from "../assets/V0-list.json";

export default {
  name: "ArtWorks",
  components: {
    ArtWorkCard,
  },
  data() {
    return {
      artwork_list: artworkData_list,
    };
  },
};
</script>

<style lang="scss" scoped>
.about {
  padding: 20px;
}
.container {
  display: flex;
  overflow-x: auto;
}

.square {
  margin-right: 10px;
}
.square:last-child {
  margin-right: 0;
}
</style>
