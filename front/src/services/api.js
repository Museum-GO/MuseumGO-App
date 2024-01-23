import axios from "axios";

const apiClient = axios.create({
  baseURL: "/",
  headers: {
    "Content-Type": "application/json",
  },
});

export default {
  getWorks() {
    return apiClient
      .get("/works")
      .then((response) => {
        return response.data;
      })
      .catch((error) => {
        console.log(error);
      });
  },
  
  getNumberWorks() {
    return apiClient
      .get("/works_num")
      .then((response) => {
        return response.data;
      })
      .catch((error) => {
        console.log(error);
      });
  }
  // ... other API methods
};
