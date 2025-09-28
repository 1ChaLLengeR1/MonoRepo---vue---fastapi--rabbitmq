<template>
  <div class="app-wrapper">
    <ShowFormUserVue @show-form="handlerShowForm" />
    <FormCreateUserVue v-if="showForm" />
    <ListUsersVue />
    <ListTasksVue />
  </div>
</template>
<script lang="ts">
import { defineComponent, ref } from "vue";
// components
import ShowFormUserVue from "@/components/ShowFormCreateUser.vue";
import FormCreateUserVue from "@/components/FormCreateUser.vue";
import ListUsersVue from "@/components/ListUser.vue";
import ListTasksVue from "@/components/ListTask.vue";
export default defineComponent({
  components: {
    ShowFormUserVue,
    FormCreateUserVue,
    ListUsersVue,
    ListTasksVue,
  },
  setup() {
    const showForm = ref<boolean>(false);

    const handlerShowForm = (actvie: boolean) => {
      showForm.value = actvie;
    };

    return { showForm, handlerShowForm };
  },
});
</script>

<style lang="scss">
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

.app-wrapper {
  gap: 4px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
}
</style>
