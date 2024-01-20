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
            v-for="(museum, i) in museums"
            :key="i"
            :lat-lng="museum.geometry.coordinates"
            @click="console.log(museum)"
          >
            <!-- Artwork -->
            <l-icon
              v-if="museum.artworks.length == 1"
              icon-url="https://news.artnet.com/app/news-upload/2017/03/Mona_Lisa_by_Leonardo_da_Vinci_from_C2RMF_retouched-256x256.jpg"
              class-name="marker artwork"
            >
            </l-icon>

            <!-- Museum -->
            <l-icon
              v-else
              icon-url="images/Museum.png"
              class-name="marker museum"
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
  LControlZoom,
} from "@vue-leaflet/vue-leaflet";

import { latLng } from "leaflet";

import { constructMuseumsFromArtworks } from "./mapUtils";

export default {
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LIcon,
    LFeatureGroup,
    LControlZoom,
  },
  data() {
    return {
      // Map properties
      zoom: 15,
      iconWidth: 100,
      iconHeight: 100,

      // Map content data
      museums: null,

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
    // Artworks and museums
    loadMuseums(targetCoordinatesIn) {
      // Load artworks from the server that are around the target coordinates
      const targetCoordinates = targetCoordinatesIn || this.defaultLocation;

      console.log("Loading artworks around ", targetCoordinates);

      // TMP fake data, TODO remove
      const artworks = [
        {
          type: "Feature",
          geometry: {
            type: "Point",
            coordinates: [48.860611, 2.337644], // Louvre
          },
          properties: {},
        },
        {
          type: "Feature",
          geometry: {
            type: "Point",
            coordinates: [48.8526049229, 2.33466199468], // Eugene Delacroix
          },
          properties: {},
        },
      ];

      for (let i = 0; i < 10; i++) {
        artworks.push({
          type: "Feature",
          geometry: {
            type: "Point",
            coordinates: [
              targetCoordinates[0] + (Math.random() - 0.5) * 0.25,
              targetCoordinates[1] + (Math.random() - 0.5) * 0.25,
            ],
          },
        });
      }

      // Add few more artworks that have the same coordinates as some other artworks
      const nbMuseums = 5;

      for (let i = 0; i < nbMuseums; i++) {
        const randomIndex = Math.floor(Math.random() * artworks.length);
        const randomFeature = artworks[randomIndex];
        artworks.push({
          type: "Feature",
          geometry: {
            type: "Point",
            coordinates: randomFeature.geometry.coordinates,
          },
        });
      }

      // Group artworks by museums
      const museums = constructMuseumsFromArtworks(artworks);

      this.museums = museums;
    },

    // Map
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
            console.log("User location: ", position.coords);
            this.currentLocation = latLng(
              position.coords.latitude,
              position.coords.longitude
            );
            this.focusOnUserLocation();
            this.loadMuseums([
              position.coords.latitude,
              position.coords.longitude,
            ]);

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

      this.getMap().on("move", () => {
        // const artworkSearchTarget = event.target.getCenter();
        // console.log("Camera position ", artworkSearchTarget);
        // TODO, get the artworks around the camera position
        // this.loadMuseums([artworkSearchTarget.lat, artworkSearchTarget.lng]);
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
  --marker-size: 30px;
  --marker-size-half: calc(var(--marker-size) / -2);
  --marker-hover-size: 40px;
  --marker-hover-size-half: calc(var(--marker-hover-size) / -2);
  --marker-border-size: 2px;
}

.marker {
  width: var(--marker-size) !important;
  height: var(--marker-size) !important;
  margin-left: var(--marker-size-half) !important;
  margin-top: var(--marker-size-half) !important;

  border-radius: 50%;
  border: var(--marker-border-size) solid white;
  background-color: white;
  transition: all 0.1s ease-in-out;

  box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);

  // Prevent the image to warp when the icon size changes
  object-fit: cover;

  &:hover {
    // Scale up the image
    width: var(--marker-hover-size) !important;
    height: var(--marker-hover-size) !important;
    margin-left: var(--marker-hover-size-half) !important;
    margin-top: var(--marker-hover-size-half) !important;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
  }
}

.artwork {
}

.museum {
  border-color: black;

  &::after {
    content: "eee";
    position: absolute;
    width: 0;
    height: 0;
    border-top: 10px solid transparent;
    border-bottom: 10px solid transparent;
    border-left: 20px solid black;
    left: -20px;
    top: 50%;
    margin-top: -10px;
    background: red;
  }
}

.userLocation {
  height: 60px !important;
  margin-left: -10px !important;
  margin-top: -60px !important;
}
</style>