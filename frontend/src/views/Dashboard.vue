<template>
  <div class="dashboard">
    <h2>仪表板</h2>

    <el-row :gutter="20" class="stats-row">
      <el-col :span="8">
        <el-card shadow="hover">
          <template #header>内容总数</template>
          <div class="stat-number">{{ overview.total_contents }}</div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover">
          <template #header>已发布</template>
          <div class="stat-number">{{ overview.total_published }}</div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover">
          <template #header>渠道覆盖</template>
          <div class="stat-number">{{ Object.keys(overview.channels).length }}</div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="12">
        <el-card>
          <template #header>各渠道发布统计</template>
          <div v-if="Object.keys(overview.channels).length === 0" class="empty-hint">暂无发布记录</div>
          <div v-else>
            <div v-for="(count, channel) in overview.channels" :key="channel" class="channel-stat">
              <el-tag :type="channelTagType(channel as string)">{{ channelLabel(channel as string) }}</el-tag>
              <span class="channel-count">{{ count }} 篇</span>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header>最近内容</template>
          <div v-if="recentContents.length === 0" class="empty-hint">暂无内容</div>
          <div v-for="item in recentContents" :key="item.id" class="recent-item">
            <router-link :to="`/contents/${item.id}/edit`" class="recent-title">{{ item.title }}</router-link>
            <el-tag size="small" :type="statusType(item.status)">{{ statusLabel(item.status) }}</el-tag>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { fetchContents, type ContentListItem } from '../api/content'
import { getAnalyticsOverview, type AnalyticsOverview } from '../api/publish'

const overview = ref<AnalyticsOverview>({ total_contents: 0, total_published: 0, channels: {} })
const recentContents = ref<ContentListItem[]>([])

onMounted(async () => {
  try {
    overview.value = await getAnalyticsOverview()
  } catch { /* empty */ }
  try {
    const res = await fetchContents({ page: 1, page_size: 5 })
    recentContents.value = res.items
  } catch { /* empty */ }
})

function channelLabel(ch: string) {
  const map: Record<string, string> = { wechat: '微信公众号', hugo: 'Hugo 博客', csdn: 'CSDN', zhihu: '知乎' }
  return map[ch] || ch
}

function channelTagType(ch: string) {
  const map: Record<string, string> = { wechat: 'success', hugo: '', csdn: 'warning', zhihu: 'info' }
  return (map[ch] || '') as any
}

function statusLabel(s: string) {
  const map: Record<string, string> = { draft: '草稿', reviewing: '审核中', approved: '已通过', published: '已发布' }
  return map[s] || s
}

function statusType(s: string) {
  const map: Record<string, string> = { draft: 'info', reviewing: 'warning', approved: 'success', published: '' }
  return (map[s] || 'info') as any
}
</script>

<style scoped>
.dashboard h2 { margin: 0 0 20px; }
.stat-number { font-size: 36px; font-weight: bold; color: #409eff; text-align: center; padding: 10px 0; }
.channel-stat { display: flex; align-items: center; gap: 12px; padding: 8px 0; border-bottom: 1px solid #f0f0f0; }
.channel-count { font-size: 16px; font-weight: 500; }
.recent-item { display: flex; align-items: center; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #f0f0f0; }
.recent-title { color: #333; text-decoration: none; }
.recent-title:hover { color: #409eff; }
.empty-hint { color: #999; text-align: center; padding: 20px 0; }
</style>
