import apiClient from './index'
import type { User, Community } from '../stores/auth'

export interface LoginRequest {
  username: string
  password: string
}

export interface LoginResponse {
  access_token: string
  token_type: string
}

export interface UserInfoResponse {
  user: User
  communities: Community[]
}

export async function login(credentials: LoginRequest): Promise<LoginResponse> {
  const formData = new FormData()
  formData.append('username', credentials.username)
  formData.append('password', credentials.password)

  const { data } = await apiClient.post<LoginResponse>('/auth/login', formData, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  })
  return data
}

export async function getUserInfo(): Promise<UserInfoResponse> {
  const { data } = await apiClient.get<UserInfoResponse>('/auth/me')
  return data
}

export async function register(userData: {
  username: string
  email: string
  password: string
  full_name?: string
}): Promise<User> {
  const { data } = await apiClient.post<User>('/auth/register', userData)
  return data
}
