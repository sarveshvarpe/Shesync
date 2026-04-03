import axios from "axios"

const api = axios.create({
  baseURL: "http://10.217.29.89:8000",
})

// Automatically attach token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token")
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export default api