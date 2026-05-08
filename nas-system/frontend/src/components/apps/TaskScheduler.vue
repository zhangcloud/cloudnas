<template>
  <div>
    <h1>任务调度</h1>
    <div style="margin-bottom: 1rem; display: flex; gap: 1rem; flex-wrap: wrap; align-items: center;">
      <input v-model="name" placeholder="任务名称" />
      <input v-model="type" placeholder="任务类型" />
      <input v-model="schedule" placeholder="Cron 表达式" />
      <button @click="createTask">创建任务</button>
    </div>
    <table style="width: 100%; border-collapse: collapse;">
      <thead>
        <tr>
          <th>名称</th>
          <th>类型</th>
          <th>计划</th>
          <th>状态</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="task in tasks" :key="task.id">
          <td>{{ task.name }}</td>
          <td>{{ task.type }}</td>
          <td>{{ task.schedule }}</td>
          <td>{{ task.status }}</td>
          <td>
            <button @click="toggleTask(task)">
              {{ task.status === 'enabled' ? '禁用' : '启用' }}
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { fetchTasks, createTask, toggleTask } from '../../api'

const tasks = ref<any[]>([])
const name = ref('')
const type = ref('backup')
const schedule = ref('0 2 * * *')

async function loadTasks() {
  try {
    const response = await fetchTasks()
    tasks.value = response.data.tasks
  } catch (error) {
    console.error(error)
  }
}

async function createTaskHandler() {
  if (!name.value || !type.value || !schedule.value) return
  try {
    await createTask(name.value, type.value, schedule.value)
    name.value = ''
    type.value = 'backup'
    schedule.value = '0 2 * * *'
    loadTasks()
  } catch (error) {
    console.error(error)
  }
}

async function toggleTaskHandler(task: any) {
  try {
    await toggleTask(task.id, task.status !== 'enabled')
    loadTasks()
  } catch (error) {
    console.error(error)
  }
}

onMounted(loadTasks)
</script>
