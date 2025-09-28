<template>
  <section class="main_section__form_create_user">
    <div class="form-container">
      <h2 class="form-title">Utwórz nowego użytkownika</h2>

      <form @submit.prevent="handleSubmit" class="user-form">
        <div class="form-group">
          <label for="name" class="form-label">Imię</label>
          <input
            id="name"
            v-model="formData.name"
            type="text"
            placeholder="Wprowadź imię"
            class="form-input"
            :class="{ error: errors.name }"
          />
          <span v-if="errors.name" class="error-message">{{
            errors.name
          }}</span>
        </div>

        <div class="form-group">
          <label for="lastname" class="form-label">Nazwisko</label>
          <input
            id="lastname"
            v-model="formData.lastname"
            type="text"
            placeholder="Wprowadź nazwisko"
            class="form-input"
            :class="{ error: errors.lastname }"
          />
          <span v-if="errors.lastname" class="error-message">{{
            errors.lastname
          }}</span>
        </div>

        <div class="form-group">
          <label for="email" class="form-label">Email</label>
          <input
            id="email"
            v-model="formData.email"
            type="email"
            placeholder="Wprowadź email"
            class="form-input"
            :class="{ error: errors.email }"
          />
          <span v-if="errors.email" class="error-message">{{
            errors.email
          }}</span>
        </div>

        <div class="form-group">
          <label for="age" class="form-label">Wiek</label>
          <input
            id="age"
            v-model="formData.age"
            type="number"
            placeholder="Wprowadź wiek"
            class="form-input"
            :class="{ error: errors.age }"
            min="1"
            max="120"
          />
          <span v-if="errors.age" class="error-message">{{ errors.age }}</span>
        </div>

        <div class="form-group">
          <label for="city" class="form-label">Miasto</label>
          <input
            id="city"
            v-model="formData.city"
            type="text"
            placeholder="Wprowadź miasto"
            class="form-input"
            :class="{ error: errors.city }"
          />
          <span v-if="errors.city" class="error-message">{{
            errors.city
          }}</span>
        </div>

        <button type="submit" class="submit-button" :disabled="isSubmitting">
          {{ isSubmitting ? "Wysyłanie..." : "Utwórz użytkownika" }}
        </button>
      </form>
    </div>
  </section>
</template>

<script lang="ts">
import { defineComponent, ref, reactive } from "vue";

// apis
import { apiCreateUser } from "@/api/post";

export default defineComponent({
  setup() {
    const formData = ref({
      name: "",
      lastname: "",
      email: "",
      age: "",
      city: "",
    });

    const errors = reactive({
      name: "",
      lastname: "",
      email: "",
      age: "",
      city: "",
    });

    const isSubmitting = ref(false);

    const validateForm = (): boolean => {
      Object.keys(errors).forEach((key) => {
        errors[key as keyof typeof errors] = "";
      });

      let isValid = true;

      if (!formData.value.name.trim()) {
        errors.name = "Imię jest wymagane";
        isValid = false;
      }

      if (!formData.value.lastname.trim()) {
        errors.lastname = "Nazwisko jest wymagane";
        isValid = false;
      }

      if (!formData.value.email.trim()) {
        errors.email = "Email jest wymagany";
        isValid = false;
      } else if (!formData.value.email.includes("@")) {
        errors.email = "Email musi zawierać znak @";
        isValid = false;
      }

      if (!formData.value.age.toString().trim()) {
        errors.age = "Wiek jest wymagany";
        isValid = false;
      } else if (
        parseInt(formData.value.age) < 1 ||
        parseInt(formData.value.age) > 120
      ) {
        errors.age = "Wiek musi być między 1 a 120";
        isValid = false;
      }

      if (!formData.value.city.trim()) {
        errors.city = "Miasto jest wymagane";
        isValid = false;
      }

      return isValid;
    };

    const clearForm = () => {
      formData.value = {
        name: "",
        lastname: "",
        email: "",
        age: "",
        city: "",
      };

      Object.keys(errors).forEach((key) => {
        errors[key as keyof typeof errors] = "";
      });
    };

    const handleSubmit = async () => {
      if (!validateForm()) {
        return;
      }

      isSubmitting.value = true;

      try {
        const userData = {
          name: formData.value.name.trim(),
          lastname: formData.value.lastname.trim(),
          email: formData.value.email.trim(),
          age: formData.value.age.toString().trim(),
          city: formData.value.city.trim(),
        };

        const response = await apiCreateUser(userData);
        if (response.isValid) {
          await new Promise((resolve) => setTimeout(resolve, 1000));
          clearForm();
          console.info("Formularz został pomyślnie wysłany i wyczyszczony");
          return;
        }
        console.error("Formularz nie został pomyślnie wysłany i wyczyszczony!");
      } catch (error) {
        console.error("Błąd podczas wysyłania formularza:", error);
      } finally {
        isSubmitting.value = false;
      }
    };

    return {
      formData,
      errors,
      isSubmitting,
      handleSubmit,
    };
  },
});
</script>

<style scoped lang="scss">
.main_section__form_create_user {
  width: 100%;
  min-height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 16px;
}

.form-container {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1),
    0 10px 10px -5px rgba(0, 0, 0, 0.04);
  min-width: 1200px;
}

.form-title {
  font-size: 1.875rem;
  font-weight: 700;
  text-align: center;
  margin-bottom: 2rem;
  color: #374151;
}

.user-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 0.25rem;
}

.form-input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.2s ease-in-out;
  background-color: #fff;

  &:focus {
    outline: none;
    border-color: #667eea;
  }

  &.error {
    border-color: #ef4444;
    background-color: #fef2f2;
  }

  &::placeholder {
    color: #9ca3af;
  }
}

.error-message {
  font-size: 0.75rem;
  color: #ef4444;
  font-weight: 500;
  margin-top: 0.25rem;
}

.submit-button {
  width: 100%;

  color: black;
  padding: 0.875rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
  margin-top: 1rem;

  &:hover:not(:disabled) {
    transform: translateY(-1px);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  }

  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
  }

  &:active {
    transform: translateY(0);
  }
}

// Responsywność
@media (max-width: 640px) {
  .form-container {
    margin: 1rem;
    padding: 1.5rem;
  }

  .form-title {
    font-size: 1.5rem;
    margin-bottom: 1.5rem;
  }

  .user-form {
    gap: 1.25rem;
  }
}
</style>
