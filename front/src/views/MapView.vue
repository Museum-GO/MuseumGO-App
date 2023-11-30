<template>
  <div id="map-view">
    <div id="map-container">
      <l-map ref="map" v-model:zoom="zoom" :center="[47.41322, -1.219482]">
        <!-- url="https://api.maptiler.com/maps/toner-v2/?key=zvSWykBhfXO9HxJ5ZX7j#{z}/{x}/{y}.png" -->
        <!-- url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" -->
        <!-- url="https://api.maptiler.com/maps/toner-v2/{z}/{x}/{y}.png?key=zvSWykBhfXO9HxJ5ZX7j" -->
        <l-tile-layer
          url="https://api.maptiler.com/maps/streets-v2/{z}/{x}/{y}.png?key=zvSWykBhfXO9HxJ5ZX7j"
        />

        <div style="position: absolute">
          {{ x }}
        </div>

        <l-marker :lat-lng="[47.61322, -0.519482]">
          <l-icon :icon-size="[21, 21]">★</l-icon>
        </l-marker>

        <l-marker :lat-lng="[47, -1]">
          <l-icon class-name="">Hello, Map!</l-icon>
        </l-marker>

        <l-feature-group>
          <l-marker
            v-for="(feature, i) in randomFeatures"
            :key="i"
            :lat-lng="feature.geometry.coordinates"
            @click="console.log(feature)"
          >
            <l-icon
              icon-url="https://news.artnet.com/app/news-upload/2017/03/Mona_Lisa_by_Leonardo_da_Vinci_from_C2RMF_retouched-256x256.jpg"
              class-name="random-marker"
            >
            </l-icon>
          </l-marker>
        </l-feature-group>
      </l-map>
    </div>
  </div>
</template>

<script>
import "leaflet/dist/leaflet.css";
import {
  LIcon,
  LMap,
  LMarker,
  LTileLayer,
  LFeatureGroup,
} from "@vue-leaflet/vue-leaflet";

export default {
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LIcon,
    LFeatureGroup,
  },
  data() {
    const randomFeatures = [];
    for (let i = 0; i < 10; i++) {
      randomFeatures.push({
        type: "Feature",
        geometry: {
          type: "Point",
          coordinates: [
            47.41322 + (Math.random() - 0.5) * 0.25,
            -1.219482 + (Math.random() - 0.5) * 0.25,
          ],
        },
        properties: {
          code: 44000 + Math.floor(Math.random() * 10000),
          name: "Nantes",
        },
      });
    }
    return {
      zoom: 15,
      iconWidth: 100,
      iconHeight: 100,
      randomFeatures: randomFeatures,
      currentLocation: {
        type: "Feature",
        geometry: {
          type: "Point",
          coordinates: [47.41322, -1.219482],
        },
        properties: {
          code: 44000,
          name: "Nantes",
        },
      },
      geojson: null,
      geoStyler: (feature) => {
        return {
          fillColor: "red",
          fillOpacity: feature.properties.code / 100000,
        };
      },
    };
  },
  computed: {},
  methods: {
    changeIcon() {
      this.iconWidth += 1;
      if (this.iconWidth > this.iconHeight) {
        this.iconWidth = Math.floor(this.iconHeight / 2);
      }
    },
  },
};
</script>

<style lang="scss" scoped>
#map-view {
  #map-container {
    height: 94vh;
    width: 100vw;
  }
}
</style>

<style lang="scss">
:root {
  --marker-size: 70px;
  --marker-size-half: calc(var(--marker-size) / -2);
  --marker-hover-size: 80px;
  --marker-hover-size-half: calc(var(--marker-hover-size) / -2);
}

.random-marker {
  width: var(--marker-size) !important;
  height: var(--marker-size) !important;
  margin-left: var(--marker-size-half) !important;
  margin-top: var(--marker-size-half) !important;

  border-radius: 50%;
  border: 3px solid white;
  background-color: white;
  transition: all 0.1s ease-in-out;

  box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);

  // Prevent the image to warp when the icon size changes
  object-fit: cover;
}
.random-marker:hover {
  // Scale up the image
  width: var(--marker-hover-size) !important;
  height: var(--marker-hover-size) !important;
  margin-left: var(--marker-hover-size-half) !important;
  margin-top: var(--marker-hover-size-half) !important;
  border: 4px solid white;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
}
</style>
