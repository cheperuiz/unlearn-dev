<template>
  <v-card class="ma-4" max-width="800">
    <v-card-actions>
      <v-card-title>{{todo.title}}</v-card-title>
      <v-spacer></v-spacer>
      <v-card-subtitle>Completed:</v-card-subtitle>
      <v-icon v-if="todo.completed" color="success">mdi-circle</v-icon>
      <v-icon v-else>mdi-circle-outline</v-icon>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  props: ["todo"]
};
</script>

