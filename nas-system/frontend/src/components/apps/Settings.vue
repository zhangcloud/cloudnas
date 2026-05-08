<template>
  <div>
    <h1>控制面板</h1>
    <div class="dsm-grid">
      <div class="dsm-widget">
        <h3>系统状态</h3>
        <pre>{{ systemInfo }}</pre>
      </div>
      <div class="dsm-widget">
        <h3>存储状态</h3>
        <p>存储池数量: {{ storageStatus.pool_count }}</p>
        <p>健康状态: <span :class="'status-' + storageStatus.health">{{ storageStatus.health }}</span></p>
      </div>
      <div class="dsm-widget">
        <h3>网络状态</h3>
        <p>IP: {{ networkStatus.ip_address }}</p>
        <p>主机名: {{ networkStatus.hostname }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { fetchSystemStatus, fetchVolumes, fetchNetworkStatus } from '../../api'

const systemInfo = ref('加载中...')
const storageStatus = ref({ pool_count: 0, health: 'unknown' })
const networkStatus = ref({ ip_address: '', hostname: '' })

async function loadStatus() {
  try {
    const sysResponse = await fetchSystemStatus()
    systemInfo.value = JSON.stringify(sysResponse.data, null, 2)

    const storageResponse = await fetchVolumes()
    storageStatus.value = {
      pool_count: storageResponse.data.volumes.length,
      health: storageResponse.data.volumes.every((v: any) => v.status === 'online') ? 'good' : 'degraded'
    }

    const networkResponse = await fetchNetworkStatus()
    networkStatus.value = networkResponse.data
  } catch (error) {
    console.error(error)
    systemInfo.value = '获取失败'
  }
}

onMounted(loadStatus)
</script>
