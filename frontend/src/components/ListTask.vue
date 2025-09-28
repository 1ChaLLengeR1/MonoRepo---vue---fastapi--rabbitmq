<template>
  <div class="tasks-list-container">
    <div class="header">
      <h2 class="title">Lista zadań</h2>
      <button
        @click="handleRefresh"
        class="refresh-button"
        :disabled="isLoading"
      >
        <span class="refresh-icon" :class="{ spinning: isLoading }">🔄</span>
        {{ isLoading ? "Pobieranie..." : "Odśwież" }}
      </button>
    </div>

    <div class="tasks-stats" v-if="tasks.length > 0">
      <div class="stat-item">
        <span class="stat-label">Wszystkich:</span>
        <span class="stat-value total">{{ tasks.length }}</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">Udanych:</span>
        <span class="stat-value success">{{ successCount }}</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">Nieudanych:</span>
        <span class="stat-value failure">{{ failureCount }}</span>
      </div>
    </div>

    <div class="tasks-grid" v-if="tasks.length > 0">
      <div class="task-card" v-for="task in tasks" :key="task.id">
        <div class="task-header">
          <div class="status-badge" :class="task.status">
            <span class="status-icon">{{
              task.status === "success" ? "✅" : "❌"
            }}</span>
            <span class="status-text">{{
              task.status === "success" ? "Sukces" : "Błąd"
            }}</span>
          </div>
          <div class="task-id">
            <span class="id-label">Task ID:</span>
            <span class="id-value">{{ task.task_id }}</span>
          </div>
        </div>

        <div class="task-content">
          <div class="result-section">
            <h4 class="result-title">Rezultat:</h4>
            <p class="result-text" :class="task.status">{{ task.result }}</p>
          </div>

          <div class="task-meta">
            <span class="meta-label">ID zapisku:</span>
            <span class="meta-value">{{ task.id }}</span>
          </div>
        </div>
      </div>
    </div>

    <div class="empty-state" v-else-if="!isLoading">
      <div class="empty-icon">📋</div>
      <h3>Brak zadań</h3>
      <p>Kliknij "Odśwież" aby pobrać dane</p>
    </div>

    <div class="loading-state" v-if="isLoading">
      <div class="spinner"></div>
      <p>Ładowanie zadań...</p>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from "vue";

// types
import type { userTask } from "@/types/global";

// apis
import { apiCollectionTasks } from "@/api/get";

export default defineComponent({
  setup() {
    const tasks = ref<userTask[]>([]);
    const isLoading = ref(false);

    const successCount = computed(
      () => tasks.value.filter((task) => task.status === "success").length
    );

    const failureCount = computed(
      () => tasks.value.filter((task) => task.status === "failure").length
    );

    const handleRefresh = async () => {
      console.log("pobieranie");

      isLoading.value = true;

      try {
        const response = await apiCollectionTasks();
        if (response.isValid) {
          tasks.value = response.users as userTask[];
        }
      } catch (error) {
        console.error("Błąd podczas pobierania zadań:", error);
      } finally {
        isLoading.value = false;
      }
    };

    return {
      tasks,
      isLoading,
      successCount,
      failureCount,
      handleRefresh,
    };
  },
});
</script>

<style scoped lang="scss">
* {
  box-sizing: border-box;
}

.tasks-list-container {
  max-width: 1200px;
  margin: 0 auto;
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

.tasks-stats {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;

  .stat-item {
    background: #f8fafc;
    padding: 1rem;
    border-radius: 8px;
    display: flex;
    flex-direction: column;
    align-items: center;
    min-width: 120px;
    border: 1px solid #e2e8f0;

    .stat-label {
      font-size: 0.875rem;
      color: #64748b;
      margin-bottom: 0.25rem;
    }

    .stat-value {
      font-size: 1.5rem;
      font-weight: 700;

      &.total {
        color: #3b82f6;
      }

      &.success {
        color: #10b981;
      }

      &.failure {
        color: #ef4444;
      }
    }
  }
}

.tasks-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(450px, 1fr));
  gap: 1.5rem;
}

.task-card {
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

.task-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e5e7eb;
}

.status-badge {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.875rem;

  &.success {
    background: #dcfce7;
    color: #166534;
    border: 1px solid #bbf7d0;
  }

  &.failure {
    background: #fef2f2;
    color: #dc2626;
    border: 1px solid #fecaca;
  }

  .status-icon {
    font-size: 1rem;
  }
}

.task-id {
  text-align: right;

  .id-label {
    display: block;
    font-size: 0.75rem;
    color: #6b7280;
    margin-bottom: 0.25rem;
  }

  .id-value {
    font-family: monospace;
    font-size: 0.8rem;
    color: #374151;
    background: #f3f4f6;
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    max-width: 150px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    display: inline-block;
  }
}

.task-content {
  .result-section {
    margin-bottom: 1rem;

    .result-title {
      font-size: 1rem;
      font-weight: 600;
      color: #374151;
      margin: 0 0 0.5rem 0;
    }

    .result-text {
      margin: 0;
      padding: 0.75rem;
      border-radius: 6px;
      font-family: monospace;
      font-size: 0.9rem;
      line-height: 1.4;

      &.success {
        background: #f0fdf4;
        color: #166534;
        border-left: 4px solid #22c55e;
      }

      &.failure {
        background: #fef2f2;
        color: #dc2626;
        border-left: 4px solid #ef4444;
      }
    }
  }

  .task-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.875rem;

    .meta-label {
      color: #6b7280;
      font-weight: 500;
    }

    .meta-value {
      font-family: monospace;
      color: #374151;
      background: #f9fafb;
      padding: 0.25rem 0.5rem;
      border-radius: 4px;
      font-size: 0.8rem;
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
  .tasks-list-container {
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

  .tasks-stats {
    flex-direction: column;
  }

  .tasks-grid {
    grid-template-columns: 1fr;
  }

  .task-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }

  .task-id {
    text-align: left;
  }

  .task-meta {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
}
</style>
