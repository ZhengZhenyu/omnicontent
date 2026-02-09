<template>
  <el-card class="member-card" :body-style="{ padding: '20px' }">
    <div class="member-header">
      <el-avatar :size="size === 'small' ? 40 : 60" :src="member.avatar_url">
        {{ member.name.charAt(0) }}
      </el-avatar>
      <div class="member-info">
        <div class="member-name">
          {{ member.name }}
          <el-tag v-if="!member.is_active" type="info" size="small">已离任</el-tag>
        </div>
        <div v-if="member.organization" class="member-org">
          {{ member.organization }}
        </div>
        <div class="member-roles">
          <RoleBadge
            v-for="role in member.roles"
            :key="role"
            :role="role"
            size="small"
          />
        </div>
      </div>
    </div>

    <div v-if="showDetails" class="member-details">
      <div v-if="member.bio" class="member-bio">
        {{ member.bio }}
      </div>

      <div class="member-contacts">
        <div v-if="member.email" class="contact-item">
          <el-icon><Message /></el-icon>
          <span>{{ member.email }}</span>
        </div>
        <div v-if="member.phone" class="contact-item">
          <el-icon><Phone /></el-icon>
          <span>{{ member.phone }}</span>
        </div>
        <div v-if="member.wechat" class="contact-item">
          <el-icon><ChatDotRound /></el-icon>
          <span>{{ member.wechat }}</span>
        </div>
      </div>

      <div v-if="member.term_start || member.term_end" class="member-term">
        <el-icon><Calendar /></el-icon>
        <span>
          任期: {{ formatDate(member.term_start) }} ~ {{ formatDate(member.term_end) || '至今' }}
        </span>
      </div>
    </div>

    <div v-if="showActions" class="member-actions">
      <el-button
        type="primary"
        size="small"
        link
        @click="$emit('edit', member)"
      >
        <el-icon><Edit /></el-icon>
        编辑
      </el-button>
      <el-button
        type="danger"
        size="small"
        link
        @click="$emit('delete', member)"
      >
        <el-icon><Delete /></el-icon>
        删除
      </el-button>
    </div>
  </el-card>
</template>

<script setup lang="ts">
import { Message, Phone, ChatDotRound, Calendar, Edit, Delete } from '@element-plus/icons-vue'
import RoleBadge from './RoleBadge.vue'
import type { CommitteeMember } from '@/api/governance'

interface Props {
  member: CommitteeMember
  size?: 'default' | 'small'
  showDetails?: boolean
  showActions?: boolean
}

withDefaults(defineProps<Props>(), {
  size: 'default',
  showDetails: true,
  showActions: false
})

defineEmits<{
  edit: [member: CommitteeMember]
  delete: [member: CommitteeMember]
}>()

function formatDate(dateStr?: string) {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('zh-CN')
}
</script>

<style scoped>
.member-card {
  margin-bottom: 16px;
}

.member-header {
  display: flex;
  gap: 16px;
  margin-bottom: 16px;
}

.member-info {
  flex: 1;
}

.member-name {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 4px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.member-org {
  color: var(--el-text-color-secondary);
  font-size: 14px;
  margin-bottom: 8px;
}

.member-roles {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.member-details {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid var(--el-border-color-lighter);
}

.member-bio {
  color: var(--el-text-color-regular);
  font-size: 14px;
  margin-bottom: 12px;
  line-height: 1.6;
}

.member-contacts {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 12px;
}

.contact-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: var(--el-text-color-regular);
}

.contact-item .el-icon {
  color: var(--el-text-color-secondary);
}

.member-term {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: var(--el-text-color-secondary);
}

.member-actions {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid var(--el-border-color-lighter);
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}
</style>
