import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useCommunityStore = defineStore('community', () => {
  // State
  const currentCommunityId = ref<number | null>(
    localStorage.getItem('current_community_id')
      ? Number(localStorage.getItem('current_community_id'))
      : null
  )

  // Computed
  const hasSelectedCommunity = computed(() => currentCommunityId.value !== null)

  // Actions
  function setCommunity(communityId: number) {
    currentCommunityId.value = communityId
    localStorage.setItem('current_community_id', String(communityId))
  }

  function clearCommunity() {
    currentCommunityId.value = null
    localStorage.removeItem('current_community_id')
  }

  // Initialize from localStorage on store creation
  function initialize() {
    const storedId = localStorage.getItem('current_community_id')
    if (storedId) {
      currentCommunityId.value = Number(storedId)
    }
  }

  // Initialize immediately
  initialize()

  return {
    // State
    currentCommunityId,
    // Computed
    hasSelectedCommunity,
    // Actions
    setCommunity,
    clearCommunity,
    initialize,
  }
})
