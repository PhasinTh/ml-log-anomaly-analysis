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
                <h4>From : <v-chip color="green" text-color="white" v-if="logs.length" small>{{ moment(logs[0].Date_time, 'DD/MMMM/YYYY:hh:mm:ss z').format('LLL') }}</v-chip></h4><v-divider></v-divider>
                <h4>To : <v-chip color="green" text-color="white" v-if="logs.length" small>{{ moment(logs[logs.length - 1].Date_time, 'DD/MMMM/YYYY:hh:mm:ss z').format('LLL') }}</v-chip></h4>
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
                <h2>{{ total_attack }}</h2>
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
      :pagination.sync="pagination"
      class="elevation-1">
      <template
      slot="items"
      slot-scope="props">
      <tr v-bind:class="[(props.item.Label > 0 && hilight) ? 'anomaly' : '']">
        <td>{{ props.index }}</td>
        <td>{{ moment(props.item.Date_time, 'DD/MMMM/YYYY:hh:mm:ss z').format('lll') }}</td>
        <td><span @click="detail(props.item.Remote_host)">{{ props.item.Remote_host }}</span></td>
        <td>{{ props.item.Method }}</td>
        <td>{{ props.item.Path }}</td>
        <td>{{ props.item.Version }}</td>
        <td>{{ props.item.Status }}</td>
        <td>{{ props.item.Length }}</td>
        <td>{{ props.item.Label }}</td>
      </tr>
      </template>
    </v-data-table>
    </v-flex>
  </v-layout>
  <v-dialog v-model="dialog" persistent max-width="80%">
    <v-card>
      <v-card-title class="headline">
        Detail Host IP : <span class="red--text">{{ host_ip }}</span>
        <v-spacer></v-spacer>
        <v-btn color="green darken-1" flat @click="dialog = false">close</v-btn>
      </v-card-title>
      <v-card-text>
        <Details :logs="focus_log" />
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
      host_ip: '',
      search: '',
      dialog: false,
      focus_log: [],
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
          text: 'Bytes',
          value: 'Length'
        },
        {
          text: 'Label',
          value: 'Label'
        }
      ]
    }
  },
  methods: {
    detail (ip) {
      this.host_ip = ip
      this.focus_log = this.logs.filter(x => x.Remote_host == ip)
      this.dialog = true
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
      return this.$store.state.logs
    },
    file () {
      return this.$store.state.file
    },
    total_attack () {
      return this.$store.state.total_attack
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
