import { defineStore } from 'pinia'
import { computed } from 'vue'
import { useAuthStore } from './auth'
import { useCommunityStore } from './community'

export const useUserStore = defineStore('user', () => {
  const authStore = useAuthStore()
  const communityStore = useCommunityStore()

  // Check if user is community admin
  // Note: For now, we consider superuser as community admin
  // TODO: Fetch actual community role from backend
  const isCommunityAdmin = computed(() => {
    return authStore.isSuperuser
  })

  const currentUser = computed(() => authStore.user)

  return {
    isCommunityAdmin,
    currentUser
  }
})
