import apiClient from './index'

export interface ChannelConfig {
  id: number
  channel: string
  config: Record<string, string>
  enabled: boolean
}

export interface ChannelConfigCreate {
  channel: string
  config: Record<string, string>
  enabled: boolean
}

export interface ChannelConfigUpdate {
  config?: Record<string, string>
  enabled?: boolean
}

export async function listChannels(): Promise<ChannelConfig[]> {
  const { data } = await apiClient.get<ChannelConfig[]>('/channels')
  return data
}

export async function createChannel(payload: ChannelConfigCreate): Promise<ChannelConfig> {
  const { data } = await apiClient.post<ChannelConfig>('/channels', payload)
  return data
}

export async function updateChannel(
  channelId: number,
  payload: ChannelConfigUpdate
): Promise<ChannelConfig> {
  const { data } = await apiClient.put<ChannelConfig>(`/channels/${channelId}`, payload)
  return data
}

export async function deleteChannel(channelId: number): Promise<void> {
  await apiClient.delete(`/channels/${channelId}`)
}
