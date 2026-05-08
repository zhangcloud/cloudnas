<template>
  <div>
    <h1>应用中心</h1>
    <table style="width: 100%; border-collapse: collapse;">
      <thead>
        <tr>
          <th>名称</th>
          <th>版本</th>
          <th>状态</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="app in apps" :key="app.id">
          <td>{{ app.name }}</td>
          <td>{{ app.version }}</td>
          <td>{{ app.status }}</td>
          <td>
            <button v-if="app.status !== 'installed'" @click="installApp(app.id)">安装</button>
            <button v-if="app.status === 'installed'" @click="uninstallApp(app.id)">卸载</button>
            <button v-if="app.status === 'installed' && app.id.startsWith('plugin_')" @click="runPlugin(app.id)">运行</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { fetchApps, installApp, uninstallApp, runPlugin } from '../../api'

const apps = ref<any[]>([])

async function loadApps() {
  try {
    const response = await fetchApps()
    apps.value = response.data.apps
  } catch (error) {
    console.error(error)
  }
}

async function installAppHandler(id: string) {
  try {
    await installApp(id)
    loadApps()
  } catch (error) {
    console.error(error)
  }
}

async function uninstallAppHandler(id: string) {
  try {
    await uninstallApp(id)
    loadApps()
  } catch (error) {
    console.error(error)
  }
}

async function runPluginHandler(id: string) {
  try {
    const response = await runPlugin(id)
    alert(`插件执行结果: ${response.data.result || response.data.message}`)
  } catch (error) {
    console.error(error)
  }
}

onMounted(loadApps)
</script>
