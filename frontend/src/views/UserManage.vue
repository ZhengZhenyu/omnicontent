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
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="showEditDialog(row)">编辑</el-button>
            <el-button
              v-if="row.id !== currentUser?.id"
              size="small"
              type="danger"
              @click="handleDelete(row)"
            >删除</el-button>
          </template>
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

    <!-- Edit User Dialog -->
    <el-dialog v-model="editDialogVisible" title="编辑用户" width="480px">
      <el-form
        ref="editFormRef"
        :model="editForm"
        :rules="editRules"
        label-width="80px"
      >
        <el-form-item label="用户名">
          <el-input :model-value="editForm.username" disabled />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="editForm.email" placeholder="邮箱地址" />
        </el-form-item>
        <el-form-item label="姓名">
          <el-input v-model="editForm.full_name" placeholder="姓名（可选）" />
        </el-form-item>
        <el-form-item label="状态">
          <el-switch
            v-model="editForm.is_active"
            active-text="活跃"
            inactive-text="禁用"
            :disabled="editForm.id === currentUser?.id"
          />
        </el-form-item>
        <el-form-item label="用户类型">
          <el-checkbox v-model="editForm.is_superuser">
            超级管理员
          </el-checkbox>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="editDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleEdit" :loading="submitting">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { listAllUsers, register, updateUser, deleteUser } from '../api/auth'
import { useAuthStore } from '../stores/auth'
import type { User } from '../stores/auth'

const authStore = useAuthStore()
const currentUser = authStore.user

const users = ref<User[]>([])
const loading = ref(false)
const registerDialogVisible = ref(false)
const editDialogVisible = ref(false)
const submitting = ref(false)
const registerFormRef = ref<FormInstance>()
const editFormRef = ref<FormInstance>()

const registerForm = ref({
  username: '',
  email: '',
  full_name: '',
  password: '',
  is_superuser: false,
})

const editForm = ref({
  id: 0,
  username: '',
  email: '',
  full_name: '',
  is_active: true,
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

const editRules: FormRules = {
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入有效的邮箱地址', trigger: 'blur' },
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

function showEditDialog(user: User) {
  editForm.value = {
    id: user.id,
    username: user.username,
    email: user.email,
    full_name: user.full_name || '',
    is_active: user.is_active,
    is_superuser: user.is_superuser,
  }
  editDialogVisible.value = true
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

async function handleEdit() {
  if (!editFormRef.value) return
  await editFormRef.value.validate()

  submitting.value = true
  try {
    await updateUser(editForm.value.id, {
      email: editForm.value.email,
      full_name: editForm.value.full_name || undefined,
      is_active: editForm.value.is_active,
      is_superuser: editForm.value.is_superuser,
    })
    ElMessage.success('用户信息已更新')
    editDialogVisible.value = false
    await loadUsers()
  } catch (e: any) {
    ElMessage.error(e?.response?.data?.detail || '更新失败')
  } finally {
    submitting.value = false
  }
}

async function handleDelete(user: User) {
  try {
    await ElMessageBox.confirm(
      `确定要删除用户「${user.username}」吗？此操作不可恢复。`,
      '确认删除',
      { confirmButtonText: '删除', cancelButtonText: '取消', type: 'warning' },
    )
  } catch {
    return
  }

  try {
    await deleteUser(user.id)
    ElMessage.success('用户已删除')
    await loadUsers()
  } catch (e: any) {
    ElMessage.error(e?.response?.data?.detail || '删除失败')
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
