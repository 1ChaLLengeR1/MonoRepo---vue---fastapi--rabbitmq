<template>
  <div class="main_section__show_form_user">
    <button @click="handlerShowForm" class="styled-button">
      {{ buttonText }}
    </button>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";

export default defineComponent({
  emits: ["show-form"],
  setup(_, ctx) {
    const showForm = ref<boolean>(false);
    const buttonText = ref<string>("Pokaż Formularz");

    const handlerShowForm = () => {
      showForm.value = !showForm.value;
      buttonText.value = showForm.value ? "Ukryj Formularz" : "Pokaż Formularz";
      ctx.emit("show-form", showForm.value);
    };

    return { showForm, buttonText, handlerShowForm };
  },
});
</script>

<style scoped lang="scss">
.main_section__show_form_user {
  width: 100%;
  min-height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2rem;
}

.styled-button {
  background: white;
  color: #374151;
  border: none;
  border-radius: 12px;
  padding: 1rem 2rem;
  font-size: 1.125rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  min-width: 1200px;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    background: #f8f9fa;
  }

  &:active {
    transform: translateY(0);
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  }
}
</style>
