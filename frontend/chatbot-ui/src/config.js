// src/config.js
const BACKEND_URL =
  import.meta.env.MODE === 'development'
    ? 'http://localhost:5000'
    : 'https://all-about-pooja.onrender.com';

export default BACKEND_URL;
