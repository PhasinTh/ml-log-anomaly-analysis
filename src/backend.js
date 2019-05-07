import axios from 'axios'

let $axios = axios.create({
  baseURL: '/api/',
  timeout: 1000 * 60 * 60 * 60,
  maxContentLength: 1024 * 1024 * 1024 * 1024
  // headers: { 'Content-Type': 'application/json' }
})

// Request Interceptor
$axios.interceptors.request.use(function (config) {
  config.headers['Authorization'] = 'Fake Token'
  return config
})

// Response Interceptor to handle and log errors
$axios.interceptors.response.use(function (response) {
  return response
}, function (error) {
  // Handle Error
  console.log(error)
  return Promise.reject(error)
})

export default {

  fetchResource () {
    return $axios.get(`resource/xxx`)
      .then(response => response.data)
  },

  fetchSecureResource () {
    return $axios.get(`secure-resource/zzz`)
      .then(response => response.data)
  },

  uploadFile (data) {
    let formData = new FormData()
    formData.append('file', data)
    return $axios.post('uploadfile', formData)
      .then(response => response.data)
  },

  downloadFile (ip) {
    if (ip !== '') {
      return $axios.post('download/' + ip)
    }
    return $axios.post('download')
  }
}
