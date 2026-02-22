<template>
  <div class="placeholder-page">
    <div class="placeholder-content">
      <el-icon class="placeholder-icon"><Flag /></el-icon>
      <h2 class="placeholder-title">活动管理</h2>
      <p class="placeholder-desc">活动策划、执行、复盘全流程管理功能即将上线。</p>
      <el-tag type="info" size="large">功能开发中</el-tag>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Flag } from '@element-plus/icons-vue'
</script>

<style scoped>
.placeholder-page {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  min-height: 400px;
  padding: 48px;
}

.placeholder-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  text-align: center;
  max-width: 420px;
}

.placeholder-icon {
  font-size: 56px;
  color: #cbd5e1;
}

.placeholder-title {
  margin: 0;
  font-size: 22px;
  font-weight: 600;
  color: #1e293b;
}

.placeholder-desc {
  margin: 0;
  font-size: 14px;
  color: #64748b;
  line-height: 1.6;
}
</style>
