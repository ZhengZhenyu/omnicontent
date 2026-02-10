<template>
  <div class="community-overview">
    <!-- 页面标题 -->
    <div class="page-title-row">
      <div class="page-title">
        <h2>社区总览</h2>
        <p class="subtitle">查看所有社区的运营概况</p>
      </div>
      <el-button v-if="isSuperuser" type="primary" :icon="Plus" @click="$router.push('/communities')">
        管理社区
      </el-button>
    </div>

    <!-- 指标卡片 -->
    <div class="metric-cards">
      <div class="metric-card">
        <div class="metric-value">{{ totalCommunities }}</div>
        <div class="metric-label">社区总数</div>
      </div>
      <div class="metric-card">
        <div class="metric-value">{{ totalContents }}</div>
        <div class="metric-label">内容总数</div>
      </div>
      <div class="metric-card highlight-warning">
        <div class="metric-value">{{ totalCommittees }}</div>
        <div class="metric-label">委员会总数</div>
      </div>
      <div class="metric-card highlight-success">
        <div class="metric-value">{{ totalPublishes }}</div>
        <div class="metric-label">发布总数</div>
      </div>
    </div>

    <!-- 社区表格 -->
    <div class="section-card">
      <div class="section-header">
        <h3>社区列表</h3>
        <el-input
          v-model="searchQuery"
          placeholder="搜索社区名称或标识"
          :prefix-icon="Search"
          style="width: 280px"
          clearable
        />
      </div>

      <el-table :data="filteredCommunities" style="width: 100%" v-loading="loading">
        <el-table-column label="社区" width="300">
          <template #default="{ row }">
            <div class="community-cell">
              <div class="community-avatar">{{ row.name.charAt(0).toUpperCase() }}</div>
              <div class="community-info">
                <div class="community-name">
                  {{ row.name }}
                  <span v-if="!row.is_active" class="status-badge status-disabled">已停用</span>
                </div>
                <div class="community-slug">{{ row.slug }}</div>
              </div>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="委员会" width="100" align="center">
          <template #default="{ row }">
            <span
              class="count-link"
              :class="{ disabled: row.committee_count === 0 }"
              @click="row.committee_count > 0 && viewCommittees(row.id)"
            >
              {{ row.committee_count || 0 }}
            </span>
          </template>
        </el-table-column>
        <el-table-column label="内容数" width="100" align="center">
          <template #default="{ row }">
            <span class="meta-text">{{ row.content_count || 0 }}</span>
          </template>
        </el-table-column>
        <el-table-column label="发布渠道" width="220">
          <template #default="{ row }">
            <div class="channels">
              <span
                v-for="channel in row.channels"
                :key="channel.channel"
                class="count-badge"
                :class="channel.enabled ? 'channel-active' : 'channel-inactive'"
              >
                {{ getChannelLabel(channel.channel) }} ({{ channel.publish_count || 0 }})
              </span>
              <span v-if="!row.channels || row.channels.length === 0" class="empty-text">未配置</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="描述" min-width="250">
          <template #default="{ row }">
            <span class="description">{{ row.description || '暂无描述' }}</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="viewCommunity(row.id)">
              <el-icon><View /></el-icon>
              查看
            </el-button>
            <el-button
              v-if="canManageCommunity(row)"
              size="small"
              @click="manageCommunity(row.id)"
            >
              <el-icon><Setting /></el-icon>
              管理
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
  Plus, Search, View, Setting
} from '@element-plus/icons-vue'
import { useAuthStore } from '../stores/auth'
import { getCommunities } from '../api/community'
import type { Community } from '../stores/auth'
import apiClient from '../api/index'

interface CommunityStats extends Community {
  committee_count?: number
  content_count?: number
  channels?: Array<{
    channel: string
    enabled: boolean
    publish_count?: number
  }>
}

const router = useRouter()
const authStore = useAuthStore()
const isSuperuser = computed(() => authStore.isSuperuser)

const loading = ref(false)
const searchQuery = ref('')
const communities = ref<CommunityStats[]>([])

const filteredCommunities = computed(() => {
  if (!searchQuery.value) return communities.value
  const query = searchQuery.value.toLowerCase()
  return communities.value.filter(c =>
    c.name.toLowerCase().includes(query) ||
    c.slug.toLowerCase().includes(query)
  )
})

const totalCommunities = computed(() => communities.value.length)
const totalCommittees = computed(() =>
  communities.value.reduce((sum, c) => sum + (c.committee_count || 0), 0)
)
const totalContents = computed(() =>
  communities.value.reduce((sum, c) => sum + (c.content_count || 0), 0)
)
const totalPublishes = computed(() => {
  let total = 0
  communities.value.forEach(c => {
    c.channels?.forEach(ch => {
      total += ch.publish_count || 0
    })
  })
  return total
})

const channelLabelMap: Record<string, string> = {
  wechat: '微信',
  hugo: 'Hugo',
  csdn: 'CSDN',
  zhihu: '知乎',
}

function getChannelLabel(channel: string): string {
  return channelLabelMap[channel] || channel
}

function canManageCommunity(community: Community): boolean {
  if (isSuperuser.value) return true
  return community.role === 'admin'
}

function viewCommunity(communityId: number) {
  const community = communities.value.find(c => c.id === communityId)
  if (community) {
    localStorage.setItem('current_community_id', String(communityId))
    router.push('/governance')
  }
}

function viewCommittees(communityId: number) {
  router.push(`/committees?community=${communityId}`)
}

function manageCommunity(communityId: number) {
  router.push('/communities')
}

async function loadCommunities() {
  loading.value = true
  try {
    const communityList = await getCommunities()

    const statsPromises = communityList.map(async (community) => {
      try {
        const committeesRes = await apiClient.get(
          '/committees',
          { headers: { 'X-Community-Id': community.id } }
        )
        const committee_count = committeesRes.data?.length || 0

        const contentsRes = await apiClient.get(
          '/contents',
          { headers: { 'X-Community-Id': community.id } }
        )
        const content_count = contentsRes.data?.length || 0

        const channelsRes = await apiClient.get(
          '/channels',
          { headers: { 'X-Community-Id': community.id } }
        )
        const channels = channelsRes.data || []

        const channelsWithCounts = await Promise.all(
          channels.map(async (channel: any) => {
            try {
              const publishRes = await apiClient.get(
                '/publish/records',
                {
                  params: { channel: channel.channel },
                  headers: { 'X-Community-Id': community.id }
                }
              )
              return {
                ...channel,
                publish_count: publishRes.data?.length || 0
              }
            } catch {
              return { ...channel, publish_count: 0 }
            }
          })
        )

        return {
          ...community,
          committee_count,
          content_count,
          channels: channelsWithCounts
        }
      } catch (error) {
        console.error(`Failed to load stats for community ${community.id}:`, error)
        return {
          ...community,
          committee_count: 0,
          content_count: 0,
          channels: []
        }
      }
    })

    communities.value = await Promise.all(statsPromises)
  } catch (error: any) {
    ElMessage.error(error.message || '加载社区列表失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadCommunities()
})
</script>

<style scoped>
.community-overview {
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
}

/* Page Title Row */
.page-title-row { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 24px; }
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
.section-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px; }
.section-header h3 { margin: 0; font-size: 16px; font-weight: 600; color: #1d2129; }

/* Community Cell */
.community-cell { display: flex; align-items: center; gap: 12px; }
.community-avatar { width: 36px; height: 36px; border-radius: 10px; background: linear-gradient(135deg, #667eea, #764ba2); color: #fff; display: flex; align-items: center; justify-content: center; font-size: 14px; font-weight: 600; flex-shrink: 0; }
.community-info { display: flex; flex-direction: column; }
.community-name { display: flex; align-items: center; gap: 8px; font-size: 14px; font-weight: 500; color: #1d2129; }
.community-slug { font-size: 12px; color: #86909c; }

/* Count Link */
.count-link { font-size: 14px; font-weight: 600; color: #3b82f6; cursor: pointer; }
.count-link:hover { text-decoration: underline; }
.count-link.disabled { color: #86909c; cursor: default; }
.count-link.disabled:hover { text-decoration: none; }

/* Badges */
.count-badge { display: inline-flex; align-items: center; font-size: 12px; padding: 2px 8px; border-radius: 10px; font-weight: 500; margin-right: 4px; margin-bottom: 4px; }
.channel-active { background: #f0fdf4; color: #22c55e; }
.channel-inactive { background: #f7f8fa; color: #86909c; }

.status-badge { display: inline-block; font-size: 12px; padding: 2px 8px; border-radius: 10px; font-weight: 500; }
.status-disabled { background: #fef2f2; color: #ef4444; }

/* Meta */
.meta-text { font-size: 14px; color: #4e5969; }
.empty-text { color: #c0c4cc; font-size: 12px; }
.description { color: #4e5969; font-size: 13px; line-height: 1.6; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }

/* Channels */
.channels { display: flex; flex-wrap: wrap; }
</style>
