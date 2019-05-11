<template>
<v-container fluid fill-height>
  <v-layout row wrap justify-center align-center v-if="isEmpty">
    <v-flex xs12>
      <Upload />
    </v-flex>
  </v-layout>
  <v-layout row wrap justify-center v-else>
    <v-flex xs10 mt-3>
      <v-layout row wrap>
        <v-flex xs4 pr-1>
          <v-card height="150" >
            <v-layout row wrap justify-center text-sm-center>
              <v-card-title>
                <h3>File Info</h3>
              </v-card-title>
              <v-card-text>
                <h4>File name : {{ file.name }}</h4>
                <h4>File Size : {{ file.size / 1000000 }} MB</h4>
              </v-card-text>
            </v-layout>
          </v-card>
        </v-flex>
        <v-flex xs4 px-1>
          <v-card height="150" >
            <v-layout row wrap justify-center text-sm-center>
              <v-card-title style="padding-bottom:0;">
                <h3>Log Info</h3>
              </v-card-title>
              <v-card-text text-sm-center>
                <h4>Total line : <span v-if="logs.length">{{ logs.length }}</span></h4><v-divider></v-divider>
                <h4>From : <v-chip color="green" text-color="white" v-if="logs.length" small>{{ moment(logs[0].timestamp, 'DD/MMMM/YYYY:hh:mm:ss z').format('LLL') }}</v-chip></h4><v-divider></v-divider>
                <h4>To : <v-chip color="green" text-color="white" v-if="logs.length" small>{{ moment(logs[logs.length - 1].timestamp, 'DD/MMMM/YYYY:hh:mm:ss z').format('LLL') }}</v-chip></h4>
              </v-card-text>
            </v-layout>
          </v-card>
        </v-flex>
        <v-flex xs4 pl-1>
          <v-card height="150" >
            <v-layout row wrap justify-center text-sm-center>
              <v-card-title>
                <h3>Total Prediction Anomaly</h3>
              </v-card-title>
              <v-card-text>
                <h2>{{ total_attack }} FROM {{ logs.length }}</h2>
              </v-card-text>
            </v-layout>
          </v-card>
        </v-flex>
      </v-layout>
    </v-flex>
    <v-flex xs10 mt-3>
      <Top10 :logs="logs"/>
    </v-flex>
    <v-flex xs10 mt-3>
      <v-layout row wrap justify-space-between>
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
      :pagination.sync="pagination"
      class="elevation-1">
      <template
      slot="items"
      slot-scope="props">
      <tr v-bind:class="[(props.item.class !== 'N' && hilight) ? 'anomaly' : '']">
        <td>{{ props.item.line }}</td>
        <td>{{ moment(props.item.timestamp, 'DD/MMMM/YYYY:hh:mm:ss z').format('lll') }}</td>
        <td><span @click="detail(props.item.remote_addr)">{{ props.item.remote_addr }}</span></td>
        <td>{{ props.item.method }}</td>
        <td>{{ props.item.path }}</td>
        <td>{{ props.item.version }}</td>
        <td>{{ props.item.status }}</td>
        <td>{{ props.item.bytes }}</td>
        <td>{{ props.item.class }}</td>
      </tr>
      </template>
    </v-data-table>
    </v-flex>
  </v-layout>
     <v-dialog v-model="dialog" persistent fullscreen >
      <v-card>
        <v-card-title class="headline">
          Detail Host IP : <span class="red--text">{{ host_ip }}</span>
          <v-spacer></v-spacer>
          <v-btn color="green darken-1" flat @click="dialog = false">close</v-btn>
        </v-card-title>
        <v-card-text>
          <Details :client="focus_log" />
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import Upload from '@/components/Upload.vue'
import Top10 from '@/components/Top10.vue'
import Details from '@/components/Details.vue'
export default {
  name: 'home',
  data () {
    return {
      hilight: true,
      onlyanomaly: false,
      host_ip: '',
      search: '',
      dialog: false,
      focus_log: [],
      pagination: { rowsPerPage: 10 },
      headers: [
        {
          text: 'Line',
          value: 'line'
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
      ]
    }
  },
  methods: {
    detail (ip) {
      this.host_ip = ip
      this.focus_log = this.logs.filter(x => x.remote_addr === ip)[0]
      this.dialog = true
    },
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
          url: x.path,
          version: x.version,
          status: x.status,
          bytes: x.bytes,
          class: x.class
        })
      })

      let fileTitle = 'file_log.csv'
      this.exportCSVFile(headers, itemsFormatted, fileTitle)
    }
  },
  components: {
    Upload,
    Details,
    Top10
  },
  computed: {
    isEmpty () {
      return this.$store.state.logs.length === 0
    },
    logs () {
      if (this.onlyanomaly) {
        return Object.freeze(this.$store.state.logs.filter(x => x.class !== 'N'))
      }
      return Object.freeze(this.$store.state.logs)
    },
    file () {
      return this.$store.state.file
    },
    total_attack () {
      return this.$store.state.total_attack
    },
    loading: {
      get () {
        this.$store.state.loading
      },
      set (val) {
        this.$store.commit('setLoading',val)
      }
    }
  }
}
</script>
<style >
  .anomaly {
    background-color:rgba(255, 30, 30, .5);
  }

  .anomaly:hover{
    background-color: rgba(255, 0, 0, .8)!important;
  }

  tr:hover{
    cursor: pointer;
  }

  .v-datatable {
    width: 100%!important;
  }

</style>
