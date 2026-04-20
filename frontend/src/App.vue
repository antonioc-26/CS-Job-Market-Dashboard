<!--
File: App.vue
Purpose: Root application component that serves as the entry point for the Vue app.

Responsibilities:
- Render the active route via <RouterView>
- Define global base styles and typography
- Establish consistent layout and visual foundation for the application

Notes:
- This component does not contain business logic; it primarily handles layout and styling.
- Global styles here apply across the entire app (not scoped).
-->

<template>
  <div id="app">
    <!-- RouterView renders the matched component for the current route -->
    <RouterView />
  </div>
</template>

<script setup lang="ts">
// No script logic is currently required.
// This component acts as a layout shell for routed views.
</script>

<style>
/* Global design system variables and base typography */
:root {
  color-scheme: light;

  /* System-first font stack for performance and consistency across platforms */
  font-family:
    Inter,
    ui-sans-serif,
    system-ui,
    -apple-system,
    BlinkMacSystemFont,
    "Segoe UI",
    sans-serif;

  line-height: 1.5;
  font-weight: 400;

  /* Default text and background colors */
  color: #1f2937;
  background-color: #f8fafc;

  /* Improve text rendering and font smoothing across browsers */
  font-synthesis: none;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* Apply consistent box model behavior across all elements */
* {
  box-sizing: border-box;
}

/* Ensure full-height layout and remove default browser margins */
html,
body,
#app {
  margin: 0;
  min-height: 100%;
}

/* Set global background and base text color */
body {
  background:
    radial-gradient(circle at top, #e0f2fe 0%, #f8fafc 35%, #f8fafc 100%);
  color: #111827;
}

/* Remove default link styling while preserving inherit color */
a {
  color: inherit;
  text-decoration: none;
}

/* Ensure form elements inherit font styles for consistency */
button,
input,
select,
textarea {
  font: inherit;
}
</style>