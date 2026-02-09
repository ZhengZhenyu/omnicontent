<template>
  <div class="community-manage">
    <div class="page-header">
      <h2>社区管理</h2>
      <el-button type="primary" :icon="Plus" @click="showCreateDialog">新建社区</el-button>
    </div>

    <el-row :gutter="20">
      <el-col :span="8" v-for="community in communities" :key="community.id">
        <el-card class="community-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <div class="community-title">
                <span class="name">{{ community.name }}</span>
                <el-tag v-if="!community.is_active" type="danger" size="small">已停用</el-tag>
              </div>
              <el-dropdown @command="(cmd: string) => handleCommunityAction(cmd, community)">
                <el-icon class="more-icon"><MoreFilled /></el-icon>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item command="edit">编辑</el-dropdown-item>
                    <el-dropdown-item command="members">成员管理</el-dropdown-item>
                    <el-dropdown-item command="toggle">{{ community.is_active ? '停用' : '启用' }}</el-dropdown-item>
                    <el-dropdown-item command="delete" divided style="color: #f56c6c">删除</el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </div>
          </template>
          <div class="community-info">
            <p class="slug"><el-icon><Link /></el-icon> {{ community.slug }}</p>
            <p class="desc">{{ community.description || '暂无描述' }}</p>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- Create/Edit Community Dialog -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEditing ? '编辑社区' : '新建社区'"
      width="500px"
    >
      <el-form
        ref="formRef"
        :model="communityForm"
        :rules="formRules"
        label-width="80px"
      >
        <el-form-item label="名称" prop="name">
          <el-input v-model="communityForm.name" placeholder="社区名称" />
        </el-form-item>
        <el-form-item label="标识" prop="slug">
          <el-input
            v-model="communityForm.slug"
            placeholder="英文标识 (如 my-community)"
            :disabled="isEditing"
          />
        </el-form-item>
        <el-form-item label="描述">
          <el-input
            v-model="communityForm.description"
            type="textarea"
            :rows="3"
            placeholder="社区描述"
          />
        </el-form-item>
        <el-form-item label="Logo URL">
          <el-input v-model="communityForm.logo_url" placeholder="Logo 图片地址（可选）" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">确定</el-button>
      </template>
    </el-dialog>

    <!-- Members Management Dialog -->
    <el-dialog
      v-model="membersDialogVisible"
      :title="`成员管理 - ${selectedCommunity?.name || ''}`"
      width="700px"
    >
      <div class="members-header">
        <el-select
          v-model="selectedUserId"
          filterable
          placeholder="搜索用户并添加"
          style="width: 280px"
        >
          <el-option
            v-for="u in availableUsers"
            :key="u.id"
            :label="`${u.username} (${u.email})`"
            :value="u.id"
          />
        </el-select>
        <el-button type="primary" :disabled="!selectedUserId" @click="handleAddMember">
          添加成员
        </el-button>
      </div>

      <el-table :data="communityUsers" stripe style="margin-top: 16px">
        <el-table-column prop="username" label="用户名" width="140" />
        <el-table-column prop="email" label="邮箱" min-width="200" />
        <el-table-column prop="full_name" label="姓名" width="120" />
        <el-table-column label="角色" width="160">
          <template #default="{ row }">
            <template v-if="row.is_superuser">
              <el-tag type="danger" size="small">超级管理员</el-tag>
            </template>
            <template v-else>
              <el-select
                :model-value="row.role"
                size="small"
                style="width: 110px"
                @change="(val: string) => handleRoleChange(row, val)"
              >
                <el-option label="管理员" value="admin" />
                <el-option label="普通用户" value="user" />
              </el-select>
            </template>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="100">
          <template #default="{ row }">
            <el-popconfirm
              title="确定移除该成员？"
              @confirm="handleRemoveMember(row.id)"
              :disabled="row.is_superuser"
            >
              <template #reference>
                <el-button size="small" type="danger" :disabled="row.is_superuser">
                  移除
                </el-button>
              </template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import { Plus, MoreFilled, Link } from '@element-plus/icons-vue'
import type { Community } from '../stores/auth'
import {
  getCommunities,
  createCommunity,
  updateCommunity,
  deleteCommunity,
  getCommunityUsers,
  addUserToCommunity,
  removeUserFromCommunity,
  updateUserRole,
  type CommunityUser,
} from '../api/community'
import { listAllUsers } from '../api/auth'
import type { User } from '../stores/auth'

const communities = ref<Community[]>([])
const dialogVisible = ref(false)
const membersDialogVisible = ref(false)
const isEditing = ref(false)
const submitting = ref(false)
const editingId = ref<number | null>(null)
const formRef = ref<FormInstance>()

const communityForm = ref({
  name: '',
  slug: '',
  description: '',
  logo_url: '',
})

const formRules: FormRules = {
  name: [{ required: true, message: '请输入社区名称', trigger: 'blur' }],
  slug: [
    { required: true, message: '请输入社区标识', trigger: 'blur' },
    { pattern: /^[a-z0-9-]+$/, message: '只能包含小写字母、数字和连字符', trigger: 'blur' },
  ],
}

const selectedCommunity = ref<Community | null>(null)
const communityUsers = ref<CommunityUser[]>([])
const allUsers = ref<User[]>([])
const selectedUserId = ref<number | null>(null)

const availableUsers = computed(() => {
  const memberIds = new Set(communityUsers.value.map((u) => u.id))
  return allUsers.value.filter((u) => !memberIds.has(u.id))
})

async function loadCommunities() {
  try {
    communities.value = await getCommunities()
  } catch {
    ElMessage.error('加载社区列表失败')
  }
}

function showCreateDialog() {
  isEditing.value = false
  editingId.value = null
  communityForm.value = { name: '', slug: '', description: '', logo_url: '' }
  dialogVisible.value = true
}

function showEditDialog(community: Community) {
  isEditing.value = true
  editingId.value = community.id
  communityForm.value = {
    name: community.name,
    slug: community.slug,
    description: community.description || '',
    logo_url: community.logo_url || '',
  }
  dialogVisible.value = true
}

async function handleSubmit() {
  if (!formRef.value) return
  await formRef.value.validate()

  submitting.value = true
  try {
    if (isEditing.value && editingId.value) {
      await updateCommunity(editingId.value, {
        name: communityForm.value.name,
        description: communityForm.value.description,
        logo_url: communityForm.value.logo_url || undefined,
      })
      ElMessage.success('社区更新成功')
    } else {
      await createCommunity(communityForm.value)
      ElMessage.success('社区创建成功')
    }
    dialogVisible.value = false
    await loadCommunities()
  } catch (e: any) {
    ElMessage.error(e?.response?.data?.detail || '操作失败')
  } finally {
    submitting.value = false
  }
}

async function handleCommunityAction(command: string, community: Community) {
  switch (command) {
    case 'edit':
      showEditDialog(community)
      break
    case 'members':
      await showMembersDialog(community)
      break
    case 'toggle':
      try {
        await updateCommunity(community.id, { is_active: !community.is_active })
        ElMessage.success(community.is_active ? '社区已停用' : '社区已启用')
        await loadCommunities()
      } catch {
        ElMessage.error('操作失败')
      }
      break
    case 'delete':
      try {
        await ElMessageBox.confirm(
          `确定要删除社区 "${community.name}" 吗？此操作不可恢复，所有相关数据将被删除。`,
          '删除确认',
          { type: 'warning', confirmButtonText: '删除', cancelButtonText: '取消' }
        )
        await deleteCommunity(community.id)
        ElMessage.success('社区已删除')
        await loadCommunities()
      } catch {
        // cancelled
      }
      break
  }
}

async function showMembersDialog(community: Community) {
  selectedCommunity.value = community
  selectedUserId.value = null
  try {
    communityUsers.value = await getCommunityUsers(community.id)
    allUsers.value = await listAllUsers()
  } catch {
    ElMessage.error('加载成员列表失败')
  }
  membersDialogVisible.value = true
}

async function handleAddMember() {
  if (!selectedCommunity.value || !selectedUserId.value) return
  try {
    await addUserToCommunity(selectedCommunity.value.id, selectedUserId.value)
    ElMessage.success('成员添加成功')
    communityUsers.value = await getCommunityUsers(selectedCommunity.value.id)
    selectedUserId.value = null
  } catch (e: any) {
    ElMessage.error(e?.response?.data?.detail || '添加失败')
  }
}

async function handleRemoveMember(userId: number) {
  if (!selectedCommunity.value) return
  try {
    await removeUserFromCommunity(selectedCommunity.value.id, userId)
    ElMessage.success('成员已移除')
    communityUsers.value = await getCommunityUsers(selectedCommunity.value.id)
  } catch (e: any) {
    ElMessage.error(e?.response?.data?.detail || '移除失败')
  }
}

async function handleRoleChange(user: CommunityUser, newRole: string) {
  if (!selectedCommunity.value) return
  try {
    await updateUserRole(selectedCommunity.value.id, user.id, newRole)
    user.role = newRole
    ElMessage.success('角色更新成功')
  } catch (e: any) {
    ElMessage.error(e?.response?.data?.detail || '更新角色失败')
  }
}

onMounted(loadCommunities)
</script>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.page-header h2 { margin: 0; }

.community-card {
  margin-bottom: 20px;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.community-title {
  display: flex;
  align-items: center;
  gap: 8px;
}
.community-title .name {
  font-weight: 600;
  font-size: 16px;
}
.more-icon {
  cursor: pointer;
  color: #909399;
  font-size: 18px;
}
.more-icon:hover {
  color: #409eff;
}
.community-info .slug {
  color: #909399;
  font-size: 13px;
  display: flex;
  align-items: center;
  gap: 4px;
  margin: 0 0 8px;
}
.community-info .desc {
  color: #606266;
  font-size: 14px;
  margin: 0;
  line-height: 1.6;
}

.members-header {
  display: flex;
  gap: 12px;
  align-items: center;
}
</style>
