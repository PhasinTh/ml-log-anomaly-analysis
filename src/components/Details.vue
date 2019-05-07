<template>
  <div>
    <v-layout row wrap>
      <v-flex xs7>
        <v-card height="280">
          <v-card-text>
            <h3>IP Address</h3>
            <v-chip v-if="client">{{ client.remote_addr }}</v-chip>
            <v-divider></v-divider>
            <h3>Browser</h3>
            <v-chip v-if="client">{{ user_agent.browser.name + ' ' +user_agent.browser.version }}</v-chip>
            <v-divider></v-divider>
            <h3>Operating System</h3>
            <v-chip v-if="client">{{ user_agent.os.name + ' ' +user_agent.os.version}}</v-chip>
            <v-divider></v-divider>
          </v-card-text>
        </v-card>
      </v-flex>
      <v-flex xs5 pl-3>
        <v-card height="280">
          <v-card-title>
            <h3>Country:</h3> <h4 v-if="client"> Thailand</h4>
          </v-card-title>
          <v-card-text>
            <GChart type="GeoChart" :data="chartData" :options="chartOptions" :resizeDebounce="500" />
          </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>
    <v-layout row wrap justify-space-between mt-3>
        <v-switch label="Hilight" v-model="hilight" ></v-switch>
        <v-switch label="Show only anomaly" v-model="onlyanomaly" ></v-switch>
        <v-btn color="info darken-1"  @click="save_csv">Export</v-btn>
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
      <tr v-bind:class="[(props.item.class > 0 && hilight) > 0 ? 'anomaly' : '']">
        <td>{{ props.item.line }}</td>
        <td>{{ props.item.timestamp }}</td>
        <td >{{ props.item.remote_addr }}</td>
        <td>{{ props.item.method }}</td>
        <td class="text-xs-left">{{ props.item.url }}</td>
        <td>{{ props.item.version }}</td>
        <td>{{ props.item.status }}</td>
        <td>{{ props.item.bytes }}</td>
        <td>{{ props.item.class }}</td>
      </tr>
      </template>
    </v-data-table>
  </div>
</template>
<script>
import { GChart } from 'vue-google-charts'
import axios from 'axios'
const parser = require('ua-parser-js')
export default {
  mounted () {
    // console.log(this.client.country)
  },
  methods: {
    convertToCSV (objArray) {
      var array = typeof objArray != 'object' ? JSON.parse(objArray) : objArray;
      var str = '';
      for (var i = 0; i < array.length; i++) {
        var line = '';
        for (var index in array[i]) {
            if (line != '') line += ','

            line += array[i][index];
        }

        str += line + '\r\n';
      }
      return str;
    },
    exportCSVFile(headers, items, fileTitle) {
      if (headers) {
        items.unshift(headers);
      }

      // Convert Object to JSON
      let jsonObject = JSON.stringify(items)
      let csv = this.convertToCSV(jsonObject)

      let exportedFilenmae = fileTitle + '.csv' || 'export.csv'

      let blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' })

      if (navigator.msSaveBlob) { // IE 10+
        navigator.msSaveBlob(blob, exportedFilenmae);
      } else {
        var link = document.createElement("a");
        if (link.download !== undefined) { // feature detection
            // Browsers that support HTML5 download attribute
            var url = URL.createObjectURL(blob);
            link.setAttribute("href", url);
            link.setAttribute("download", exportedFilenmae);
            link.style.visibility = 'hidden';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
      }

    },
    save_csv () {
      let headers = this.headers.map(x => x.text)
      let itemsFormatted = []

      this.logs.forEach(x => {
        itemsFormatted.push({
          line: x.line,
          timestamp: x.timestamp,
          remote_addr: x.remote_addr,
          method: x.method,
          url: x.url,
          version: x.version,
          status: x.status,
          bytes: x.bytes,
          class: x.class
        })
      })

      let fileTitle = 'log_'+ this.client.remote_addr +'.csv'
      this.exportCSVFile(headers, itemsFormatted, fileTitle)
    }
  },
  props: ['client'],
  components: {
    GChart
  },
  data () {
    return {
      hilight: true,
      onlyanomaly: false,
      country: 'Thailand',
      region: 'TH',
      search: '',
      pagination: { rowsPerPage: 10 },
      headers: [
        {
          text: 'Line',
          value: 'index'
        },
        {
          text: 'Timestamp',
          value: 'timestamp'
        },
        {
          text: 'Remote_addr',
          value: 'remote_addr'
        },
        {
          text: 'Method',
          value: 'method'
        },
        {
          text: 'Path',
          value: 'url'
        },
        {
          text: 'Version',
          value: 'version'
        },
        {
          text: 'Status',
          value: 'status'
        },
        {
          text: 'Bytes',
          value: 'bytes'
        },
        {
          text: 'Class',
          value: 'class'
        }
      ],
      chartData: [
        ['Country'],
        ['Thailand']
      ],
      chartOptions: {
        height: 200, region: 'TH', width: '100%'
      }
    }
  },
  computed: {
    logs () {
      if (this.client) {
        if (this.onlyanomaly) {
          return this.$store.state.logs.filter(x => (x.remote_addr == this.client.remote_addr) && x.class > 0)
        }
        return this.$store.state.logs.filter(x => x.remote_addr == this.client.remote_addr)
      }
    },
    user_agent () {
      let user_agent = parser(this.client.user_agent)
      // console.log(user_agent)
      return user_agent
    }
  }
}
</script>
<style scope>
  .v-card__title {
    padding: 10px;
    padding-bottom: 0px;
  }

  .anomaly:hover{
    background-color: rgba(255, 0, 0, .8)!important;
  }
</style>
