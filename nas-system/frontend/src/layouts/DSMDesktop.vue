<template>
  <div>
    <header class="navbar">
      <a href="/">CloudNAS</a>
      <router-link to="/files">文件总管</router-link>
      <router-link to="/storage">存储管理</router-link>
      <router-link to="/users">用户管理</router-link>
      <router-link to="/shares">共享管理</router-link>
      <router-link to="/network">网络管理</router-link>
      <router-link to="/tasks">任务调度</router-link>
      <router-link to="/apps">应用中心</router-link>
      <router-link to="/snapshots">快照管理</router-link>
      <router-link to="/san">SAN 管理</router-link>
      <router-link to="/settings">控制面板</router-link>
    </header>
    <main class="card" style="margin: 1rem;">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts"></script>
