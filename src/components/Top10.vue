<template>
  <div>
    <v-layout row wrap>
      <v-flex xs6 pr-2>
        <v-card  height="490">
          <v-card-text>
            <apexchart type=donut width="100%"  height="360"  :options="chartOptions" :series="attack_type" />
          </v-card-text>
        </v-card>
      </v-flex>
      <v-flex xs6 pl-2>
        <v-card height="490">
          <v-layout row wrap justify-center>
            <v-card-title primary-title>
              <h3>Top 10 Suspected IP</h3>
            </v-card-title>
            <v-card-text>
              <v-data-table
                :items="attacker"
                class="elevation-1"
                :headers="attacker_header"
              >
                <template slot="items" slot-scope="props">
                  <tr @click="detail(props.item.ip)">
                    <td class="">{{ props.item.rank }}</td>
                    <td class="">{{ props.item.ip }}</td>
                    <td class="">{{ props.item.count }}</td>
                  </tr>
                </template>
              </v-data-table>
            </v-card-text>
          </v-layout>
        </v-card>
      </v-flex>
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
    </v-layout>
  </div>
</template>
<script>
import apexchart from 'vue-apexcharts'
import Details from '@/components/Details.vue'
export default {
  props: ['logs'],
  components: {
    apexchart,
    Details
  },
  data () {
    return {
      host_ip: null,
      dialog: false,
      focus_log: null,
      attacker_header: [
        {
          text: 'RANK',
          value: 'rank'
        },
        {
          text: 'IP',
          value: 'ip'
        },
        {
          text: 'Anomaly',
          value: 'count'
        }
      ],
      chartOptions: {
        plotOptions: {
          pie: {
            donut: {
              labels: {
                show: true
              }
            }
          }
        },
        labels: ['XSS', 'SQL Injection', 'Directory Travelsal'],
        title: {
          text: 'Ratio of attacks'
        },
        responsive: [{
          breakpoint: 480,
          options: {
            chart: {
              width: 200
            },
            legend: {
              position: 'bottom'
            }
          }
        }]
      }
    }
  },
  methods: {
    detail (ip) {
      this.host_ip = ip
      this.focus_log = this.logs.filter(x => x.remote_addr == ip)[0]
      this.dialog = true
    }
  },
  computed: {
    uniqueIP () {
      return [...new Set(this.logs.map(x => x.remote_addr))]
    },
    attack_type () {
      let test = [0,0,0,0]
      this.attack_total = this.logs.filter(function (x) {
        let index = 0
        if (x.class === 'XSS') {
          index = 1
        } else if (x.class === 'SQLi') {
          index = 2
        } else if (x.class === 'DT') {
          index = 3
        }
        test[index] = test[index] >= 0 ? test[index] += 1 : 0
        return x.class !== 'N'
      }).length
      this.$store.state.total_attack = this.attack_total
      // console.log(test)
      return test.slice(1)
    },
    attacker () {
      let attacker = []
      let temp = {}
      this.logs.forEach(x => {
        if (x.class !== 'N') {
          temp[x.remote_addr] = temp[x.remote_addr] >= 0 ? temp[x.remote_addr] += 1 : 0
        }
        // temp[x.remote_addr] = temp[x.remote_addr] >= 0 ? temp[x.remote_addr] += 1 : 0 // test
      })
      for (const key in temp) {
        if (temp.hasOwnProperty(key)) {
          const element = temp[key]
          attacker.push({ ip: key, count: element })
        }
      }
      // console.log(attacker)
      attacker.sort((a, b) => b.count - a.count)
      attacker.forEach((x, i) => x['rank'] = i + 1)
      return attacker.slice(0, 10)
    }
  }
}
</script>
<style>
  .apexcharts-title-text {
    font-size: 1.2em;
    font-weight: bold;
  }
</style>
