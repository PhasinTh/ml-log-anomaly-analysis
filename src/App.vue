<template>
  <v-app >
    <v-layout row wrap>
      <v-content>
        <router-view></router-view>
      </v-content>
    </v-layout>
  </v-app>
</template>
<script>
export default {
  name: 'app',
  data () {
    return {
      drawer: true,
      items: [
        { title: 'Dashboard', icon: 'dashboard' },
        { title: 'About', icon: 'question_answer' }
      ],
      mini: true
    }
  },
  methods: {
    goto (item) {
      this.$router.replace(item.title)
    }
  },
  computed: {
    isEmpty () {
      return this.$store.state.logs.length === 0
    }
  }
}
</script>
