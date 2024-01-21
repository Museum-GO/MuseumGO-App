<template>
  <div id="map-view">
    <div id="map-container">
      <l-map
        ref="map"
        :zoom="zoom"
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
        <button id="focusOnUserLocationBtn" @click="focusOnUserLocation">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            fill="black"
            viewBox="0 0 26 26"
          >
            <path
              fill-rule="evenodd"
              d="M 11 1 L 11 3.03125 C 6.7956596 3.4828018 3.4828018 6.7956596 3.03125 11 L 1 11 L 1 13 L 3.03125 13 C 3.4828018 17.20434 6.7956596 20.517198 11 20.96875 L 11 23 L 13 23 L 13 20.96875 C 17.20434 20.517198 20.517198 17.20434 20.96875 13 L 23 13 L 23 11 L 20.96875 11 C 20.517198 6.7956596 17.20434 3.4828018 13 3.03125 L 13 1 L 11 1 z M 12 5 C 15.9 5 19 8.1 19 12 C 19 15.9 15.9 19 12 19 C 8.1 19 5 15.9 5 12 C 5 8.1 8.1 5 12 5 z M 12 8 C 9.790861 8 8 9.790861 8 12 C 8 14.209139 9.790861 16 12 16 C 14.209139 16 16 14.209139 16 12 C 16 9.790861 14.209139 8 12 8 z"
            />
          </svg>
        </button>

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
            :lat-lng="museum.location.coordinates"
            @click="console.log(museum)"
          >
            <!-- Artwork -->
            <l-icon
              v-if="museum.artworks.length == 1"
              icon-url="https://news.artnet.com/app/news-upload/2017/03/Mona_Lisa_by_Leonardo_da_Vinci_from_C2RMF_retouched-256x256.jpg"
              class-name="marker artwork growOnHover"
            >
            </l-icon>

            <!-- Museum -->
            <l-icon v-else icon-url="images/Museum.png">
              <div class="museum">
                <div class="banner">Louvre LouvreLouvre</div>
                <img src="images/Museum.png" alt="" class="marker" />
                <div class="artworkNumber">
                  {{ museum.artworks.length }}
                </div>
              </div>
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

import api from "@/services/api";

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
      baseZoom: 15,
      zoom: this.baseZoom,
      iconWidth: 100,
      iconHeight: 100,

      // Map content data
      museums: null,

      defaultLocation: [48.860611, 2.337644],
      defaultSearchRect: [
        [48.730067935507265, 2.215762198023139],
        [48.69872201673064, 2.277517378382026],
      ],
      currentLocation: null,

      // Map options
      geojson: null,
      geoStyler: (feature) => {
        return {
          fillColor: "red",
          fillOpacity: feature.properties.code / 100000,
        };
      },

      cameraCoordinates: null,
      rangeSearchTarget: 1000,
    };
  },
  mounted() {},
  computed: {},
  methods: {
    // Artworks and museums
    loadMuseums(bottomLeftCoordinatesIn, topRightCoordinatesIn) {
      // Load artworks from the server that are in the given rectangle
      const bottomLeftCoordinates =
        [bottomLeftCoordinatesIn.lat, bottomLeftCoordinatesIn.lng] ||
        this.defaultSearchRect[0];
      const topRightCoordinates =
        [topRightCoordinatesIn.lat, topRightCoordinatesIn.lng] ||
        this.defaultSearchRect[1];

      // Request artworks from the server
      console.log("send");
      api
        .getWorksInRect(bottomLeftCoordinates, topRightCoordinates)
        .then((artworks) => {
          console.log("receive");
          // Group artworks by museums
          this.museums = constructMuseumsFromArtworks(artworks);
        });
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
            this.currentLocation = latLng(
              position.coords.latitude,
              position.coords.longitude
            );
            this.focusOnUserLocation();
            // this.loadMuseums(
            //   [position.coords.latitude, position.coords.longitude],
            //   this.getRangeFromZoom(this.zoom)
            // );
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
      if (!this.currentLocation || !this.getMap()) return;
      this.$refs.userLocation?.setLatLng(this.currentLocation);
    },
    focusOnUserLocation() {
      if (!this.currentLocation || !this.getMap()) return;
      this.getMap().setView(this.currentLocation, this.baseZoom);
    },

    // Camera location
    watchCameraLocation() {
      if (!this.getMap()) return;

      this.getMap().on("move", this.cameraLocationUpdated);

      this.getMap().on("zoomend", this.cameraLocationUpdated);
    },

    cameraLocationUpdated() {
      const mapBounds = this.getMap().getBounds();
      const bottomLeft = mapBounds.getSouthWest(); // Bottom-left coordinates
      const topRight = mapBounds.getNorthEast(); // Top-right coordinates

      this.loadMuseums(bottomLeft, topRight);
    },

    // Search parameters
    getRangeFromZoom(zoomLevel) {
      // Compute the range in meters from the zoom level
      // const m = -38423.08;
      // const b = 692115.38;
      return (20 - zoomLevel) ** 3 * 1000;
    },
  },
  watch: {
    currentLocation() {
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
  --marker-size: 50px;
  --marker-size-half: calc(var(--marker-size) / -2);
  --marker-hover-size: 55px;
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
}

.growOnHover {
  transition: all 0.1s ease-in-out;

  &:hover {
    // Scale up the image
    width: var(--marker-hover-size) !important;
    height: var(--marker-hover-size) !important;
    margin-left: var(--marker-hover-size-half) !important;
    margin-top: var(--marker-hover-size-half) !important;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
    z-index: 1000 !important;
  }
}

.artwork {
}

.museum {
  img {
    position: absolute;
    border-color: black;
    width: 100%;
    height: 100%;
    object-fit: cover;
    z-index: 1000;
  }

  .artworkNumber {
    display: flex;
    justify-content: center;
    min-width: calc(var(--marker-size) / 3);
    height: calc(var(--marker-size) / 3);
    position: absolute;
    bottom: calc(var(--marker-size) / 3);
    right: calc(var(--marker-size) / -3);
    padding: 2px;
    border-radius: 50px;
    z-index: 1000;

    font-weight: bold;
    color: white;
    background-color: red;

    transition: all 0.1s ease-in-out;
  }

  .banner {
    position: absolute;
    // min-width: calc(var(--marker-size) * 2);
    top: calc(var(--marker-size) / -2);
    padding-top: calc(var(--marker-size) / 5);
    padding-bottom: calc(var(--marker-size) / 5);
    padding-left: calc(var(--marker-size) / 3);
    padding-right: calc(var(--marker-size) / 8);

    margin-top: calc(var(--marker-size) / 6.7);
    margin-bottom: calc(var(--marker-size) / 6.7);
    margin-right: 0;
    margin-left: calc(var(--marker-size) * 0.32);

    border-top-right-radius: calc(var(--marker-size) / 10);
    border-bottom-right-radius: calc(var(--marker-size) / 10);
    z-index: 100;

    color: white;
    background-color: var(--primary-color);
    // Force the text to be on one line
    white-space: nowrap;
  }

  &:hover {
    img {
      width: var(--marker-hover-size) !important;
      height: var(--marker-hover-size) !important;
      margin-left: var(--marker-hover-size-half) !important;
      margin-top: var(--marker-hover-size-half) !important;
      box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
      z-index: 1000 !important;
    }

    .artworkNumber {
      bottom: calc(var(--marker-hover-size) / 3);
      right: calc(var(--marker-hover-size) / -3);
    }

    .banner {
    }
  }
}

.userLocation {
  height: 60px !important;
  margin-left: -10px !important;
  margin-top: -60px !important;
  filter: drop-shadow(0 0 5px rgba(0, 0, 0, 0.2));
}

#focusOnUserLocationBtn {
  position: absolute;
  display: flex;
  justify-content: center;
  align-items: center;
  width: 31px;
  height: 31px;
  bottom: 100px;
  right: 12px;
  z-index: 1000;
  margin: 0;
  border-radius: 3px;
  background-color: white;
  box-shadow: 0 0 3px rgba(0, 0, 0, 1);
}
</style>
