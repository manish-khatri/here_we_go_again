<script>
export default {
  name: 'App'
}
</script>

<template>
  <div id="app">
    <router-view />
  </div>
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  line-height: 1.6;
  color: #333;
}

#app {
  min-height: 100vh;
}

/* Global button styles */
button {
  cursor: pointer;
  transition: all 0.3s ease;
}

button:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

/* Global input styles */
input, textarea, select {
  font-family: inherit;
  font-size: inherit;
}

/* Global link styles */
a {
  text-decoration: none;
  color: inherit;
}

/* Global table styles */
table {
  border-collapse: collapse;
  width: 100%;
}

/* Global modal styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
}

/* Responsive utilities */
@media (max-width: 768px) {
  .modal-content {
    padding: 1rem;
    width: 95%;
  }
}
</style>
