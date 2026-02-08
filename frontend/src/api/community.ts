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
  user_id: number
  username: string
  email: string
  role: string
  joined_at: string
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
