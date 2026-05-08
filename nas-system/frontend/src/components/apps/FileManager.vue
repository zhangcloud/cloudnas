<template>
  <div>
    <h1>文件总管</h1>
    <div style="display: flex; gap: 1rem; margin-bottom: 1rem; flex-wrap: wrap; align-items: center;">
      <button @click="loadFiles(currentPath)">刷新</button>
      <button @click="mkdir">新建文件夹</button>
      <button @click="goBack" :disabled="!currentPath">返回上级</button>
      <label style="display: inline-flex; gap: 0.5rem; align-items: center;">
        上传文件
        <input type="file" @change="handleFileUpload" />
      </label>
    </div>

    <div style="margin-bottom: 1rem;">当前目录：{{ currentPath || '/' }}</div>

    <table style="width: 100%; border-collapse: collapse;">
      <thead>
        <tr>
          <th>名称</th>
          <th>类型</th>
          <th>大小</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="entry in entries" :key="entry.path">
          <td>
            <a v-if="entry.is_dir" href="#" @click.prevent="loadFiles(entry.path)">📁 {{ entry.name }}</a>
            <span v-else>{{ entry.name }}</span>
          </td>
          <td>{{ entry.is_dir ? '文件夹' : '文件' }}</td>
          <td>{{ entry.is_dir ? '-' : entry.size }}</td>
          <td>
            <button v-if="!entry.is_dir" @click="downloadEntry(entry)">下载</button>
            <button @click="deleteEntry(entry)">删除</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { fetchFiles, createDirectory, uploadFile, downloadFile, deletePath } from '../../api'

const entries = ref<any[]>([])
const currentPath = ref('')

async function loadFiles(path = '') {
  try {
    const response = await fetchFiles(path)
    entries.value = response.data.entries
    currentPath.value = response.data.path
  } catch (error) {
    console.error(error)
  }
}

function goBack() {
  if (!currentPath.value) return
  const parts = currentPath.value.split('/').filter(Boolean)
  parts.pop()
  loadFiles(parts.join('/'))
}

async function mkdir() {
  const name = prompt('请输入新文件夹名称')
  if (!name) return
  try {
    const newPath = currentPath.value ? `${currentPath.value}/${name}` : name
    await createDirectory(newPath)
    loadFiles(currentPath.value)
  } catch (error) {
    console.error(error)
  }
}

async function handleFileUpload(event: Event) {
  const target = event.target as HTMLInputElement
  if (!target.files || !target.files.length) return
  const file = target.files[0]
  try {
    await uploadFile(currentPath.value, file)
    loadFiles(currentPath.value)
  } catch (error) {
    console.error(error)
  } finally {
    target.value = ''
  }
}

async function downloadEntry(entry: any) {
  try {
    const response = await downloadFile(entry.path)
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const a = document.createElement('a')
    a.href = url
    a.download = entry.name
    document.body.appendChild(a)
    a.click()
    a.remove()
    window.URL.revokeObjectURL(url)
  } catch (error) {
    console.error(error)
  }
}

async function deleteEntry(entry: any) {
  if (!confirm(`确认删除 ${entry.name} 吗？`)) return
  try {
    await deletePath(entry.path)
    loadFiles(currentPath.value)
  } catch (error) {
    console.error(error)
  }
}

onMounted(() => loadFiles())
</script>
