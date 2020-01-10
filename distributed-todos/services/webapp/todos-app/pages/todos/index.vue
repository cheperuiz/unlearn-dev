<template>
  <div>
    <nuxt-link v-for="todo in todos" :key="todo.uuid" to="/todos/1">todo.uuid</nuxt-link>
  </div>
</template>

<script>
export default {
  async asyncData({ app }) {
    const { data: todos } = await app.$axios.get(
      "http://localhost:5000/todos-api/v1/todos/"
    );
    return {
      todos
    };
  }
};
</script>

<style>
</style>