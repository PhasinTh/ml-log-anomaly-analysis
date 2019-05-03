<template>
  <div>
    <v-layout row wrap>
      <v-flex xs7>
        <v-card height="280">
          <v-card-text>
            <h3>IP Address</h3>
            <v-chip v-if="client"></v-chip>
            <v-divider></v-divider>
            <h3>Browser</h3>
            <v-chip v-if="client"></v-chip>
            <v-divider></v-divider>
            <h3>Operating System</h3>
            <v-chip v-if="client"></v-chip>
            <v-divider></v-divider>
          </v-card-text>
        </v-card>
      </v-flex>
      <v-flex xs5 pl-3>
        <v-card height="280">
          <v-card-title>
            <h3>Country:</h3> <h4>Thailand</h4>
          </v-card-title>
          <v-card-text>
            <GChart type="GeoChart" :data="chartData" :options="chartOptions" :resizeDebounce="500" />
          </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>
    <v-layout row wrap justify-space-between mt-3>
        <v-switch label="Prediction" v-model="hilight" ></v-switch>
        <v-flex xs6 pl-3>
          <v-text-field
            v-model="search"
            append-icon="search"
            label="Search"
            single-line
            hide-details
          ></v-text-field>
        </v-flex>
      </v-layout>
    <v-data-table
      :headers="headers"
      :items="logs"
      :search="search"
      expand
      :pagination.sync="pagination"
      class="elevation-1">
      <template
      slot="items"
      slot-scope="props">
      <tr v-bind:class="[props.item.Label > 0 ? 'anomaly' : '']">
        <td>{{ props.index }}</td>
        <td>{{ props.item.Date_time }}</td>
        <td >{{ props.item.Remote_host }}</td>
        <td>{{ props.item.Method }}</td>
        <td class="text-xs-left">{{ props.item.Path }}</td>
        <td>{{ props.item.Version }}</td>
        <td>{{ props.item.Status }}</td>
        <td>{{ props.item.Length }}</td>
        <td>{{ props.item.Label }}</td>
      </tr>
      </template>
    </v-data-table>
  </div>
</template>
<script>
import { GChart } from 'vue-google-charts'
const parser = require('ua-parser-js')
export default {
  mounted () {
    console.log(parser('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.2 (KHTML, like Gecko) Ubuntu/11.10 Chromium/15.0.874.106 Chrome/15.0.874.106 Safari/535.2'))
  },
  props: ['client'],
  components: {
    GChart
  },
  data () {
    return {
      hilight: true,
      search: '',
      pagination: { rowsPerPage: 10 },
      headers: [
        {
          text: 'Line',
          value: 'index'
        },
        {
          text: 'Date_time',
          value: 'Date_time'
        },
        {
          text: 'Remote_host',
          value: 'Remote_host'
        },
        {
          text: 'Method',
          value: 'Method'
        },
        {
          text: 'Path',
          value: 'Path'
        },
        {
          text: 'Version',
          value: 'Version'
        },
        {
          text: 'Status',
          value: 'Status'
        },
        {
          text: 'Length',
          value: 'Length'
        },
        {
          text: 'Label',
          value: 'Label'
        }
      ],
      chartData: [
        ['Country'],
        ['Thailand']
      ],
      chartOptions: {
        height: 200, region: 'TH'
      }
    }
  },
  computed: {
    logs () {
      if (this.client) { return this.$store.state.logs.filter(x => x.Remote_host == this.client.Remote_host) }
    }
  }
}
</script>
<style scope>
  .v-card__title {
    padding: 10px;
    padding-bottom: 0px;
  }
</style>
