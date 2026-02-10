<template>
  <div class="governance-overview">
    <div v-if="!communityStore.currentCommunityId" class="empty-state">
      <el-empty description="请先选择一个社区" :image-size="150">
        <p class="empty-tip">使用顶部的社区切换器选择要管理的社区</p>
      </el-empty>
    </div>

    <template v-else>
      <!-- 页面标题 -->
      <div class="page-title">
        <h2>社区治理</h2>
        <p class="subtitle">管理委员会、会议和成员</p>
      </div>

      <!-- 指标卡片 -->
      <div class="metric-cards">
        <div class="metric-card">
          <div class="metric-value">{{ stats.committeeCount }}</div>
          <div class="metric-label">委员会</div>
        </div>
        <div class="metric-card">
          <div class="metric-value">{{ stats.memberCount }}</div>
          <div class="metric-label">成员</div>
        </div>
        <div class="metric-card highlight-warning">
          <div class="metric-value">{{ stats.upcomingMeetings }}</div>
          <div class="metric-label">即将召开</div>
        </div>
        <div class="metric-card">
          <div class="metric-value">{{ stats.totalMeetings }}</div>
          <div class="metric-label">历史会议</div>
        </div>
      </div>

      <!-- 双列内容 -->
      <div class="content-grid">
        <!-- 委员会列表 -->
        <div class="section-card">
          <div class="section-header">
            <h3>委员会</h3>
            <span class="section-link" @click="$router.push('/committees')">查看全部 →</span>
          </div>

          <div v-loading="loadingCommittees">
            <div
              v-for="committee in committees"
              :key="committee.id"
              class="list-item clickable"
              @click="$router.push('/committees/' + committee.id)"
            >
              <div class="item-left">
                <div class="item-avatar committee-avatar">
                  {{ committee.name.charAt(0).toUpperCase() }}
                </div>
                <div class="item-content">
                  <span class="item-title">{{ committee.name }}</span>
                  <div class="item-meta">
                    <span>{{ committee.member_count }} 名成员</span>
                    <span v-if="!committee.is_active" class="status-tag status-planning">已归档</span>
                  </div>
                </div>
              </div>
              <span class="item-arrow">›</span>
            </div>
            <div v-if="committees.length === 0" class="empty-hint">暂无委员会</div>
          </div>
        </div>

        <!-- 近期会议 -->
        <div class="section-card">
          <div class="section-header">
            <h3>近期会议</h3>
            <span class="section-link" @click="$router.push('/meetings')">查看日历 →</span>
          </div>

          <div v-loading="loadingMeetings">
            <div
              v-for="meeting in upcomingMeetings"
              :key="meeting.id"
              class="list-item clickable"
              @click="$router.push('/meetings/' + meeting.id)"
            >
              <div class="item-left">
                <span class="stat-dot" :class="meetingDotClass(meeting.status)"></span>
                <div class="item-content">
                  <span class="item-title">{{ meeting.title }}</span>
                  <div class="item-meta">
                    <span>{{ formatDateTime(meeting.scheduled_at) }}</span>
                    <span class="status-tag" :class="meetingStatusClass(meeting.status)">
                      {{ getMeetingStatusText(meeting.status) }}
                    </span>
                  </div>
                </div>
              </div>
              <span class="item-arrow">›</span>
            </div>
            <div v-if="upcomingMeetings.length === 0" class="empty-hint">暂无即将召开的会议</div>
          </div>
        </div>
      </div>

      <!-- 快捷操作 -->
      <div v-if="isAdmin" class="section-card">
        <div class="section-header">
          <h3>快捷操作</h3>
        </div>
        <div class="quick-actions">
          <el-button type="primary" @click="$router.push('/committees?action=create')">
            <el-icon><Plus /></el-icon>
            创建委员会
          </el-button>
          <el-button type="success" @click="$router.push('/meetings?action=create')">
            <el-icon><Plus /></el-icon>
            创建会议
          </el-button>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { Plus } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { listCommittees, listMeetings, type Committee, type Meeting } from '@/api/governance'
import { useUserStore } from '@/stores/user'
import { useCommunityStore } from '@/stores/community'

const router = useRouter()
const userStore = useUserStore()
const communityStore = useCommunityStore()
const isAdmin = computed(() => userStore.isCommunityAdmin)
const loadingCommittees = ref(false)
const loadingMeetings = ref(false)
const committees = ref<Committee[]>([])
const upcomingMeetings = ref<Meeting[]>([])

const stats = computed(() => {
  const now = new Date()
  const upcoming = upcomingMeetings.value.filter(
    m => new Date(m.scheduled_at) > now && m.status === 'scheduled'
  )
  return {
    committeeCount: committees.value.filter(c => c.is_active).length,
    memberCount: committees.value.reduce((sum, c) => sum + c.member_count, 0),
    upcomingMeetings: upcoming.length,
    totalMeetings: upcomingMeetings.value.length
  }
})

onMounted(() => {
  if (communityStore.currentCommunityId) {
    loadData()
  }
})

watch(
  () => communityStore.currentCommunityId,
  (newId) => {
    if (newId) {
      loadData()
    }
  }
)

async function loadData() {
  await Promise.all([loadCommittees(), loadMeetings()])
}

async function loadCommittees() {
  loadingCommittees.value = true
  try {
    const data = await listCommittees({ is_active: true })
    committees.value = data.slice(0, 5)
  } catch (error: any) {
    ElMessage.error(error.message || '加载委员会失败')
  } finally {
    loadingCommittees.value = false
  }
}

async function loadMeetings() {
  loadingMeetings.value = true
  try {
    const now = new Date()
    const startDate = now.toISOString().split('T')[0]
    const endDate = new Date(now.getTime() + 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0]
    const data = await listMeetings({ start_date: startDate, end_date: endDate, limit: 5 })
    upcomingMeetings.value = data
  } catch (error: any) {
    ElMessage.error(error.message || '加载会议失败')
  } finally {
    loadingMeetings.value = false
  }
}

function formatDateTime(dateStr: string) {
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })
}

function meetingDotClass(status: string) {
  const map: Record<string, string> = { scheduled: 'planning', in_progress: 'in-progress', completed: 'completed', cancelled: 'completed' }
  return map[status] || 'planning'
}

function meetingStatusClass(status: string) {
  const map: Record<string, string> = { scheduled: 'status-primary', in_progress: 'status-in-progress', completed: 'status-completed', cancelled: 'status-planning' }
  return map[status] || 'status-planning'
}

function getMeetingStatusText(status: string) {
  const map: Record<string, string> = { scheduled: '已安排', in_progress: '进行中', completed: '已完成', cancelled: '已取消' }
  return map[status] || status
}
</script>

<style scoped>
.governance-overview {
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
}

/* Empty State */
.empty-state { display: flex; justify-content: center; align-items: center; min-height: 400px; }
.empty-tip { color: #86909c; font-size: 14px; margin: 8px 0 16px; }

/* Page Title */
.page-title { margin-bottom: 24px; }
.page-title h2 { margin: 0 0 4px; font-size: 22px; font-weight: 600; color: #1d2129; }
.page-title .subtitle { margin: 0; color: #86909c; font-size: 14px; }

/* Metric Cards */
.metric-cards { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 28px; }
.metric-card { background: #fff; border-radius: 12px; padding: 20px 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.06); border: 1px solid #f0f0f0; }
.metric-value { font-size: 32px; font-weight: 700; color: #1d2129; line-height: 1.2; }
.metric-label { font-size: 13px; color: #86909c; margin-top: 4px; }
.metric-card.highlight-warning .metric-value { color: #f59e0b; }

/* Content Grid */
.content-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin-bottom: 20px; }

/* Section Card */
.section-card { background: #fff; border-radius: 12px; padding: 24px; margin-bottom: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.06); border: 1px solid #f0f0f0; }
.section-header { display: flex; align-items: baseline; justify-content: space-between; margin-bottom: 20px; }
.section-header h3 { margin: 0; font-size: 16px; font-weight: 600; color: #1d2129; }
.section-link { font-size: 13px; color: #3b82f6; cursor: pointer; font-weight: 500; }
.section-link:hover { text-decoration: underline; }

/* List Item */
.list-item { display: flex; align-items: center; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid #f5f5f5; }
.list-item:last-child { border-bottom: none; }
.list-item.clickable { cursor: pointer; }
.list-item.clickable:hover { background: #fafbfc; margin: 0 -24px; padding: 12px 24px; border-radius: 8px; }

.item-left { display: flex; align-items: center; gap: 12px; min-width: 0; flex: 1; }

.item-avatar { width: 36px; height: 36px; border-radius: 10px; color: #fff; display: flex; align-items: center; justify-content: center; font-size: 14px; font-weight: 600; flex-shrink: 0; }
.committee-avatar { background: linear-gradient(135deg, #667eea, #764ba2); }

.item-content { min-width: 0; flex: 1; }
.item-title { font-size: 14px; font-weight: 500; color: #1d2129; }
.item-meta { display: flex; align-items: center; gap: 8px; font-size: 13px; color: #86909c; margin-top: 2px; }

.item-arrow { color: #c0c4cc; font-size: 18px; font-weight: 300; }

/* Status Dot */
.stat-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.stat-dot.planning { background: #94a3b8; }
.stat-dot.in-progress { background: #f59e0b; }
.stat-dot.completed { background: #10b981; }

/* Status Tag */
.status-tag { display: inline-block; font-size: 12px; padding: 2px 8px; border-radius: 10px; font-weight: 500; }
.status-planning { background: #f7f8fa; color: #94a3b8; }
.status-in-progress { background: #fef3c7; color: #d97706; }
.status-completed { background: #f0fdf4; color: #22c55e; }
.status-primary { background: #eff6ff; color: #3b82f6; }

/* Quick Actions */
.quick-actions { display: flex; gap: 12px; flex-wrap: wrap; }

/* Empty */
.empty-hint { color: #c0c4cc; text-align: center; padding: 40px 0; font-size: 14px; }
</style>
