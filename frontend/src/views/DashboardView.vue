<!--
File: DashboardView.vue
Purpose: Define the main dashboard view for the CS Job Market project by loading
analysis outputs and rendering summary metrics, charts, and interactive filtering controls.

Responsibilities:
- Render the dashboard hero content and project description
- Load summary and chart data from generated analysis outputs
- Load cleaned job-level data for interactive filtering
- Transform CSV values into typed chart-friendly structures
- Compute filtered top-skill and salary-by-skill results based on the selected state
- Display summary metrics and data visualizations
- Scope layout and presentation styles to this view

Notes:
- This component fetches static analysis files from frontend/public/data.
- Data loading occurs when the view is mounted.
- Failures are logged to the console; no user-facing error state is currently shown.
-->

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import Papa, { type ParseResult } from 'papaparse'

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

type StateRow = {
  state: string
  count: string
}

type CleanedJobRow = {
  job_title: string
  company: string
  location: string
  state: string
  avg_salary: string
  skills: string
  experience_required: string
}

type SkillCountRow = {
  skill: string
  count: number
}

type SalarySkillRow = {
  skills: string
  avg_salary: number
}

// Reactive view state for summary metrics and chart datasets.
const summary = ref<Summary | null>(null)
const jobsByState = ref<{ state: string; count: number }[]>([])
const cleanedJobs = ref<CleanedJobRow[]>([])

// Default to the unfiltered dashboard view until the user selects a state.
const selectedState = ref('ALL')

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
      complete: (results: ParseResult<T>) => resolve(results.data),
      error: (error: Error) => reject(error),
    })
  })
}

// Build the state dropdown options from the cleaned dataset so the filter
// always reflects the actual available records.
const stateOptions = computed(() => {
  const states = cleanedJobs.value
    .map((row) => row.state?.trim())
    .filter((state): state is string => Boolean(state))
    // Guard against stringified missing values that may appear in CSV exports.
    .filter((state) => state !== 'nan')

  return ['ALL', ...new Set(states.sort())]
})

// Restrict the job set only when a concrete state has been selected.
const filteredJobs = computed(() => {
  if (selectedState.value === 'ALL') {
    return cleanedJobs.value
  }

  return cleanedJobs.value.filter((row) => row.state === selectedState.value)
})

// Recompute top skills from the filtered job-level dataset so the chart updates
// immediately when the state filter changes.
const filteredTopSkills = computed<SkillCountRow[]>(() => {
  const skillCounts = new Map<string, number>()

  for (const job of filteredJobs.value) {
    const skills = String(job.skills || '')
      .split(',')
      .map((skill) => skill.trim())
      .filter(Boolean)

    for (const skill of skills) {
      skillCounts.set(skill, (skillCounts.get(skill) ?? 0) + 1)
    }
  }

  return Array.from(skillCounts.entries())
    .map(([skill, count]) => ({ skill, count }))
    .sort((a, b) => b.count - a.count)
    .slice(0, 10)
})

// Recompute average salary by skill from the filtered job-level dataset so the
// salary chart stays aligned with the selected state.
const filteredSalaryBySkill = computed<SalarySkillRow[]>(() => {
  const salaryBuckets = new Map<string, number[]>()

  for (const job of filteredJobs.value) {
    const avgSalary = Number(job.avg_salary)

    // Skip records with missing or invalid salary values so averages remain meaningful.
    if (!Number.isFinite(avgSalary)) {
      continue
    }

    const skills = String(job.skills || '')
      .split(',')
      .map((skill) => skill.trim())
      .filter(Boolean)

    for (const skill of skills) {
      const existing = salaryBuckets.get(skill) ?? []
      existing.push(avgSalary)
      salaryBuckets.set(skill, existing)
    }
  }

  return Array.from(salaryBuckets.entries())
    .map(([skills, salaries]) => ({
      skills,
      avg_salary: salaries.reduce((sum, salary) => sum + salary, 0) / salaries.length,
    }))
    .sort((a, b) => b.avg_salary - a.avg_salary)
    .slice(0, 10)
})

// Update the chart titles to reflect whether the data is filtered globally
// or scoped to a specific state.
const topSkillsTitle = computed(() =>
  selectedState.value === 'ALL'
    ? 'Top In-Demand Skills'
    : `Top In-Demand Skills (${selectedState.value})`,
)

const salaryBySkillTitle = computed(() =>
  selectedState.value === 'ALL'
    ? 'Average Salary by Skill'
    : `Average Salary by Skill (${selectedState.value})`,
)

onMounted(async () => {
  try {
    // Load the summary first so the top-level metrics can render as soon as
    // the JSON payload is available.
    const summaryResponse = await fetch('/data/summary.json')
    summary.value = await summaryResponse.json()

    const stateRows = await loadCsv<StateRow>('/data/jobs_by_state.csv')
    jobsByState.value = stateRows.map((row) => ({
      state: row.state,
      count: Number(row.count),
    }))

    // Load the full cleaned job-level dataset used for interactive filtering.
    cleanedJobs.value = await loadCsv<CleanedJobRow>('/data/cleaned_jobs.csv')
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

    <section class="filters-card">
      <div class="filter-header">
        <h2>Filter Dashboard</h2>
        <p>Select a state to update skill demand and salary insights.</p>
      </div>

      <div class="filter-control">
        <label for="state-filter">State</label>
        <select id="state-filter" v-model="selectedState">
          <option v-for="state in stateOptions" :key="state" :value="state">
            {{ state === 'ALL' ? 'All States' : state }}
          </option>
        </select>
      </div>
    </section>

    <section class="charts-grid">
      <!-- Each chart renders only when its backing dataset has been loaded. -->
      <TopSkillsChart
        v-if="filteredTopSkills.length"
        :rows="filteredTopSkills"
        :title="topSkillsTitle"
      />
      <SalaryBySkillChart
        v-if="filteredSalaryBySkill.length"
        :rows="filteredSalaryBySkill"
        :title="salaryBySkillTitle"
      />
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

.filters-card {
  display: flex;
  justify-content: space-between;
  align-items: end;
  gap: 1.5rem;
  margin: 2rem 0;
  padding: 1.25rem;
  border: 1px solid #ddd;
  border-radius: 16px;
  background: #fff;
}

.filter-header h2 {
  margin: 0 0 0.35rem;
  font-size: 1.15rem;
}

.filter-header p {
  margin: 0;
  color: #4b5563;
}

.filter-control {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  min-width: 220px;
}

.filter-control label {
  font-weight: 600;
  color: #111827;
}

.filter-control select {
  padding: 0.75rem 0.9rem;
  border: 1px solid #cbd5e1;
  border-radius: 12px;
  background: #fff;
  color: #111827;
  font: inherit;
}

.charts-grid {
  /* Stack charts vertically with consistent spacing for the current layout. */
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
  margin-top: 2rem;
}

@media (max-width: 768px) {
  .filters-card {
    /* Collapse the filter layout vertically on smaller screens. */
    flex-direction: column;
    align-items: stretch;
  }

  .filter-control {
    min-width: 100%;
  }
}
</style>