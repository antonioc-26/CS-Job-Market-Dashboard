<!--
File: SummaryCards.vue
Purpose: Display high-level summary metrics for the job market dashboard.

Responsibilities:
- Render key aggregate metrics (jobs analyzed, entry-level jobs, top skill)
- Provide a clean, consistent card-based layout for dashboard summaries
- Accept data via props for reuse across different datasets or views

Notes:
- This is a presentational component; all data is passed in from parent components.
- Assumes props are precomputed and validated upstream.
-->

<script setup lang="ts">
/**
 * Props defining the summary metrics displayed in the dashboard cards.
 * These values are expected to be computed by the parent (e.g., from analysis output).
 */
defineProps<{
  jobsAnalyzed: number
  entryLevelJobs: number
  topSkill: string
  topSkillCount: number
}>()
</script>

<template>
  <section class="cards">
    <!-- Total number of jobs processed in the dataset -->
    <article class="card">
      <h3>Jobs Analyzed</h3>
      <p>{{ jobsAnalyzed }}</p>
    </article>

    <!-- Count of jobs classified as entry-level -->
    <article class="card">
      <h3>Entry-Level Jobs</h3>
      <p>{{ entryLevelJobs }}</p>
    </article>

    <!-- Most frequently occurring skill and its count -->
    <article class="card">
      <h3>Top Skill</h3>
      <p>{{ topSkill }} ({{ topSkillCount }})</p>
    </article>
  </section>
</template>

<style scoped>
/* Grid layout for evenly spaced summary cards */
.cards {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1rem;
  margin: 2rem 0;
}

/* Individual card styling for metric display */
.card {
  border: 1px solid #ddd;
  border-radius: 16px;
  padding: 1.25rem;
  background: #fff;
}

/* Card title styling */
.card h3 {
  margin-bottom: 0.5rem;
  font-size: 1rem;
}

/* Emphasized metric value */
.card p {
  font-size: 1.5rem;
  font-weight: 700;
}
</style>