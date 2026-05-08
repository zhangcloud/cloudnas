<template>
  <div>
    <h1>快照管理</h1>
    <div style="margin-bottom: 1rem; display: flex; gap: 1rem; flex-wrap: wrap; align-items: center;">
      <input v-model="snapshotName" placeholder="快照名称" />
      <button @click="createSnapshot">创建快照</button>
    </div>
    <table style="width: 100%; border-collapse: collapse;">
      <thead>
        <tr>
          <th>名称</th>
          <th>创建时间</th>
          <th>状态</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="snap in snapshots" :key="snap.id">
          <td>{{ snap.name }}</td>
          <td>{{ snap.created_at }}</td>
          <td>{{ snap.status }}</td>
          <td><button @click="restoreSnapshot(snap.id)">恢复</button></td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { fetchSnapshots, createSnapshot, restoreSnapshot } from '../../api'

const snapshots = ref<any[]>([])
const snapshotName = ref('')

async function loadSnapshots() {
  try {
    const response = await fetchSnapshots()
    snapshots.value = response.data.snapshots
  } catch (error) {
    console.error(error)
  }
}

async function createSnapshotHandler() {
  if (!snapshotName.value) return
  try {
    await createSnapshot(snapshotName.value)
    snapshotName.value = ''
    loadSnapshots()
  } catch (error) {
    console.error(error)
  }
}

async function restoreSnapshotHandler(id: string) {
  if (!confirm('确认恢复此快照吗？')) return
  try {
    await restoreSnapshot(id)
    loadSnapshots()
  } catch (error) {
    console.error(error)
  }
}

onMounted(loadSnapshots)
</script>
