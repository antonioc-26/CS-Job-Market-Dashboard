<!--
File: JobsByStateChart.vue
Purpose: Render a bar chart showing the distribution of job postings by state.

Responsibilities:
- Register required Chart.js modules for rendering a bar chart
- Transform state-level job counts into chart-compatible data
- Configure chart options for display within the dashboard

Notes:
- This component expects pre-aggregated job counts by state.
- Designed for quick geographic distribution insights in the dashboard.
-->

<script setup lang="ts">
import { computed } from 'vue'
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
} from 'chart.js'

// Register only the required Chart.js modules for this visualization.
ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

type StateRow = {
  state: string
  count: number
}

const props = defineProps<{
  rows: StateRow[]
}>()

// Map incoming state data into the structure expected by vue-chartjs.
const chartData = computed(() => ({
  labels: props.rows.map((row) => row.state),
  datasets: [
    {
      label: 'Jobs',
      data: props.rows.map((row) => row.count),
      borderWidth: 1,
    },
  ],
}))

// Configure chart behavior and presentation.
const chartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: true,
    },
    title: {
      display: true,
      text: 'Job Counts by State',
    },
  },
}))
</script>

<template>
  <section class="chart-card">
    <div class="chart-wrapper">
      <!-- Render the bar chart using computed data and options -->
      <Bar :data="chartData" :options="chartOptions" />
    </div>
  </section>
</template>

<style scoped>
/* Card container to align with dashboard UI patterns */
.chart-card {
  border: 1px solid #ddd;
  border-radius: 16px;
  padding: 1rem;
  background: #fff;
}

/* Fixed height ensures consistent chart rendering */
.chart-wrapper {
  height: 360px;
}
</style>