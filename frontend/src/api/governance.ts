import request from './request'



























































































































































































































































































































































































































</style>}  flex-wrap: wrap;  gap: 12px;  display: flex;.quick-actions {}  margin-top: 24px;.actions-card {}  font-size: 14px;  color: var(--el-text-color-placeholder);.item-arrow {}  color: var(--el-text-color-secondary);  font-size: 13px;  gap: 8px;  align-items: center;  display: flex;.item-meta {}  margin-bottom: 4px;  color: var(--el-text-color-primary);  font-weight: 500;  font-size: 15px;.item-title {}  flex: 1;.item-content {}  border-radius: 4px;  padding-right: 12px;  padding-left: 12px;  margin: 0 -12px;  background: var(--el-fill-color-light);.list-item:hover {}  border-bottom: none;.list-item:last-child {}  transition: background 0.2s;  cursor: pointer;  border-bottom: 1px solid var(--el-border-color-lighter);  padding: 12px 0;  align-items: center;  display: flex;.list-item {}  font-weight: 600;  align-items: center;  justify-content: space-between;  display: flex;.card-header {}  height: 100%;.section-card {}  margin-bottom: 24px;.content-row {}  color: var(--el-text-color-secondary);  font-size: 14px;.stat-label {}  margin-bottom: 4px;  line-height: 1;  color: var(--el-text-color-primary);  font-weight: 700;  font-size: 28px;.stat-value {}  flex: 1;.stat-content {}  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);.stat-icon.history {}  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);.stat-icon.meeting {}  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);.stat-icon.member {}  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);.stat-icon.committee {}  color: white;  font-size: 28px;  justify-content: center;  align-items: center;  display: flex;  border-radius: 12px;  height: 56px;  width: 56px;.stat-icon {}  padding: 20px;  gap: 16px;  align-items: center;  display: flex;.stat-card :deep(.el-card__body) {}  cursor: default;.stat-card {}  margin-bottom: 24px;.stats-row {}  font-size: 14px;  color: var(--el-text-color-secondary);  margin: 0;.page-header p {}  font-weight: 600;  font-size: 24px;  margin: 0 0 4px 0;.page-header h2 {}  margin-bottom: 24px;.page-header {}  padding: 24px;.governance-overview {<style scoped></script>}  return map[status] || status  }    cancelled: '已取消'    completed: '已完成',    in_progress: '进行中',    scheduled: '已安排',  const map: Record<string, string> = {function getMeetingStatusText(status: string) {}  return map[status] || ''  }    cancelled: 'danger'    completed: 'info',    in_progress: 'success',    scheduled: 'primary',  const map: Record<string, any> = {function getMeetingStatusType(status: string) {}  })    minute: '2-digit'    hour: '2-digit',    day: 'numeric',    month: 'short',  return date.toLocaleString('zh-CN', {  const date = new Date(dateStr)function formatDateTime(dateStr: string) {}  }    loadingMeetings.value = false  } finally {    ElMessage.error(error.message || '加载会议失败')  } catch (error: any) {    upcomingMeetings.value = data    })      limit: 5      end_date: endDate,      start_date: startDate,    const data = await listMeetings({          .split('T')[0]      .toISOString()    const endDate = new Date(now.getTime() + 30 * 24 * 60 * 60 * 1000)    const startDate = now.toISOString().split('T')[0]    const now = new Date()  try {  loadingMeetings.value = trueasync function loadMeetings() {}  }    loadingCommittees.value = false  } finally {    ElMessage.error(error.message || '加载委员会失败')  } catch (error: any) {    committees.value = data.slice(0, 5) // Show top 5    const data = await listCommittees({ is_active: true })  try {  loadingCommittees.value = trueasync function loadCommittees() {}  await Promise.all([loadCommittees(), loadMeetings()])async function loadData() {})  loadData()onMounted(() => {})  }    totalMeetings: upcomingMeetings.value.length    upcomingMeetings: upcoming.length,    memberCount: committees.value.reduce((sum, c) => sum + c.member_count, 0),    committeeCount: committees.value.filter(c => c.is_active).length,  return {    )    m => new Date(m.scheduled_at) > now && m.status === 'scheduled'  const upcoming = upcomingMeetings.value.filter(  const now = new Date()const stats = computed(() => {const upcomingMeetings = ref<Meeting[]>([])const committees = ref<Committee[]>([])const loadingMeetings = ref(false)const loadingCommittees = ref(false)const isAdmin = computed(() => userStore.isCommunityAdmin)const userStore = useUserStore()const router = useRouter()import { useUserStore } from '@/stores/user'import { listCommittees, listMeetings, type Committee, type Meeting } from '@/api/governance'import { ElMessage } from 'element-plus'} from '@element-plus/icons-vue'  Plus  ArrowRight,  Clock,  Calendar,  UserFilled,  OfficeBuilding,import {import { useRouter } from 'vue-router'import { ref, onMounted, computed } from 'vue'<script setup lang="ts"></template>  </div>    </el-card>      </div>        </el-button>          创建会议          <el-icon><Plus /></el-icon>        <el-button type="success" @click="$router.push('/meetings?action=create')">        </el-button>          创建委员会          <el-icon><Plus /></el-icon>        <el-button type="primary" @click="$router.push('/committees?action=create')">      <div class="quick-actions">      </template>        <span>快捷操作</span>      <template #header>    <el-card v-if="isAdmin" class="actions-card">    <!-- Quick Actions -->    </el-row>      </el-col>        </el-card>          </div>            <el-empty v-if="upcomingMeetings.length === 0" description="暂无即将召开的会议" :image-size="80" />            </div>              <el-icon class="item-arrow"><ArrowRight /></el-icon>              </div>                </div>                  </el-tag>                    {{ getMeetingStatusText(meeting.status) }}                  <el-tag :type="getMeetingStatusType(meeting.status)" size="small">                  <span>{{ formatDateTime(meeting.scheduled_at) }}</span>                <div class="item-meta">                <div class="item-title">{{ meeting.title }}</div>              <div class="item-content">            >              @click="$router.push(`/meetings/${meeting.id}`)"              class="list-item"              :key="meeting.id"              v-for="meeting in upcomingMeetings"            <div          <div v-loading="loadingMeetings">          </template>            </div>              </el-button>                <el-icon><ArrowRight /></el-icon>                查看日历              <el-button type="primary" link @click="$router.push('/meetings')">              <span>近期会议</span>            <div class="card-header">          <template #header>        <el-card class="section-card">      <el-col :xs="24" :md="12">      <!-- Upcoming Meetings Section -->      </el-col>        </el-card>          </div>            <el-empty v-if="committees.length === 0" description="暂无委员会" :image-size="80" />            </div>              <el-icon class="item-arrow"><ArrowRight /></el-icon>              </div>                </div>                  <el-tag v-if="!committee.is_active" type="info" size="small">已归档</el-tag>                  <span>{{ committee.member_count }} 名成员</span>                <div class="item-meta">                <div class="item-title">{{ committee.name }}</div>              <div class="item-content">            >              @click="$router.push(`/committees/${committee.id}`)"              class="list-item"              :key="committee.id"              v-for="committee in committees"            <div          <div v-loading="loadingCommittees">          </template>            </div>              </el-button>                <el-icon><ArrowRight /></el-icon>                查看全部              <el-button type="primary" link @click="$router.push('/committees')">              <span>委员会</span>            <div class="card-header">          <template #header>        <el-card class="section-card">      <el-col :xs="24" :md="12">      <!-- Committees Section -->    <el-row :gutter="24" class="content-row">    </el-row>      </el-col>        </el-card>          </div>            <div class="stat-label">历史会议</div>            <div class="stat-value">{{ stats.totalMeetings }}</div>          <div class="stat-content">          </div>            <el-icon><Clock /></el-icon>          <div class="stat-icon history">        <el-card class="stat-card">      <el-col :xs="24" :sm="12" :md="6">      </el-col>        </el-card>          </div>            <div class="stat-label">即将召开</div>            <div class="stat-value">{{ stats.upcomingMeetings }}</div>          <div class="stat-content">          </div>            <el-icon><Calendar /></el-icon>          <div class="stat-icon meeting">        <el-card class="stat-card">      <el-col :xs="24" :sm="12" :md="6">      </el-col>        </el-card>          </div>            <div class="stat-label">成员</div>            <div class="stat-value">{{ stats.memberCount }}</div>          <div class="stat-content">          </div>            <el-icon><UserFilled /></el-icon>          <div class="stat-icon member">        <el-card class="stat-card">      <el-col :xs="24" :sm="12" :md="6">      </el-col>        </el-card>          </div>            <div class="stat-label">委员会</div>            <div class="stat-value">{{ stats.committeeCount }}</div>          <div class="stat-content">          </div>            <el-icon><OfficeBuilding /></el-icon>          <div class="stat-icon committee">        <el-card class="stat-card">      <el-col :xs="24" :sm="12" :md="6">    <el-row :gutter="24" class="stats-row">    </div>      <p>管理委员会、会议和成员</p>      <h2>社区治理</h2>    <div class="page-header">// ==================== Types ====================

export interface Committee {
  id: number
  community_id: number
  name: string
  slug: string
  description?: string
  is_active: boolean
  meeting_frequency?: string
  notification_email?: string
  notification_wechat?: string
  established_at?: string
  member_count: number
  created_at: string
  updated_at: string
}

export interface CommitteeMember {
  id: number
  committee_id: number
  name: string
  email?: string
  phone?: string
  wechat?: string
  organization?: string
  roles: string[]
  term_start?: string
  term_end?: string
  is_active: boolean
  bio?: string
  avatar_url?: string
  joined_at: string
  created_at: string
}

export interface CommitteeWithMembers extends Committee {
  members: CommitteeMember[]
}

export interface CommitteeCreate {
  name: string
  slug: string
  description?: string
  meeting_frequency?: string
  notification_email?: string
  notification_wechat?: string
  established_at?: string
}

export interface CommitteeUpdate {
  name?: string
  description?: string
  is_active?: boolean
  meeting_frequency?: string
  notification_email?: string
  notification_wechat?: string
  established_at?: string
}

export interface CommitteeMemberCreate {
  name: string
  email?: string
  phone?: string
  wechat?: string
  organization?: string
  roles?: string[]
  term_start?: string
  term_end?: string
  bio?: string
}

export interface CommitteeMemberUpdate {
  name?: string
  email?: string
  phone?: string
  wechat?: string
  organization?: string
  roles?: string[]
  term_start?: string
  term_end?: string
  is_active?: boolean
  bio?: string
  avatar_url?: string
}

// ==================== Committee APIs ====================

export function listCommittees(params?: { is_active?: boolean }) {
  return request<Committee[]>({
    url: '/api/committees',
    method: 'get',
    params
  })
}

export function createCommittee(data: CommitteeCreate) {
  return request<Committee>({
    url: '/api/committees',
    method: 'post',
    data
  })
}

export function getCommittee(id: number) {
  return request<CommitteeWithMembers>({
    url: `/api/committees/${id}`,
    method: 'get'
  })
}

export function updateCommittee(id: number, data: CommitteeUpdate) {
  return request<Committee>({
    url: `/api/committees/${id}`,
    method: 'put',
    data
  })
}

export function deleteCommittee(id: number) {
  return request<void>({
    url: `/api/committees/${id}`,
    method: 'delete'
  })
}

// ==================== Committee Member APIs ====================

export function listCommitteeMembers(committeeId: number, params?: { is_active?: boolean }) {
  return request<CommitteeMember[]>({
    url: `/api/committees/${committeeId}/members`,
    method: 'get',
    params
  })
}

export function createCommitteeMember(committeeId: number, data: CommitteeMemberCreate) {
  return request<CommitteeMember>({
    url: `/api/committees/${committeeId}/members`,
    method: 'post',
    data
  })
}

export function updateCommitteeMember(
  committeeId: number,
  memberId: number,
  data: CommitteeMemberUpdate
) {
  return request<CommitteeMember>({
    url: `/api/committees/${committeeId}/members/${memberId}`,
    method: 'put',
    data
  })
}

export function deleteCommitteeMember(committeeId: number, memberId: number) {
  return request<void>({
    url: `/api/committees/${committeeId}/members/${memberId}`,
    method: 'delete'
  })
}

// ==================== Meeting Types ====================

export interface Meeting {
  id: number
  committee_id: number
  community_id: number
  title: string
  description?: string
  scheduled_at: string
  duration: number
  location_type?: string
  location?: string
  status: string
  reminder_sent: boolean
  created_by_user_id?: number
  created_at: string
  updated_at: string
}

export interface MeetingDetail extends Meeting {
  agenda?: string
  minutes?: string
  attachments?: any[]
  committee_name?: string
}

export interface MeetingCreate {
  committee_id: number
  title: string
  description?: string
  scheduled_at: string
  duration?: number
  location_type?: string
  location?: string
  agenda?: string
  reminder_before_hours?: number
}

export interface MeetingUpdate {
  title?: string
  description?: string
  scheduled_at?: string
  duration?: number
  location_type?: string
  location?: string
  status?: string
  agenda?: string
  reminder_before_hours?: number
}

export interface MeetingReminder {
  id: number
  meeting_id: number
  reminder_type: string
  scheduled_at: string
  sent_at?: string
  notification_channels: string[]
  status: string
  error_message?: string
  created_at: string
}

// ==================== Meeting APIs ====================

export function listMeetings(params?: {
  committee_id?: number
  start_date?: string
  end_date?: string
  skip?: number
  limit?: number
}) {
  return request<Meeting[]>({
    url: '/api/meetings',
    method: 'get',
    params
  })
}

export function createMeeting(data: MeetingCreate) {
  return request<Meeting>({
    url: '/api/meetings',
    method: 'post',
    data
  })
}

export function getMeeting(id: number) {
  return request<MeetingDetail>({
    url: `/api/meetings/${id}`,
    method: 'get'
  })
}

export function updateMeeting(id: number, data: MeetingUpdate) {
  return request<Meeting>({
    url: `/api/meetings/${id}`,
    method: 'put',
    data
  })
}

export function deleteMeeting(id: number) {
  return request<void>({
    url: `/api/meetings/${id}`,
    method: 'delete'
  })
}

export function updateMeetingMinutes(id: number, minutes: string) {
  return request<MeetingDetail>({
    url: `/api/meetings/${id}/minutes`,
    method: 'put',
    data: { minutes }
  })
}

export function getMeetingMinutes(id: number) {
  return request<{ minutes: string }>({
    url: `/api/meetings/${id}/minutes`,
    method: 'get'
  })
}

export function listMeetingReminders(meetingId: number) {
  return request<MeetingReminder[]>({
    url: `/api/meetings/${meetingId}/reminders`,
    method: 'get'
  })
}

export function createMeetingReminder(meetingId: number, reminderType: string) {
  return request<MeetingReminder>({
    url: `/api/meetings/${meetingId}/reminders`,
    method: 'post',
    data: { reminder_type: reminderType }
  })
}
