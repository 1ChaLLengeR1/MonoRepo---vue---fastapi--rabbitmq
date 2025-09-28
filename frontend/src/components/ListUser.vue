<template>
  <div class="users-list-container">
    <div class="header">
      <h2 class="title">Lista użytkowników</h2>
      <button
        @click="handleRefresh"
        class="refresh-button"
        :disabled="isLoading"
      >
        <span class="refresh-icon" :class="{ spinning: isLoading }">🔄</span>
        {{ isLoading ? "Pobieranie..." : "Odśwież" }}
      </button>
    </div>

    <div class="users-count" v-if="users.length > 0">
      Znaleziono: <strong>{{ users.length }}</strong> użytkowników
    </div>

    <div class="users-grid" v-if="users.length > 0">
      <div class="user-card" v-for="user in users" :key="user.id">
        <div class="user-button-delete">
          <button @click="handlerDeleteUser(user.id)">Usuń</button>
        </div>
        <div class="user-header">
          <div class="user-avatar">
            {{ user.name.charAt(0).toUpperCase()
            }}{{ user.lastname.charAt(0).toUpperCase() }}
          </div>
          <div class="user-basic-info">
            <h3 class="user-name">{{ user.name }} {{ user.lastname }}</h3>
            <p class="user-email">{{ user.email }}</p>
          </div>
        </div>
        <div class="user-details">
          <div class="detail-item">
            <span class="detail-label">Wiek:</span>
            <span class="detail-value">{{ user.age }} lat</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">Miasto:</span>
            <span class="detail-value">{{ user.city }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">ID:</span>
            <span class="detail-value user-id">{{ user.id }}</span>
          </div>
        </div>
      </div>
    </div>

    <div class="empty-state" v-else-if="!isLoading">
      <div class="empty-icon">👤</div>
      <h3>Brak użytkowników</h3>
      <p>Kliknij "Odśwież" aby pobrać dane</p>
    </div>

    <div class="loading-state" v-if="isLoading">
      <div class="spinner"></div>
      <p>Ładowanie użytkowników...</p>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";

// types
import type { user } from "@/types/global";

// apis
import { apiCollectionUsers } from "@/api/get";
import { apiDeleteUser } from "@/api/delete";

export default defineComponent({
  setup() {
    const users = ref<user[]>([]);
    const isLoading = ref(false);

    const handleRefresh = async () => {
      isLoading.value = true;

      try {
        const response = await apiCollectionUsers();
        if (response.isValid) {
          users.value = response.users as user[];
        }
      } catch (error) {
        console.error("Błąd podczas pobierania użytkowników:", error);
      } finally {
        isLoading.value = false;
      }
    };

    const handlerDeleteUser = async (userId: string) => {
      const response = await apiDeleteUser(userId);
      if (response.isValid) {
        await new Promise((res) => setTimeout(res, 1000));
        await handleRefresh();
      }
    };

    return {
      users,
      isLoading,
      handleRefresh,
      handlerDeleteUser,
    };
  },
});
</script>

<style scoped lang="scss">
* {
  box-sizing: border-box;
}

.users-list-container {
  max-width: 1200px;
  margin: 4px auto;
  padding: 2rem;
  background: white;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #f3f4f6;

  .title {
    font-size: 1.875rem;
    font-weight: 700;
    color: #374151;
    margin: 0;
  }
}

.refresh-button {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 12px;
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);

  &:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
  }

  &:disabled {
    opacity: 0.7;
    cursor: not-allowed;
    transform: none;
  }

  .refresh-icon {
    font-size: 1.2rem;
    transition: transform 0.3s ease;

    &.spinning {
      animation: spin 1s linear infinite;
    }
  }
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.users-count {
  background: #f0f9ff;
  color: #0369a1;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
  font-weight: 500;
  border-left: 4px solid #0ea5e9;
}

.users-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 1.5rem;
}

.user-card {
  background: #fafafa;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 1.5rem;
  transition: all 0.2s ease;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
    border-color: #667eea;
  }
}

.user-button-delete {
  padding-bottom: 4px;

  button {
    background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.5rem 1rem;
    font-size: 0.875rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    box-shadow: 0 2px 8px rgba(239, 68, 68, 0.3);
    min-width: 80px;

    &:hover:not(:disabled) {
      transform: translateY(-1px);
      box-shadow: 0 4px 12px rgba(239, 68, 68, 0.4);
      background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
    }

    &:active:not(:disabled) {
      transform: translateY(0);
      box-shadow: 0 1px 4px rgba(239, 68, 68, 0.4);
    }

    &:disabled {
      opacity: 0.6;
      cursor: not-allowed;
      transform: none;
    }
  }
}

.user-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e5e7eb;
}

.user-avatar {
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1.1rem;
}

.user-basic-info {
  flex: 1;

  .user-name {
    font-size: 1.25rem;
    font-weight: 600;
    color: #374151;
    margin: 0 0 0.25rem 0;
  }

  .user-email {
    color: #6b7280;
    margin: 0;
    font-size: 0.95rem;
  }
}

.user-details {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  align-items: center;

  .detail-label {
    font-weight: 600;
    color: #4b5563;
    font-size: 0.9rem;
  }

  .detail-value {
    color: #374151;
    font-weight: 500;

    &.user-id {
      font-family: monospace;
      font-size: 0.8rem;
      color: #6b7280;
      max-width: 200px;
      overflow: hidden;
      text-overflow: ellipsis;
    }
  }
}

.empty-state {
  text-align: center;
  padding: 3rem 1rem;
  color: #6b7280;

  .empty-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
  }

  h3 {
    margin: 0 0 0.5rem 0;
    color: #374151;
  }

  p {
    margin: 0;
  }
}

.loading-state {
  text-align: center;
  padding: 3rem 1rem;
  color: #6b7280;

  .spinner {
    width: 40px;
    height: 40px;
    border: 4px solid #f3f4f6;
    border-left: 4px solid #667eea;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin: 0 auto 1rem auto;
  }
}

// Responsywność
@media (max-width: 768px) {
  .users-list-container {
    padding: 1rem;
  }

  .header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;

    .title {
      text-align: center;
      font-size: 1.5rem;
    }
  }

  .users-grid {
    grid-template-columns: 1fr;
  }

  .detail-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.25rem;
  }
}
</style>
