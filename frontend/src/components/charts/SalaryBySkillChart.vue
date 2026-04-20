<!--
File: SalaryBySkillChart.vue
Purpose: Render a bar chart showing the average salary associated with top skills.

Responsibilities:
- Register required Chart.js modules for bar chart rendering
- Transform salary-by-skill data into chart-compatible format
- Configure chart options, including currency formatting for the Y-axis
- Support a dynamic chart title so the view can reflect state-based filtering

Notes:
- This component assumes salary values are already aggregated (average) upstream.
- Currency formatting is applied at the chart axis and tooltip level for readability.
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

// Register only the necessary Chart.js components required by this chart.
ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

type SalaryRow = {
  skills: string
  avg_salary: number
}

const props = withDefaults(
  defineProps<{
    rows: SalaryRow[]
    title?: string
  }>(),
  {
    // Provide a reusable default title when a parent does not override it.
    title: 'Average Salary by Skill',
  },
)

// Reuse a fixed palette across bars; colors cycle when there are more rows than entries.
const chartColors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#6366f1']

// Convert incoming data into the structure required by vue-chartjs.
const chartData = computed(() => ({
  labels: props.rows.map((row) => row.skills),
  datasets: [
    {
      label: 'Average Salary',
      data: props.rows.map((row) => row.avg_salary),
      backgroundColor: props.rows.map((_, i) => chartColors[i % chartColors.length]),
      borderWidth: 1,
      // Rounded bars improve readability without changing the underlying data.
      borderRadius: 6,
      // Slightly reduce bar and category width to keep dense charts visually balanced.
      barPercentage: 0.7,
      categoryPercentage: 0.7,
    },
  ],
}))

// Keep chart configuration reactive so the title and formatting can respond
// cleanly if props or future view state change.
const chartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      // Hide the legend because the chart displays only a single dataset.
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
    tooltip: {
      callbacks: {
        // Format hovered values as currency for easier interpretation.
        label: (context: { parsed: { y: number } }) =>
          `Average Salary: $${context.parsed.y.toLocaleString()}`,
      },
    },
  },
  scales: {
    x: {
      ticks: {
        color: '#374151',
      },
      // Use subtle grid lines so the chart remains readable without feeling noisy.
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
        // Format Y-axis labels as whole-dollar currency values.
        callback: function (value: string | number) {
          return `$${Number(value).toLocaleString()}`
        },
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
      <!-- Render the bar chart using reactive data and configuration. -->
      <Bar :data="chartData" :options="chartOptions" />
    </div>
  </section>
</template>

<style scoped>
/* Container for the chart to match dashboard card styling. */
.chart-card {
  border: 1px solid #ddd;
  border-radius: 16px;
  padding: 1rem;
  background: #fff;
}

/* Fixed height ensures consistent chart rendering across layouts. */
.chart-wrapper {
  height: 360px;
}
</style>