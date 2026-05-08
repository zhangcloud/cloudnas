<template>
  <div>
    <h1>存储管理</h1>
    <div class="dsm-grid">
      <div class="dsm-widget">
        <h3>存储操作</h3>
        <button @click="loadVolumes">刷新存储池</button>
        <button @click="scanDisks">扫描磁盘</button>
        <router-link to="/san" style="display: inline-block; margin-left: 1rem;">
          <button>SAN 管理</button>
        </router-link>
      </div>
    </div>
    <div style="margin: 1rem 0; display: flex; gap: 1rem; align-items: center; flex-wrap: wrap;">
      <input v-model="newName" placeholder="存储池名称" />
      <input v-model="newSize" placeholder="容量，例如 4TB" />
      <button @click="createNewVolume">创建存储池</button>
    </div>
    <h2>存储池</h2>
    <table style="width: 100%; border-collapse: collapse; margin-bottom: 1.5rem;">
      <thead>
        <tr>
          <th>名称</th>
          <th>类型</th>
          <th>总量</th>
          <th>已用</th>
          <th>状态</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="vol in volumes" :key="vol.id">
          <td>{{ vol.name }}</td>
          <td>{{ vol.type }}</td>
          <td>{{ vol.total }}</td>
          <td>{{ vol.used }}</td>
          <td>{{ vol.status }}</td>
        </tr>
      </tbody>
    </table>

    <h2>磁盘列表</h2>
    <table style="width: 100%; border-collapse: collapse;">
      <thead>
        <tr>
          <th>ID</th>
          <th>型号</th>
          <th>容量</th>
          <th>状态</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="disk in disks" :key="disk.id">
          <td>{{ disk.id }}</td>
          <td>{{ disk.model }}</td>
          <td>{{ disk.size }}</td>
          <td>{{ disk.status }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { fetchVolumes, createVolume, fetchDisks, scanDisks as scanDisksApi } from '../../api'
