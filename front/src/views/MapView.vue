<template>
  <div id="map-view">
    <div id="map-container">
      <l-map ref="map" v-model:zoom="zoom" :center="[47.41322, -1.219482]">
        <l-tile-layer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <l-marker :lat-lng="[47.41322, -1.219482]">
          <l-icon
            :icon-url="iconUrl"
            :icon-size="iconSize"
            class-name="random-marker"
          />
        </l-marker>

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
              icon-url="https://t1.gstatic.com/licensed-image?q=tbn:ANd9GcQ-FvbbAq5IaJUhtwxXEwY0D-jiZju02ejnNHx_bQWL_27GF3srhwJgqusMAqKh3QqU"
              :icon-size="[31, 31]"
              :icon-anchor="[15, 15]"
              class-name="random-marker"
            >
            </l-icon>
            <br>
            <b>
              {{ feature.properties.code }}
            </b>
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
    for (let i = 0; i < 1000; i++) {
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
  computed: {
    iconUrl() {
      return `https://placekitten.com/${this.iconWidth}/${this.iconHeight}`;
    },
    iconSize() {
      return [this.iconWidth, this.iconHeight];
    },
  },
  methods: {
    changeIcon() {
      this.iconWidth += 1;
      if (this.iconWidth > this.iconHeight) {
        this.iconWidth = Math.floor(this.iconHeight / 2);
      }
    },
    // async loadGeoJson() {
    //   const response = await fetch(
    //     "https://rawgit.com/gregoiredavid/france-geojson/master/regions/pays-de-la-loire/communes-pays-de-la-loire.geojson"
    //   );
    //   this.geojson = await response.json();
    // },
  },
};
</script>

<style lang="scss" scoped>
#map-view {
  #map-container {
    height: 94vh;
    width: 100vw;
  }
  button {
    position: absolute;
    top: 10px;
    left: 10px;
    z-index: 1000;
  }
}
</style>

<style lang="scss">
.random-marker {
  border-radius: 50%;
  border: 3px solid black;
  background-color: white;
  transition: transform 0.2s ease-in-out;
}
.random-marker:hover {
  transform: scale(1.5);
  opacity: 0.5;
}
</style>
