<template>
  <div class="dashboard">
    <!-- No communities: empty state -->
    <div v-if="authStore.communities.length === 0" class="empty-state">
      <el-empty description="您还没有加入任何社区" :image-size="200">
        <template v-if="authStore.isSuperuser">
          <p class="empty-tip">作为超级管理员，您可以创建社区开始使用</p>
          <el-button type="primary" @click="$router.push('/communities')">创建社区</el-button>
        </template>
        <template v-else>
          <p class="empty-tip">请联系管理员将您添加到社区</p>
        </template>
      </el-empty>
    </div>

    <!-- Has communities but none selected -->
    <div v-else-if="!communityStore.currentCommunityId" class="empty-state">
      <el-empty description="请先选择一个社区" :image-size="150">
        <p class="empty-tip">使用顶部的社区切换器选择要管理的社区</p>
      </el-empty>
    </div>

    <!-- Normal dashboard -->
    <div v-else>
      <div class="page-title">
        <h2>仪表板</h2>
        <p class="subtitle">社区内容与发布数据概览</p>
      </div>

      <!-- 指标卡片 -->
      <div class="metric-cards">
        <div class="metric-card">
          <div class="metric-value">{{ overview.total_contents }}</div>
          <div class="metric-label">内容总数</div>
        </div>
        <div class="metric-card highlight-success">
          <div class="metric-value">{{ overview.total_published }}</div>
          <div class="metric-label">已发布</div>
        </div>
        <div class="metric-card">
          <div class="metric-value">{{ Object.keys(overview.channels).length }}</div>
          <div class="metric-label">渠道覆盖</div>
        </div>
        <div class="metric-card">
          <div class="metric-value">{{ recentContents.length }}</div>
          <div class="metric-label">最近更新</div>
        </div>
      </div>

      <!-- 内容区域 -->
      <div class="content-grid">
        <!-- 各渠道发布统计 -->
        <div class="section-card">
          <div class="section-header">
            <h3>各渠道发布统计</h3>
            <span class="section-desc">按发布渠道分类</span>
          </div>
          <div v-if="Object.keys(overview.channels).length === 0" class="empty-hint">
            <span>暂无发布记录</span>
          </div>
          <div v-else>
            <div v-for="(count, channel) in overview.channels" :key="channel" class="list-item">
              <div class="channel-info">
                <span class="channel-dot" :class="channelDotClass(channel as string)"></span>
                <span class="item-title">{{ channelLabel(channel as string) }}</span>
              </div>
              <span class="count-badge content-badge">{{ count }} 篇</span>
            </div>
          </div>
        </div>

        <!-- 最近内容 -->
        <div class="section-card">
          <div class="section-header">
            <h3>最近内容</h3>
            <span class="section-desc">最新 5 条内容</span>
          </div>
          <div v-if="recentContents.length === 0" class="empty-hint">
            <span>暂无内容</span>
          </div>
          <div v-else>
            <div v-for="item in recentContents" :key="item.id" class="list-item">
              <router-link :to="`/contents/${item.id}/edit`" class="item-title link">{{ item.title }}</router-link>
              <span class="status-tag" :class="statusClass(item.status)">{{ statusLabel(item.status) }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { fetchContents, type ContentListItem } from '../api/content'
import { getAnalyticsOverview, type AnalyticsOverview } from '../api/publish'
import { getUserInfo } from '../api/auth'
import { useAuthStore } from '../stores/auth'
import { useCommunityStore } from '../stores/community'

const authStore = useAuthStore()
const communityStore = useCommunityStore()

const overview = ref<AnalyticsOverview>({ total_contents: 0, total_published: 0, channels: {} })
const recentContents = ref<ContentListItem[]>([])

onMounted(async () => {
  if (!authStore.user) {
    try {
      const userInfo = await getUserInfo()
      authStore.setUser(userInfo.user)
      authStore.setCommunities(userInfo.communities)
    } catch (error) {
      console.error('Failed to fetch user info:', error)
    }
  }

  if (communityStore.currentCommunityId) {
    await loadDashboardData()
  }
})

watch(
  () => communityStore.currentCommunityId,
  async (newId) => {
    if (newId) {
      await loadDashboardData()
    }
  }
)

async function loadDashboardData() {
  try {
    overview.value = await getAnalyticsOverview()
  } catch { /* empty */ }
  try {
    const res = await fetchContents({ page: 1, page_size: 5 })
    recentContents.value = res.items
  } catch { /* empty */ }
}

function channelLabel(ch: string) {
  const map: Record<string, string> = { wechat: '微信公众号', hugo: 'Hugo 博客', csdn: 'CSDN', zhihu: '知乎' }
  return map[ch] || ch
}

function channelDotClass(ch: string) {
  const map: Record<string, string> = { wechat: 'dot-success', hugo: 'dot-primary', csdn: 'dot-warning', zhihu: 'dot-info' }
  return map[ch] || 'dot-primary'
}

function statusLabel(s: string) {
  const map: Record<string, string> = { draft: '草稿', reviewing: '审核中', approved: '已通过', published: '已发布' }
  return map[s] || s
}

function statusClass(s: string) {
  const map: Record<string, string> = { draft: 'status-planning', reviewing: 'status-in-progress', approved: 'status-completed', published: 'status-primary' }
  return map[s] || 'status-planning'
}
</script>

<style scoped>
.dashboard {
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
.metric-card.highlight-success .metric-value { color: #10b981; }

/* Content Grid */
.content-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; }

/* Section Card */
.section-card { background: #fff; border-radius: 12px; padding: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.06); border: 1px solid #f0f0f0; }
.section-header { display: flex; align-items: baseline; gap: 12px; margin-bottom: 20px; }
.section-header h3 { margin: 0; font-size: 16px; font-weight: 600; color: #1d2129; }
.section-desc { font-size: 13px; color: #86909c; }

/* List Item */
.list-item { display: flex; align-items: center; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid #f5f5f5; }
.list-item:last-child { border-bottom: none; }

.channel-info { display: flex; align-items: center; gap: 10px; }
.channel-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.channel-dot.dot-success { background: #10b981; }
.channel-dot.dot-primary { background: #3b82f6; }
.channel-dot.dot-warning { background: #f59e0b; }
.channel-dot.dot-info { background: #94a3b8; }

.item-title { font-size: 14px; font-weight: 500; color: #4e5969; }
.item-title.link { text-decoration: none; cursor: pointer; }
.item-title.link:hover { color: #3b82f6; }

/* Count Badge */
.count-badge { display: inline-flex; align-items: center; gap: 3px; font-size: 12px; padding: 2px 8px; border-radius: 10px; font-weight: 500; }
.content-badge { background: #eff6ff; color: #3b82f6; }

/* Status Tag */
.status-tag { display: inline-block; font-size: 12px; padding: 2px 8px; border-radius: 10px; font-weight: 500; }
.status-planning { background: #f7f8fa; color: #94a3b8; }
.status-in-progress { background: #fef3c7; color: #d97706; }
.status-completed { background: #f0fdf4; color: #22c55e; }
.status-primary { background: #eff6ff; color: #3b82f6; }

/* Empty States */
.empty-hint { color: #c0c4cc; text-align: center; padding: 40px 0; font-size: 14px; }
.empty-state { display: flex; justify-content: center; align-items: center; min-height: 400px; }
.empty-tip { color: #86909c; font-size: 14px; margin: 8px 0 16px; }
</style>
