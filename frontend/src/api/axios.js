// axios.js
// PURPOSE: One shared Axios instance used by all pages.
//          Sets the base URL so we don't repeat it everywhere.
//          withCredentials: true → sends session cookies automatically.

import axios from "axios";

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || "http://127.0.0.1:5000",
  headers: { "Content-Type": "application/json" },
});

// Automatically attach token to every request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers["Authorization"] = `Bearer ${token}`;
  }
  return config;
});

export default api;