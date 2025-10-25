// src/api.js
import axios from "axios";

// ✅ Base API URL (from environment variable)
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

// ✅ Create axios instance
export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// ✅ Attach Authorization header (JWT) automatically
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token"); // or sessionStorage
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// ✅ Handle 401 errors globally (optional auto-logout)
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      console.warn("Unauthorized — logging out...");
      localStorage.removeItem("token");
      window.location.href = "/login"; // optional redirect
    }
    return Promise.reject(error);
  }
);

// ✅ Generic helper functions

// Fetch odds list
export async function fetchOdds() {
  const res = await api.get("/odds");
  return res.data;
}

// Place a bet
export async function placeBet(bet) {
  const res = await api.post("/bets", bet);
  return res.data;
}

// Register user
export async function registerUser(data) {
  const res = await api.post("/auth/register", data);
  return res.data;
}

// Login user
export async function loginUser(credentials) {
  const res = await api.post("/auth/login", credentials);
  // ✅ Save token automatically
  if (res.data?.access_token) {
    localStorage.setItem("token", res.data.access_token);
  }
  return res.data;
}

// Fetch current user profile
export async function fetchProfile() {
  const res = await api.get("/users/me");
  return res.data;
}

// Logout (clear token)
export function logoutUser() {
  localStorage.removeItem("token");
}

