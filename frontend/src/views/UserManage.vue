<template>
  <div class="user-manage">
    <div class="page-header">
      <h2>用户管理</h2>
      <el-button type="primary" :icon="Plus" @click="showRegisterDialog">注册新用户</el-button>
    </div>

    <el-card>
      <el-table :data="users" v-loading="loading" stripe>
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column prop="username" label="用户名" width="140" />
        <el-table-column prop="email" label="邮箱" min-width="200" />
        <el-table-column prop="full_name" label="姓名" width="140">
          <template #default="{ row }">{{ row.full_name || '-' }}</template>
        </el-table-column>
        <el-table-column label="角色" width="120">
          <template #default="{ row }">
            <el-tag v-if="row.is_superuser" type="danger" size="small">超级管理员</el-tag>
            <el-tag v-else type="info" size="small">普通用户</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.is_active ? 'success' : 'danger'" size="small">
              {{ row.is_active ? '活跃' : '已禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="{ row }">{{ formatDate(row.created_at) }}</template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- Register User Dialog -->
    <el-dialog v-model="registerDialogVisible" title="注册新用户" width="480px">
      <el-form
        ref="registerFormRef"
        :model="registerForm"
        :rules="registerRules"
        label-width="80px"
      >
        <el-form-item label="用户名" prop="username">
          <el-input v-model="registerForm.username" placeholder="用户名" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="registerForm.email" placeholder="邮箱地址" />
        </el-form-item>
        <el-form-item label="姓名">
          <el-input v-model="registerForm.full_name" placeholder="姓名（可选）" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input
            v-model="registerForm.password"
            type="password"
            show-password
            placeholder="密码（至少6位）"
          />
        </el-form-item>
        <el-form-item label="用户类型">
          <el-checkbox v-model="registerForm.is_superuser">
            创建为超级管理员
          </el-checkbox>
          <div style="color: #909399; font-size: 12px; margin-top: 4px;">
            超级管理员可以管理所有社区和用户
          </div>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="registerDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleRegister" :loading="submitting">注册</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { listAllUsers, register } from '../api/auth'
import type { User } from '../stores/auth'

const users = ref<User[]>([])
const loading = ref(false)
const registerDialogVisible = ref(false)
const submitting = ref(false)
const registerFormRef = ref<FormInstance>()

const registerForm = ref({
  username: '',
  email: '',
  full_name: '',
  password: '',
  is_superuser: false,
})

const registerRules: FormRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, message: '用户名至少3个字符', trigger: 'blur' },
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入有效的邮箱地址', trigger: 'blur' },
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码至少6位', trigger: 'blur' },
  ],
}

async function loadUsers() {
  loading.value = true
  try {
    users.value = await listAllUsers()
  } catch {
    ElMessage.error('加载用户列表失败')
  } finally {
    loading.value = false
  }
}

function showRegisterDialog() {
  registerForm.value = { username: '', email: '', full_name: '', password: '', is_superuser: false }
  registerDialogVisible.value = true
}

async function handleRegister() {
  if (!registerFormRef.value) return
  await registerFormRef.value.validate()

  submitting.value = true
  try {
    await register({
      username: registerForm.value.username,
      email: registerForm.value.email,
      password: registerForm.value.password,
      full_name: registerForm.value.full_name || undefined,
      is_superuser: registerForm.value.is_superuser,
    })
    ElMessage.success('用户注册成功')
    registerDialogVisible.value = false
    await loadUsers()
  } catch (e: any) {
    ElMessage.error(e?.response?.data?.detail || '注册失败')
  } finally {
    submitting.value = false
  }
}

function formatDate(d: string) {
  return new Date(d).toLocaleString('zh-CN')
}

onMounted(loadUsers)
</script>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.page-header h2 { margin: 0; }
</style>
