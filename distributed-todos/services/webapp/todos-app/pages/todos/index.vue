<template>
  <div>
    <v-btn
      @click="$router.push('todos/new')"
      color="info"
      fab
      x-large
      dark
      absolute
      right
      fixed
      class="display-1"
    >
      <v-icon>mdi-plus</v-icon>
    </v-btn>
    <v-text-field
      prepend-icon="mdi-filter"
      label="Filter"
      v-model="filter"
      clearable
      style="max-width: 700px"
    ></v-text-field>
    <v-card-text class="title">Showing: {{filtered.length}}</v-card-text>
    <v-card-text class="subtitle-2">Completed: {{filtered.filter(e=>e.completed).length}}</v-card-text>

    <nuxt-link v-for="t in filtered" :key="t.uuid" :to="'todos/'+t.uuid" max-width="800">
      <todo-card :todo="t"></todo-card>
    </nuxt-link>
  </div>
</template>

<script>
import TodoCard from "~/components/TodoCard.vue";
export default {
  data() {
    return {
      filter: ""
    };
  },

  components: {
    TodoCard
  },

  computed: {
    filtered() {
      return !!this.filter
        ? this.todos.filter(e =>
            e.title.toUpperCase().includes(this.filter.toUpperCase())
          )
        : this.todos;
    }
  },

  async asyncData({ app }) {
    const { data: res } = await app.$axios.get("/todos/");
    return {
      todos: res.data.values
    };
  }
};
</script>


<style lang="scss" scoped>
a {
  text-decoration: none;
}
</style>
