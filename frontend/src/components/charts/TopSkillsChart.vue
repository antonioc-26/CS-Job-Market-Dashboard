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

const props = withDefaults(
  defineProps<{
    rows: SkillRow[]
    title?: string
  }>(),
  {
    // Provide a default title so the component can be reused without requiring it.
    title: 'Top In-Demand Skills',
  },
)

// Fixed color palette reused across bars; cycles if there are more skills than colors.
const chartColors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#6366f1']

// Transform incoming rows into Chart.js dataset format.
// Color assignment cycles to avoid index overflow.
const chartData = computed(() => ({
  labels: props.rows.map((row) => row.skill),
  datasets: [
    {
      label: 'Job Count',
      data: props.rows.map((row) => row.count),
      backgroundColor: props.rows.map((_, i) => chartColors[i % chartColors.length]),
      borderWidth: 1,
      // Rounded bars improve visual polish without affecting data meaning.
      borderRadius: 6,
      // Control bar density for better spacing and readability.
      barPercentage: 0.7,
      categoryPercentage: 0.7,
    },
  ],
}))

// Reactive chart configuration allows future dynamic behavior (e.g., theming, toggles).
const chartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      // Legend is hidden since only one dataset is shown.
      display: false,
    },
    title: {
      display: true,
      text: props.title,
      color: '#111827',
      font: {
        size: 16,
      },
    },
  },
  scales: {
    x: {
      ticks: {
        color: '#374151',
      },
      // Subtle grid lines for readability without visual clutter.
      grid: {
        color: '#e5e7eb',
      },
      border: {
        color: '#6b7280',
      },
    },
    y: {
      ticks: {
        color: '#374151',
      },
      grid: {
        color: '#d1d5db',
      },
      border: {
        color: '#6b7280',
      },
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