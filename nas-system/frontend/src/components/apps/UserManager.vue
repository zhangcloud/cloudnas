<template>
  <div>
    <h1>用户管理</h1>
    <div style="margin-bottom: 1rem; display: flex; gap: 1rem; flex-wrap: wrap; align-items: center;">
      <input v-model="username" placeholder="用户名" />
      <input v-model="password" type="password" placeholder="密码" />
      <input v-model="fullName" placeholder="姓名" />
      <button @click="createUser">创建用户</button>
    </div>
    <table style="width: 100%; border-collapse: collapse;">
      <thead>
        <tr>
          <th>用户名</th>
          <th>姓名</th>
          <th>邮箱</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.username">
          <td>{{ user.username }}</td>
          <td>{{ user.full_name }}</td>
          <td>{{ user.email }}</td>
          <td><button @click="deleteUser(user.username)">删除</button></td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { fetchUsers, createUser, deleteUser } from '../../api'

const users = ref<any[]>([])
const username = ref('')
const password = ref('')
const fullName = ref('')

async function loadUsers() {
  try {
    const response = await fetchUsers()
    users.value = response.data.users
  } catch (error) {
    console.error(error)
  }
}

async function createUserHandler() {
  if (!username.value || !password.value) return
  try {
    await createUser(username.value, password.value, fullName.value)
    username.value = ''
    password.value = ''
    fullName.value = ''
    loadUsers()
  } catch (error) {
    console.error(error)
  }
}

async function deleteUserHandler(name: string) {
  if (!confirm(`确认删除用户 ${name} 吗？`)) return
  try {
    await deleteUser(name)
    loadUsers()
  } catch (error) {
    console.error(error)
  }
}

onMounted(loadUsers)
</script>
