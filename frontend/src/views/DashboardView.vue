<!--
File: DashboardView.vue
Purpose: Define the top-level presentation for the CS Job Market Dashboard landing view.

Responsibilities:
- Render the dashboard hero content and project description
- Provide a placeholder section for future analytics visualizations and metrics
- Scope layout and presentation styles to this view

Notes:
- This component is currently presentational only and does not consume analysis data yet.
- Styles are scoped to avoid leaking layout rules into other views.
-->

<template>
  <main class="dashboard">
    <section class="hero">
      <p class="eyebrow">Data Analytics Project</p>
      <h1>CS Job Market Dashboard</h1>
      <p class="description">
        A dashboard that analyzes entry-level computer science job postings to identify
        in-demand skills, salary trends, and regional hiring patterns.
      </p>
    </section>

    <section class="placeholder-section">
      <h2>Dashboard Overview</h2>
      <p>
        Visualizations and summary metrics will appear here after the analysis outputs are connected.
      </p>
    </section>
  </main>
</template>

<style scoped>
/* Component-scoped styles */

.dashboard {
  max-width: 1100px;
  margin: 0 auto;
  padding: 2rem;
}

.hero {
  margin-bottom: 2rem;
}

.eyebrow {
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-bottom: 0.5rem;
}

h1 {
  font-size: 2.5rem;
  margin-bottom: 0.75rem;
}

.description {
  font-size: 1.05rem;
  line-height: 1.6;
  max-width: 760px;
}

.placeholder-section {
  border: 1px solid #ddd;
  border-radius: 16px;
  padding: 1.5rem;
  background: #fff;
}
</style>