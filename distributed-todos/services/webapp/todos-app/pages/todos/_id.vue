<template>
  <div>
    <todo-editable-card :todo="todo"></todo-editable-card>

    <v-toolbar color="rgba(0,0,0,0)" max-width="700" class="ma-4" flat>
      <v-btn @click="goBack()" color="info" class="ma-0">
        <v-icon class="mr-4">mdi-undo</v-icon>Back
      </v-btn>
      <v-spacer></v-spacer>
      <v-btn @click="deleteTodo(todo)" color="error" class="mr-4">
        <v-icon class="mr-2">mdi-delete-forever-outline</v-icon>Delete
      </v-btn>
      <v-btn @click="updateTodo(todo)" color="success">
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

  async asyncData({ app, params }) {
    const { data: res } = await app.$axios.get(`/todos/${params.id}`);
    return {
      todo: res.data
    };
  },

  methods: {
    goBack() {
      this.$router.go(-1);
    },
    async updateTodo(todo) {
      const { title, completed, uuid } = todo;
      try {
        const { data: res } = await this.$axios.put(`/todos/${uuid}`, {
          title,
          completed
        });
        this.goBack();
      } catch (e) {
        console.log(e);
      }
    },
    async deleteTodo(todo) {
      const { uuid } = todo;
      try {
        const { data: res } = await this.$axios.delete(`/todos/${uuid}`);
        this.goBack();
      } catch (e) {
        console.log(e);
      }
    }
  }
};
</script>

