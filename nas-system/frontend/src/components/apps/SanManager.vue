<template>
  <div>
    <h1>SAN 存储管理</h1>

    <div class="dsm-grid">
      <div class="dsm-widget">
        <h3>SAN 状态</h3>
        <p>iSCSI: <span :class="sanStatus.iscsi.enabled ? 'status-online' : 'status-offline'">
          {{ sanStatus.iscsi.enabled ? '启用' : '禁用' }}
        </span> ({{ sanStatus.iscsi.targets_count }} 个目标)</p>
        <p>FC: <span :class="sanStatus.fc.enabled ? 'status-online' : 'status-offline'">
          {{ sanStatus.fc.enabled ? '启用' : '禁用' }}
        </span> ({{ sanStatus.fc.targets_count }} 个目标)</p>
        <p>整体健康: <span :class="'status-' + sanStatus.overall_health">{{ sanStatus.overall_health }}</span></p>
      </div>
    </div>

    <div class="dsm-grid">
      <!-- iSCSI 管理 -->
      <div class="dsm-widget">
        <h3>iSCSI 目标</h3>
        <div style="margin-bottom: 1rem; display: flex; gap: 1rem; flex-wrap: wrap; align-items: center;">
          <input v-model="newIscsiName" placeholder="目标名称" />
          <input v-model="newIscsiLun" placeholder="LUN 路径" />
          <button @click="createIscsiTarget">创建 iSCSI 目标</button>
        </div>
        <table style="width: 100%; border-collapse: collapse;">
          <thead>
            <tr>
              <th>名称</th>
              <th>IQN</th>
              <th>状态</th>
              <th>客户端</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="target in iscsiTargets" :key="target.id">
              <td>{{ target.name }}</td>
              <td>{{ target.id }}</td>
              <td>{{ target.status }}</td>
              <td>{{ target.clients.length }}</td>
              <td>
                <button @click="addIscsiClient(target.id)">添加客户端</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- FC 管理 -->
      <div class="dsm-widget">
        <h3>FC 目标</h3>
        <div style="margin-bottom: 1rem; display: flex; gap: 1rem; flex-wrap: wrap; align-items: center;">
          <input v-model="newFcName" placeholder="目标名称" />
          <input v-model="newFcWwn" placeholder="WWN" />
          <button @click="createFcTarget">创建 FC 目标</button>
        </div>
        <table style="width: 100%; border-collapse: collapse;">
          <thead>
            <tr>
              <th>名称</th>
              <th>WWN</th>
              <th>状态</th>
              <th>端口</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="target in fcTargets" :key="target.id">
              <td>{{ target.name || target.id }}</td>
              <td>{{ target.wwn }}</td>
              <td>{{ target.status }}</td>
              <td>{{ target.ports.join(', ') }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { fetchIscsiTargets, createIscsiTarget, addIscsiClient, fetchFcTargets, createFcTarget, fetchSanStatus } from '../../api'

const iscsiTargets = ref<any[]>([])
const fcTargets = ref<any[]>([])
const sanStatus = ref({ iscsi: { enabled: false, targets_count: 0 }, fc: { enabled: false, targets_count: 0 }, overall_health: 'unknown' })

const newIscsiName = ref('')
const newIscsiLun = ref('')
const newFcName = ref('')
const newFcWwn = ref('')

async function loadSanData() {
  try {
    const [iscsiResponse, fcResponse, statusResponse] = await Promise.all([
      fetchIscsiTargets(),
      fetchFcTargets(),
      fetchSanStatus()
    ])
    iscsiTargets.value = iscsiResponse.data.targets
    fcTargets.value = fcResponse.data.targets
    sanStatus.value = statusResponse.data
  } catch (error) {
    console.error(error)
  }
}

async function createIscsiTargetHandler() {
  if (!newIscsiName.value || !newIscsiLun.value) return
  try {
    await createIscsiTarget(newIscsiName.value, newIscsiLun.value)
    newIscsiName.value = ''
    newIscsiLun.value = ''
    loadSanData()
  } catch (error) {
    console.error(error)
  }
}

async function addIscsiClientHandler(targetId: string) {
  const clientIqn = prompt('请输入客户端 IQN')
  if (!clientIqn) return
  try {
    await addIscsiClient(targetId, clientIqn)
    loadSanData()
  } catch (error) {
    console.error(error)
  }
}

async function createFcTargetHandler() {
  if (!newFcName.value || !newFcWwn.value) return
  try {
    await createFcTarget(newFcName.value, newFcWwn.value)
    newFcName.value = ''
    newFcWwn.value = ''
    loadSanData()
  } catch (error) {
    console.error(error)
  }
}

onMounted(loadSanData)
</script>