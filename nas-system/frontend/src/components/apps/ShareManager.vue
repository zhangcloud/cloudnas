<template>
  <div>
    <h1>共享管理</h1>
    <div style="margin-bottom: 1rem;">
      <button @click="activeTab = 'basic'" :class="{ active: activeTab === 'basic' }">基本共享</button>
      <button @click="activeTab = 'nfs'" :class="{ active: activeTab === 'nfs' }">NFS 共享</button>
      <button @click="activeTab = 'cifs'" :class="{ active: activeTab === 'cifs' }">CIFS 共享</button>
    </div>

    <!-- 基本共享 -->
    <div v-if="activeTab === 'basic'">
      <div style="margin-bottom: 1rem; display: flex; gap: 1rem; flex-wrap: wrap; align-items: center;">
        <input v-model="name" placeholder="共享名称" />
        <input v-model="path" placeholder="共享路径" />
        <select v-model="access">
          <option>Everyone</option>
          <option>Admin</option>
        </select>
        <button @click="createShareHandler">创建共享</button>
      </div>
      <table style="width: 100%; border-collapse: collapse;">
        <thead>
          <tr>
            <th>名称</th>
            <th>路径</th>
            <th>访问</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="share in shares" :key="share.id">
            <td>{{ share.name }}</td>
            <td>{{ share.path }}</td>
            <td>{{ share.access }}</td>
            <td><button @click="deleteShareHandler(share.id)">删除</button></td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- NFS 共享 -->
    <div v-if="activeTab === 'nfs'">
      <div style="margin-bottom: 1rem; display: flex; gap: 1rem; flex-wrap: wrap; align-items: center;">
        <input v-model="nfsPath" placeholder="共享路径" />
        <input v-model="nfsClients" placeholder="客户端 (用逗号分隔)" />
        <input v-model="nfsOptions" placeholder="选项 (如 rw,sync)" />
        <button @click="createNfsShareHandler">创建 NFS 共享</button>
      </div>
      <table style="width: 100%; border-collapse: collapse;">
        <thead>
          <tr>
            <th>路径</th>
            <th>客户端</th>
            <th>选项</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="share in nfsShares" :key="share.path">
            <td>{{ share.path }}</td>
            <td>{{ share.clients.join(', ') }}</td>
            <td>{{ share.options }}</td>
            <td><button @click="deleteNfsShareHandler(share.path)">删除</button></td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- CIFS 共享 -->
    <div v-if="activeTab === 'cifs'">
      <div style="margin-bottom: 1rem; display: flex; gap: 1rem; flex-wrap: wrap; align-items: center;">
        <input v-model="cifsName" placeholder="共享名称" />
        <input v-model="cifsPath" placeholder="共享路径" />
        <input v-model="cifsComment" placeholder="注释" />
        <label><input type="checkbox" v-model="cifsPublic" /> 公共</label>
        <label><input type="checkbox" v-model="cifsWritable" /> 可写</label>
        <button @click="createCifsShareHandler">创建 CIFS 共享</button>
      </div>
      <table style="width: 100%; border-collapse: collapse;">
        <thead>
          <tr>
            <th>名称</th>
            <th>路径</th>
            <th>注释</th>
            <th>公共</th>
            <th>可写</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="share in cifsShares" :key="share.name">
            <td>{{ share.name }}</td>
            <td>{{ share.path }}</td>
            <td>{{ share.comment }}</td>
            <td>{{ share.public ? '是' : '否' }}</td>
            <td>{{ share.writable ? '是' : '否' }}</td>
            <td><button @click="deleteCifsShareHandler(share.name)">删除</button></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { fetchShares, createShare, deleteShare, fetchNfsShares, createNfsShare, deleteNfsShare, fetchCifsShares, createCifsShare, deleteCifsShare } from '../../api'

const activeTab = ref('basic')
const shares = ref<any[]>([])
const name = ref('')
const path = ref('/tmp/cloudnas_storage')
const access = ref('Admin')

const nfsShares = ref<any[]>([])
const nfsPath = ref('/tmp/cloudnas_storage')
const nfsClients = ref('')
const nfsOptions = ref('rw,sync')

const cifsShares = ref<any[]>([])
const cifsName = ref('')
const cifsPath = ref('/tmp/cloudnas_storage')
const cifsComment = ref('')
const cifsPublic = ref(false)
const cifsWritable = ref(true)

async function loadShares() {
  try {
    const response = await fetchShares()
    shares.value = response.data.shares
  } catch (error) {
    console.error(error)
  }
}

async function createShareHandler() {
  if (!name.value || !path.value) return
  try {
    await createShare(name.value, path.value, access.value)
    name.value = ''
    path.value = '/tmp/cloudnas_storage'
    access.value = 'Admin'
    loadShares()
  } catch (error) {
    console.error(error)
  }
}

async function deleteShareHandler(id: string) {
  if (!confirm('确认删除共享吗？')) return
  try {
    await deleteShare(id)
    loadShares()
  } catch (error) {
    console.error(error)
  }
}

async function loadNfsShares() {
  try {
    const response = await fetchNfsShares()
    nfsShares.value = response.data.shares
  } catch (error) {
    console.error(error)
  }
}

async function createNfsShareHandler() {
  if (!nfsPath.value || !nfsClients.value) return
  try {
    await createNfsShare(nfsPath.value, nfsClients.value.split(',').map(c => c.trim()), nfsOptions.value)
    nfsPath.value = '/tmp/cloudnas_storage'
    nfsClients.value = ''
    nfsOptions.value = 'rw,sync'
    loadNfsShares()
  } catch (error) {
    console.error(error)
  }
}

async function deleteNfsShareHandler(path: string) {
  if (!confirm('确认删除 NFS 共享吗？')) return
  try {
    await deleteNfsShare(path)
    loadNfsShares()
  } catch (error) {
    console.error(error)
  }
}

async function loadCifsShares() {
  try {
    const response = await fetchCifsShares()
    cifsShares.value = response.data.shares
  } catch (error) {
    console.error(error)
  }
}

async function createCifsShareHandler() {
  if (!cifsName.value || !cifsPath.value) return
  try {
    await createCifsShare(cifsName.value, cifsPath.value, cifsComment.value, cifsPublic.value, cifsWritable.value)
    cifsName.value = ''
    cifsPath.value = '/tmp/cloudnas_storage'
    cifsComment.value = ''
    cifsPublic.value = false
    cifsWritable.value = true
    loadCifsShares()
  } catch (error) {
    console.error(error)
  }
}

async function deleteCifsShareHandler(name: string) {
  if (!confirm('确认删除 CIFS 共享吗？')) return
  try {
    await deleteCifsShare(name)
    loadCifsShares()
  } catch (error) {
    console.error(error)
  }
}

onMounted(() => {
  loadShares()
  loadNfsShares()
  loadCifsShares()
})
</script>

<style scoped>
button.active {
  background-color: #007bff;
  color: white;
}
</style>
