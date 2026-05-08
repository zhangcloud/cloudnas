<template>
  <div>
    <h1>网络管理</h1>
    <div class="card" style="margin-bottom: 1rem;">
      <h2>当前网络</h2>
      <p>IP: {{ network.ip_address }}</p>
      <p>子网掩码: {{ network.netmask }}</p>
      <p>网关: {{ network.gateway }}</p>
      <p>DNS: {{ network.dns.join(', ') }}</p>
      <p>服务: {{ JSON.stringify(network.services) }}</p>
    </div>
    <button @click="toggleService('FTP', network.services.FTP === 'running' ? 'stop' : 'start')">
      {{ network.services.FTP === 'running' ? '停止 FTP' : '启动 FTP' }}
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { fetchNetworkStatus, toggleNetworkService } from '../../api'

const network = ref<any>({ ip_address: '', netmask: '', gateway: '', dns: [], services: {} })

async function loadNetwork() {
  try {
    const response = await fetchNetworkStatus()
    network.value = response.data
  } catch (error) {
    console.error(error)
  }
}

async function toggleService(service: string, action: string) {
  try {
    await toggleNetworkService(service, action)
    loadNetwork()
  } catch (error) {
    console.error(error)
  }
}

onMounted(loadNetwork)
</script>
