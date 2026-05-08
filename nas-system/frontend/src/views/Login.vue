<template>
  <div style="display: flex; align-items: center; justify-content: center; min-height: 100vh;">
    <div class="card" style="width: 360px;">
      <h1>CloudNAS 登录</h1>
      <form @submit.prevent="submitLogin" style="display: grid; gap: 1rem;">
        <input v-model="username" type="text" placeholder="用户名" />
        <input v-model="password" type="password" placeholder="密码" />
        <button type="submit">登录</button>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { login } from '../api'

const username = ref('admin')
const password = ref('admin123')
const router = useRouter()

async function submitLogin() {
  try {
    const response = await login(username.value, password.value)
    localStorage.setItem('cloudnas_token', response.data.access_token)
    router.push('/')
  } catch (error) {
    alert('登录失败，请检查用户名或密码')
  }
}
</script>
