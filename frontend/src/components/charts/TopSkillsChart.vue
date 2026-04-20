<!--
File: TopSkillsChart.vue
Purpose: Render a bar chart showing the most in-demand skills from the analyzed job dataset.

Responsibilities:
- Register the Chart.js modules required for bar chart rendering
- Transform incoming skill rows into the data shape expected by vue-chartjs
- Configure chart presentation options for the dashboard view

Notes:
- This is a presentational component; data preparation beyond basic mapping is expected upstream.
- Chart.js registration is performed at module scope so the chart is ready when the component renders.
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

// Register only the chart features used by this component.
ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

type SkillRow = {
  skill: string
  count: number
}

const props = defineProps<{
  rows: SkillRow[]
}>()

// Map the incoming rows into the dataset format expected by vue-chartjs.
const chartData = computed(() => ({
  labels: props.rows.map((row) => row.skill),
  datasets: [
    {
      label: 'Job Count',
      data: props.rows.map((row) => row.count),
      borderWidth: 1,
    },
  ],
}))

// Keep chart configuration reactive so the component can respond cleanly
// if future option logic depends on incoming props or state.
const chartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: true,
    },
    title: {
      display: true,
      text: 'Top In-Demand Skills',
    },
  },
}))
</script>

<template>
  <section class="chart-card">
    <div class="chart-wrapper">
      <!-- Render the bar chart using the computed data and options objects. -->
      <Bar :data="chartData" :options="chartOptions" />
    </div>
  </section>
</template>

<style scoped>
/* Card container used to visually group the chart within the dashboard layout. */
.chart-card {
  border: 1px solid #ddd;
  border-radius: 16px;
  padding: 1rem;
  background: #fff;
}

/* Fixed height ensures the chart has enough vertical space to render clearly. */
.chart-wrapper {
  height: 360px;
}
</style>