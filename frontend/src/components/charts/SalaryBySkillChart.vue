<!--
File: SalaryBySkillChart.vue
Purpose: Render a bar chart showing the average salary associated with top skills.

Responsibilities:
- Register required Chart.js modules for bar chart rendering
- Transform salary-by-skill data into chart-compatible format
- Configure chart options, including currency formatting for the Y-axis

Notes:
- This component assumes salary values are already aggregated (average) upstream.
- Currency formatting is applied at the chart axis level for readability.
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

// Register only the necessary Chart.js components for this chart.
ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

type SalaryRow = {
  skills: string
  avg_salary: number
}

const props = defineProps<{
  rows: SalaryRow[]
}>()

// Convert incoming data into the structure required by vue-chartjs.
const chartData = computed(() => ({
  labels: props.rows.map((row) => row.skills),
  datasets: [
    {
      label: 'Average Salary',
      data: props.rows.map((row) => row.avg_salary),
      borderWidth: 1,
    },
  ],
}))

// Configure chart behavior and formatting.
// Includes custom Y-axis tick formatting to display currency values.
const chartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: true,
    },
    title: {
      display: true,
      text: 'Average Salary by Skill',
    },
  },
  scales: {
    y: {
      ticks: {
        // Format numeric values as USD currency for readability.
        callback: function (value: string | number) {
          return `$${value}`
        },
      },
    },
  },
}))
</script>

<template>
  <section class="chart-card">
    <div class="chart-wrapper">
      <!-- Render the bar chart using reactive data and configuration -->
      <Bar :data="chartData" :options="chartOptions" />
    </div>
  </section>
</template>

<style scoped>
/* Container for the chart to match dashboard card styling */
.chart-card {
  border: 1px solid #ddd;
  border-radius: 16px;
  padding: 1rem;
  background: #fff;
}

/* Fixed height ensures consistent chart rendering across layouts */
.chart-wrapper {
  height: 360px;
}
</style>