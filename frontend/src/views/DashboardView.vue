<!--
File: DashboardView.vue
Purpose: Define the main dashboard view for the CS Job Market project by loading
analysis outputs and rendering summary metrics and charts.

Responsibilities:
- Render the dashboard hero content and project description
- Load summary and chart data from generated analysis outputs
- Transform CSV values into typed chart-friendly structures
- Display summary metrics and data visualizations
- Scope layout and presentation styles to this view

Notes:
- This component fetches static analysis files from frontend/public/data.
- Data loading occurs when the view is mounted.
- Failures are logged to the console; no user-facing error state is currently shown.
-->

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import Papa from 'papaparse'

import SummaryCards from '../components/SummaryCards.vue'
import TopSkillsChart from '../components/charts/TopSkillsChart.vue'
import SalaryBySkillChart from '../components/charts/SalaryBySkillChart.vue'
import JobsByStateChart from '../components/charts/JobsByStateChart.vue'

type Summary = {
  jobs_analyzed: number
  entry_level_jobs?: number
  top_skill: string
  top_skill_count: number
}

type TopSkillRow = {
  skill: string
  count: string
}

type SalaryRow = {
  skills: string
  avg_salary: string
}

type StateRow = {
  state: string
  count: string
}

// Reactive view state for summary metrics and chart datasets.
const summary = ref<Summary | null>(null)
const topSkills = ref<{ skill: string; count: number }[]>([])
const salaryBySkill = ref<{ skills: string; avg_salary: number }[]>([])
const jobsByState = ref<{ state: string; count: number }[]>([])

/**
 * Fetch and parse a CSV file into a typed array of row objects.
 *
 * The returned values preserve the raw CSV field types from Papa Parse,
 * so numeric conversions are handled explicitly by the caller.
 */
async function loadCsv<T>(path: string): Promise<T[]> {
  const response = await fetch(path)
  const csvText = await response.text()

  return new Promise((resolve, reject) => {
    Papa.parse<T>(csvText, {
      header: true,
      skipEmptyLines: true,
      complete: (results) => resolve(results.data),
      error: (error: Error) => reject(error),
    })
  })
}

onMounted(async () => {
  try {
    // Load the summary first so the top-level metrics can render as soon as
    // the JSON payload is available.
    const summaryResponse = await fetch('/data/summary.json')
    summary.value = await summaryResponse.json()

    // Convert CSV string values into numbers before passing them to chart components.
    const topSkillsRows = await loadCsv<TopSkillRow>('/data/top_skills.csv')
    topSkills.value = topSkillsRows.map((row) => ({
      skill: row.skill,
      count: Number(row.count),
    }))

    const salaryRows = await loadCsv<SalaryRow>('/data/salary_by_skill.csv')
    salaryBySkill.value = salaryRows.map((row) => ({
      skills: row.skills,
      avg_salary: Number(row.avg_salary),
    }))

    const stateRows = await loadCsv<StateRow>('/data/jobs_by_state.csv')
    jobsByState.value = stateRows.map((row) => ({
      state: row.state,
      count: Number(row.count),
    }))
  } catch (error) {
    // Keep the failure path visible during development and debugging.
    console.error('Failed to load dashboard data:', error)
  }
})
</script>

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

    <!-- Render summary metrics only after the JSON payload has been loaded. -->
    <SummaryCards
      v-if="summary"
      :jobs-analyzed="summary.jobs_analyzed"
      :entry-level-jobs="summary.entry_level_jobs ?? 0"
      :top-skill="summary.top_skill"
      :top-skill-count="summary.top_skill_count"
    />

    <section class="charts-grid">
      <!-- Each chart renders only when its backing dataset has been loaded. -->
      <TopSkillsChart v-if="topSkills.length" :rows="topSkills" />
      <SalaryBySkillChart v-if="salaryBySkill.length" :rows="salaryBySkill" />
      <JobsByStateChart v-if="jobsByState.length" :rows="jobsByState" />
    </section>
  </main>
</template>

<style scoped>
.dashboard {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.hero {
  /* Separate the page introduction from the metrics and charts below. */
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
  /* Constrain line length to keep the introductory text readable. */
  font-size: 1.05rem;
  line-height: 1.6;
  max-width: 760px;
}

.charts-grid {
  /* Stack charts vertically with consistent spacing for the current layout. */
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
  margin-top: 2rem;
}
</style>