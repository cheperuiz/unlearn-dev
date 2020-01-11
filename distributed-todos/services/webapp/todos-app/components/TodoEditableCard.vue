<template>
  <v-card class="ma-4" max-width="700">
    <v-card-actions>
      <v-text-field label="Title" v-model="todo.title"></v-text-field>
      <v-spacer></v-spacer>
      <v-switch v-model="todo.completed" label="Completed"></v-switch>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  props: ["todo"]
};
</script>

<style>
</style>