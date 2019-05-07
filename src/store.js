import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    logs: [],
    file: null,
    total_attack: 0,
    loading: false
  },
  mutations: {
    setLogs (state, payload) {
      state.logs = payload
    },
    setLoading (state, payload) {
      state.loading = payload
    }
  },
  actions: {

  }
})
