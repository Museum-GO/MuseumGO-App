<template>
  <div id="map-view">
    <div id="map-container">
      <l-map
        ref="map"
        v-model:zoom="zoom"
        :center="defaultLocation"
        :options="{ zoomControl: false }"
        @ready="onReady"
      >
        <!-- Tiles -->
        <!-- url="https://api.maptiler.com/maps/toner-v2/?key=zvSWykBhfXO9HxJ5ZX7j#{z}/{x}/{y}.png" -->
        <!-- url="https://api.maptiler.com/maps/toner-v2/{z}/{x}/{y}.png?key=zvSWykBhfXO9HxJ5ZX7j" -->
        <!-- url="https://api.maptiler.com/maps/streets-v2/{z}/{x}/{y}.png?key=zvSWykBhfXO9HxJ5ZX7j" -->
        <!-- url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" -->
        <l-tile-layer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        <!-- Controls -->
        <l-control-zoom position="bottomright"></l-control-zoom>
        <button id="locateMe" @click="focusOnUserLocation">Locate me</button>

        <!-- User location: -->
        <l-marker
          v-if="currentLocation"
          :lat-lng="currentLocation"
          :radius="16"
          :fillOpacity="1"
          color="blue"
          fillColor="blue"
        >
          <l-icon icon-url="images/MonaLisa.png" class-name="userLocation">
          </l-icon>
        </l-marker>

        <!-- Artworks: -->
        <l-feature-group>
          <l-marker
            v-for="(feature, i) in randomFeatures"
            :key="i"
            :lat-lng="feature.geometry.coordinates"
            @click="console.log(feature)"
          >
            <l-icon
              icon-url="https://news.artnet.com/app/news-upload/2017/03/Mona_Lisa_by_Leonardo_da_Vinci_from_C2RMF_retouched-256x256.jpg"
              class-name="artwork"
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
  // LCircleMarker,
  LControlZoom,
} from "@vue-leaflet/vue-leaflet";

import { latLng } from "leaflet";

export default {
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LIcon,
    LFeatureGroup,
    // LCircleMarker,
    LControlZoom,
  },
  data() {
    const randomFeatures = [
      {
        type: "Feature",
        geometry: {
          type: "Point",
          coordinates: [48.860611, 2.337644],
        },
        properties: {},
      },
    ];

    for (let i = 0; i < 10; i++) {
      randomFeatures.push({
        type: "Feature",
        geometry: {
          type: "Point",
          coordinates: [
            48.860611 + (Math.random() - 0.5) * 0.25,
            2.337644 + (Math.random() - 0.5) * 0.25,
          ],
        },
      });
    }

    return {
      // Map properties
      zoom: 15,
      iconWidth: 100,
      iconHeight: 100,

      // Map data
      randomFeatures: randomFeatures,

      defaultLocation: [48.860611, 2.337644],
      currentLocation: null,

      // Map options
      geojson: null,
      geoStyler: (feature) => {
        return {
          fillColor: "red",
          fillOpacity: feature.properties.code / 100000,
        };
      },
    };
  },
  mounted() {
    // Watch user location
  },
  computed: {},
  methods: {
    onReady() {
      this.watchUserLocation();
      this.watchCameraLocation();
    },
    getMap() {
      return this.$refs.map?.leafletObject;
    },

    // User location
    watchUserLocation() {
      // TODO fix point not updating without zooming
      if (navigator.geolocation) {
        navigator.geolocation.watchPosition(
          (position) => {
            // Success callback, update the current location
            this.currentLocation = latLng(
              position.coords.latitude,
              position.coords.longitude
            );
            this.focusOnUserLocation();

            // setInterval(() => {
            // this.currentLocation.lat += (Math.random() - 0.5) * 0.001;
            // this.currentLocation.lng += (Math.random() - 0.5) * 0.001;
            // }, 1000);
          },
          () => {
            // Error callback
          },
          {
            // Options
            enableHighAccuracy: true,
            timeout: 5000,
            maximumAge: 0,
          }
        );
      } else {
        console.log("Geolocation is not supported by this browser.");
        this.currentLocation = this.defaultLocation;
      }
    },
    updateUserLocationMarker() {
      console.log("updateUserLocationMarker");
      if (!this.currentLocation || !this.getMap()) return;
      this.$refs.userLocation?.setLatLng(this.currentLocation);
    },
    focusOnUserLocation() {
      if (!this.currentLocation || !this.getMap()) return;
      this.getMap().panTo(this.currentLocation, this.zoom);
    },

    // Camera location
    watchCameraLocation() {
      if (!this.getMap()) return;

      this.getMap().on("move", (event) => {
        const artworkSearchTarget = event.target.getCenter();
        console.log("Camera position ", artworkSearchTarget);

        // TODO, get the artworks around the camera position
      });
    },
  },
  watch: {
    currentLocation() {
      console.log("currentLocation changed");
      this.updateUserLocationMarker();
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
  --artwork-marker-size: 50px;
  --artwork-marker-size-half: calc(var(--artwork-marker-size) / -2);
  --artwork-marker-hover-size: 60px;
  --artwork-marker-hover-size-half: calc(var(--artwork-marker-hover-size) / -2);
}

.artwork {
  width: var(--artwork-marker-size) !important;
  height: var(--artwork-marker-size) !important;
  margin-left: var(--artwork-marker-size-half) !important;
  margin-top: var(--artwork-marker-size-half) !important;

  border-radius: 50%;
  border: 3px solid white;
  background-color: white;
  transition: all 0.1s ease-in-out;

  box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);

  // Prevent the image to warp when the icon size changes
  object-fit: cover;
}
.artwork:hover {
  // Scale up the image
  width: var(--artwork-marker-hover-size) !important;
  height: var(--artwork-marker-hover-size) !important;
  margin-left: var(--artwork-marker-hover-size-half) !important;
  margin-top: var(--artwork-marker-hover-size-half) !important;
  border: 4px solid white;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
}

.userLocation {
  // width: 21px !important;
  height: 60px !important;
  margin-left: -10px !important;
  margin-top: -60px !important;
  // border-radius: 50%;
  // border: 3px solid white;
  // background-color: white;
  // transition: all 0.1s ease-in-out;
  // box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);
}
</style>
