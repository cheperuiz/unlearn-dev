<template>
  <div>
    <todo-editable-card :todo="todo"></todo-editable-card>
    <v-toolbar color="rgba(0,0,0,0)" max-width="700" class="ma-4" flat>
      <v-btn @click="goBack()" color="info" class="ma-0">
        <v-icon class="mr-4">mdi-undo</v-icon>Back
      </v-btn>
      <v-spacer></v-spacer>
      <v-btn @click="save(todo)" color="success">
        <v-icon class="mr-2">mdi-content-save-outline</v-icon>Save
      </v-btn>
    </v-toolbar>
  </div>
</template>

<script>
import TodoEditableCard from "~/components/TodoEditableCard.vue";
export default {
  components: {
    TodoEditableCard
  },
  data() {
    return {
      todo: {
        title: "",
        completed: false
      }
    };
  },
  methods: {
    goBack() {
      this.$router.go(-1);
    },
    async save(todo) {
      const { title, completed } = todo;
      try {
        console.log(title, completed);
        const { data: res } = await this.$axios.post("/todos/", {
          title,
          completed
        });
        this.goBack();
      } catch (e) {
        console.log("failed", e);
      }
    }
  }
};
</script>

<style>
</style>
