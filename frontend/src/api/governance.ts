import request from './request'

// ==================== Types ====================

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
