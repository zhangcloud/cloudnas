import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE || 'http://localhost:8000/api/v1',
  timeout: 5000,
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('cloudnas_token')
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export function login(username: string, password: string) {
  const data = new URLSearchParams()
  data.append('username', username)
  data.append('password', password)
  return api.post('/auth/login', data)
}

export function fetchFiles(path = '') {
  return api.get('/files/list', { params: { path } })
}

export function createDirectory(path: string) {
  return api.post('/files/mkdir', { path })
}

export function uploadFile(path: string, file: File) {
  const form = new FormData()
  form.append('path', path)
  form.append('file', file)
  return api.post('/files/upload', form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
}

export function downloadFile(path: string) {
  return api.get('/files/download', { params: { path }, responseType: 'blob' })
}

export function deletePath(path: string) {
  return api.delete('/files/delete', { data: { path } })
}

export function fetchVolumes() {
  return api.get('/storage/volumes')
}

export function fetchDisks() {
  return api.get('/storage/disks')
}

export function scanDisks() {
  return api.post('/storage/scan')
}

export function fetchDisks() {
  return api.get('/storage/disks')
}

export function scanDisks() {
  return api.post('/storage/scan')
}

export function createVolume(name: string, size: string) {
  return api.post('/storage/create', { name, size })
}

export function fetchNetworkStatus() {
  return api.get('/network/status')
}

export function toggleNetworkService(service: string, action: string) {
  return api.post('/network/toggle-service', { service, action })
}

export function fetchUsers() {
  return api.get('/users/list')
}

export function createUser(username: string, password: string, full_name: string) {
  return api.post('/users/create', { username, password, full_name, email: `${username}@cloudnas.local` })
}

export function deleteUser(username: string) {
  return api.delete('/users/delete', { data: { username } })
}

export function fetchShares() {
  return api.get('/shares/list')
}

export function createShare(name: string, path: string, access: string) {
  return api.post('/shares/create', { name, path, access })
}

export function deleteShare(id: string) {
  return api.delete('/shares/delete', { data: { share_id: id } })
}

export function fetchNfsShares() {
  return api.get('/shares/nfs/list')
}

export function createNfsShare(path: string, clients: string[], options: string) {
  return api.post('/shares/nfs/create', { path, clients, options })
}

export function deleteNfsShare(path: string) {
  return api.delete('/shares/nfs/delete', { data: { path } })
}

export function fetchCifsShares() {
  return api.get('/shares/cifs/list')
}

export function createCifsShare(name: string, path: string, comment: string, public: boolean, writable: boolean) {
  return api.post('/shares/cifs/create', { name, path, comment, public, writable })
}

export function deleteCifsShare(name: string) {
  return api.delete('/shares/cifs/delete', { data: { name } })
}

export function fetchTasks() {
  return api.get('/tasks/list')
}

export function createTask(name: string, type: string, schedule: string) {
  return api.post('/tasks/create', { name, type, schedule })
}

export function toggleTask(task_id: string, enable: boolean) {
  return api.post('/tasks/toggle', { task_id, enable })
}

export function fetchApps() {
  return api.get('/apps/list')
}

export function installApp(app_id: string) {
  return api.post('/apps/install', { app_id })
}

export function uninstallApp(app_id: string) {
  return api.post('/apps/uninstall', { app_id })
}

export function runPlugin(plugin_id: string) {
  return api.post('/apps/run', { plugin_id })
}

export function fetchSnapshots() {
  return api.get('/snapshots/list')
}

export function createSnapshot(name: string) {
  return api.post('/snapshots/create', { name })
}

export function restoreSnapshot(snapshot_id: string) {
  return api.post('/snapshots/restore', { snapshot_id })
}

export function fetchSystemStatus() {
  return api.get('/system/status')
}

export function fetchIscsiTargets() {
  return api.get('/san/iscsi/targets')
}

export function createIscsiTarget(name: string, lun_path: string) {
  return api.post('/san/iscsi/create', { name, lun_path })
}

export function addIscsiClient(target_id: string, client_iqn: string) {
  return api.post('/san/iscsi/add-client', { target_id, client_iqn })
}

export function fetchFcTargets() {
  return api.get('/san/fc/targets')
}

export function createFcTarget(name: string, wwn: string) {
  return api.post('/san/fc/create', { name, wwn })
}

export function fetchSanStatus() {
  return api.get('/san/status')
}

export default api
