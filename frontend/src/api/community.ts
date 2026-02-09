import apiClient from './index'
import type { Community } from '../stores/auth'

export interface CommunityCreate {
  name: string
  slug: string
  description?: string
  logo_url?: string
}

export interface CommunityUpdate {
  name?: string
  slug?: string
  description?: string
  logo_url?: string
  is_active?: boolean
}

export interface CommunityUser {
  id: number
  username: string
  email: string
  full_name: string
  is_superuser: boolean
  role: string
}

export async function getCommunities(): Promise<Community[]> {
  const { data } = await apiClient.get<Community[]>('/communities')
  return data
}

export async function getCommunity(id: number): Promise<Community> {
  const { data } = await apiClient.get<Community>(`/communities/${id}`)
  return data
}

export async function createCommunity(community: CommunityCreate): Promise<Community> {
  const { data } = await apiClient.post<Community>('/communities', community)
  return data
}

export async function updateCommunity(
  id: number,
  updates: CommunityUpdate
): Promise<Community> {
  const { data } = await apiClient.put<Community>(`/communities/${id}`, updates)
  return data
}

export async function deleteCommunity(id: number): Promise<void> {
  await apiClient.delete(`/communities/${id}`)
}

export async function getCommunityUsers(communityId: number): Promise<CommunityUser[]> {
  const { data } = await apiClient.get<CommunityUser[]>(
    `/communities/${communityId}/users`
  )
  return data
}

export async function addUserToCommunity(
  communityId: number,
  userId: number
): Promise<void> {
  await apiClient.post(`/communities/${communityId}/users`, { user_id: userId })
}

export async function removeUserFromCommunity(
  communityId: number,
  userId: number
): Promise<void> {
  await apiClient.delete(`/communities/${communityId}/users/${userId}`)
}

export async function updateUserRole(
  communityId: number,
  userId: number,
  role: string
): Promise<void> {
  await apiClient.put(`/communities/${communityId}/users/${userId}/role`, null, {
    params: { role },
  })
}
