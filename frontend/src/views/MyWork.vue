<template>
  <div class="my-work" v-loading="loading">
    <!-- 页面标题 -->
    <div class="page-title">
      <h2>我的工作</h2>
      <p class="subtitle">查看和管理我负责的所有任务</p>
    </div>

    <!-- 指标卡片 -->
    <div class="metric-cards">
      <div class="metric-card">
        <div class="metric-value">{{ allItems.length }}</div>
        <div class="metric-label">全部任务</div>
      </div>
      <div class="metric-card">
        <div class="metric-value">{{ totalPlanning }}</div>
        <div class="metric-label">计划中</div>
      </div>
      <div class="metric-card highlight-warning">
        <div class="metric-value">{{ totalInProgress }}</div>
        <div class="metric-label">进行中</div>
      </div>
      <div class="metric-card highlight-success">
        <div class="metric-value">{{ totalCompleted }}</div>
        <div class="metric-label">已完成</div>
      </div>
    </div>

    <!-- 筛选栏 -->
    <div class="section-card filter-section">
      <el-radio-group v-model="filterStatus" @change="loadData">
        <el-radio-button value="all">全部</el-radio-button>
        <el-radio-button value="planning">计划中</el-radio-button>
        <el-radio-button value="in_progress">进行中</el-radio-button>
        <el-radio-button value="completed">已完成</el-radio-button>
      </el-radio-group>
      <el-radio-group v-model="filterType" style="margin-left: 16px;">
        <el-radio-button value="all">全部类型</el-radio-button>
        <el-radio-button value="content">内容</el-radio-button>
        <el-radio-button value="meeting">会议</el-radio-button>
      </el-radio-group>
    </div>

    <!-- 任务列表 -->
    <div class="section-card">
      <div class="section-header">
        <h3>任务列表</h3>
        <span class="section-desc">共 {{ filteredItems.length }} 项</span>
      </div>

      <div v-if="filteredItems.length === 0" class="empty-hint">暂无任务</div>

      <div v-else>
        <div
          v-for="item in filteredItems"
          :key="`${item.type}-${item.id}`"
          class="list-item clickable"
          @click="goToDetail(item)"
        >
          <div class="item-left">
            <span class="stat-dot" :class="statusDotClass(item.work_status)"></span>
            <div class="item-content">
              <div class="item-title-row">
                <span class="count-badge" :class="item.type === 'content' ? 'content-badge' : 'meeting-badge'">
                  {{ item.type === 'content' ? '内容' : '会议' }}
                </span>
                <span class="item-title">{{ item.title }}</span>
              </div>
              <div class="item-meta">
                <span>{{ item.creator_name || '未知' }}</span>
                <span>{{ item.assignee_count }} 人参与</span>
                <span>{{ formatDate(item.updated_at) }}</span>
              </div>
            </div>
          </div>
          <el-select
            v-model="item.work_status"
            @change="updateStatus(item)"
            @click.stop
            size="small"
            style="width: 110px; flex-shrink: 0;"
          >
            <el-option label="计划中" value="planning" />
            <el-option label="进行中" value="in_progress" />
            <el-option label="已完成" value="completed" />
          </el-select>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import axios from '../api'

const router = useRouter()

interface Item {
  id: number
  type: string
  title: string
  work_status: string
  creator_name?: string
  assignee_count: number
  updated_at: string
}

const loading = ref(false)
const data = ref<any>(null)
const filterStatus = ref('all')
const filterType = ref('all')

const allItems = computed(() => {
  if (!data.value) return []
  return [...data.value.contents, ...data.value.meetings]
})

const filteredItems = computed(() => {
  let items = allItems.value
  if (filterStatus.value !== 'all') items = items.filter((i: Item) => i.work_status === filterStatus.value)
  if (filterType.value !== 'all') items = items.filter((i: Item) => i.type === filterType.value)
  return items
})

const totalPlanning = computed(() =>
  data.value ? (data.value.content_stats.planning + data.value.meeting_stats.planning) : 0
)
const totalInProgress = computed(() =>
  data.value ? (data.value.content_stats.in_progress + data.value.meeting_stats.in_progress) : 0
)
const totalCompleted = computed(() =>
  data.value ? (data.value.content_stats.completed + data.value.meeting_stats.completed) : 0
)

const formatDate = (d: string) => new Date(d).toLocaleDateString('zh-CN')

function statusDotClass(status: string) {
  const map: Record<string, string> = { planning: 'planning', in_progress: 'in-progress', completed: 'completed' }
  return map[status] || 'planning'
}

const loadData = async () => {
  loading.value = true
  try {
    const { data: res } = await axios.get('/users/me/dashboard')
    data.value = res
  } catch (error: any) {
    ElMessage.error('加载失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    loading.value = false
  }
}

const updateStatus = async (item: Item) => {
  const url = `/users/me/${item.type === 'content' ? 'contents' : 'meetings'}/${item.id}/work-status`
  try {
    await axios.patch(url, { work_status: item.work_status })
    ElMessage.success('状态已更新')
    loadData()
  } catch (error: any) {
    ElMessage.error('更新失败: ' + (error.response?.data?.detail || error.message))
    loadData()
  }
}

const goToDetail = (item: Item) => {
  if (item.type === 'content') {
    router.push(`/contents/${item.id}/edit`)
  } else if (item.type === 'meeting') {
    router.push(`/meetings/${item.id}`)
  }
}

onMounted(() => loadData())
</script>

<style scoped>
.my-work {
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
}

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
.metric-card.highlight-success .metric-value { color: #10b981; }

/* Section Card */
.section-card { background: #fff; border-radius: 12px; padding: 24px; margin-bottom: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.06); border: 1px solid #f0f0f0; }
.section-header { display: flex; align-items: baseline; gap: 12px; margin-bottom: 20px; }
.section-header h3 { margin: 0; font-size: 16px; font-weight: 600; color: #1d2129; }
.section-desc { font-size: 13px; color: #86909c; }

/* Filter Section */
.filter-section { display: flex; align-items: center; padding: 16px 24px; }

/* List Item */
.list-item { display: flex; align-items: center; justify-content: space-between; padding: 14px 0; border-bottom: 1px solid #f5f5f5; }
.list-item:last-child { border-bottom: none; }
.list-item.clickable { cursor: pointer; }
.list-item.clickable:hover { background: #fafbfc; margin: 0 -24px; padding: 14px 24px; border-radius: 8px; }

.item-left { display: flex; align-items: center; gap: 14px; min-width: 0; flex: 1; }

/* Status Dot */
.stat-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.stat-dot.planning { background: #94a3b8; }
.stat-dot.in-progress { background: #f59e0b; }
.stat-dot.completed { background: #10b981; }

.item-content { min-width: 0; flex: 1; }
.item-title-row { display: flex; align-items: center; gap: 8px; margin-bottom: 4px; }
.item-title { font-size: 14px; font-weight: 500; color: #1d2129; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

.item-meta { display: flex; gap: 16px; font-size: 13px; color: #86909c; }

/* Badges */
.count-badge { display: inline-flex; align-items: center; gap: 3px; font-size: 12px; padding: 2px 8px; border-radius: 10px; font-weight: 500; }
.content-badge { background: #eff6ff; color: #3b82f6; }
.meeting-badge { background: #f0fdf4; color: #22c55e; }

/* Empty */
.empty-hint { color: #c0c4cc; text-align: center; padding: 40px 0; font-size: 14px; }
</style>
