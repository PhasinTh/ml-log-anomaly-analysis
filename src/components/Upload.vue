<template>
  <v-layout row wrap fill-height align-center justify-center>
    <v-flex xs5>
      <v-card>
        <v-card-text>
          <v-layout row wrap py-5>
              <v-flex xs12 text-xs-center>
                <v-icon x-large>cloud_upload</v-icon>
              </v-flex>
              <v-flex xs12 text-xs-center>
                <span
                @click="filePicker"
                class="hover"
                >Choose a files</span><span class="grey--text"> or drag it here.</span>
                <input
                type="file"
                ref="file"
                multiple
                @change="onFileChange"
                style="display: none">
              </v-flex>
          </v-layout>
        </v-card-text>
      </v-card>
    </v-flex>
    <v-dialog v-model="loading" hide-overlay persistent width="300">
    <v-card color="primary" dark>
      <v-card-text>
        Please stand by
        <v-progress-linear indeterminate color="white" class="mb-0"></v-progress-linear>
      </v-card-text>
    </v-card>
  </v-dialog>
  </v-layout>
</template>

<script>
import $backend from '../backend'
import axios from 'axios'

export default {
  name: 'upload',
  data() {
    return {
      loading: false
    }
  },
  methods: {
    filePicker () {
      this.$refs.file.click()
    },
    onFileChange (e) {
      let files = e.target.files || e.dataTransfer.files
      this.upload(files[0])
      this.$store.state.file = files[0]
      // console.log(require('fs'))
    },
    readFile (file) {
      let filereader = new FileReader()
    },
    upload (file) {
      let start = performance.now()
      this.loading = true
      $backend.uploadFile(file)
        .then(response => {
          console.log(performance.now() - start)
          console.log(response)
          this.loading = false
          if (response.data) {
            let data = JSON.parse(response.data)
            this.$store.commit('setLogs', data)
          }
        })
    }
  }
}
</script>
<style scope>
  .hover:hover {
    color: mediumaquamarine;
    cursor: pointer;
  }
</style>
