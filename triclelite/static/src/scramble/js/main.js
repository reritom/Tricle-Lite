Vue.component('done-button', {
  template: `<div>
              <svg version="1.1"
                   baseProfile="full"
                   width="300" height="500"
                   xmlns="http://www.w3.org/2000/svg">

                <rect rx="15" ry="15" width="100%" height="100%" fill="red" />
                <circle cx="150" cy="100" r="80" fill="green" />
                <text x="150" y="125" font-size="60" text-anchor="middle" fill="white">Done</text>

              </svg>
            </div>`
})

Vue.component('download-button', {
  template: `<div>
              <svg version="1.1"
                   baseProfile="full"
                   width="300" height="500"
                   xmlns="http://www.w3.org/2000/svg">

                <rect rx="15" ry="15" width="100%" height="100%" fill="red" />
                <circle cx="150" cy="100" r="80" fill="green" />
                <text x="150" y="125" font-size="60" text-anchor="middle" fill="white">Download</text>

              </svg>
            </div>`
})

Vue.component('end-tab', {
  data: function () {
    return {
      message: ""
    }
  },
  template: `<div>
            <p>This is the end tab</p>
            <div class="flex-container-row">
              <download-button></download-button>
              <done-button></done-button>
            </div>
            </div>`
})

Vue.component('form-tab', {
  props: ['noneyet'],
  data: function () {
    return {
      keyone: "",
      keytwo: "",
      keythree: ""
    }
  },
  template: `<div class="flex-container-column">
              <div class="box"><input v-model="keyone"></div>
              <div class="box"><input v-model="keytwo"></div>
              <div class="box"><input v-model="keythree"></div>
            </div>`
})

new Vue({
  el: '#VueContainer',
  delimiters: ['[[',']]'],
  data: {
  loading: false,
view: 'form'}
})
