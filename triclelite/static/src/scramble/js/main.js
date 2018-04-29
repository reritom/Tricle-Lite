Vue.component('done-button', {
  props: ['url'],
  template: `<div>
              <svg version="1.1"
                   baseProfile="full"
                   width="300" height="500"
                   xmlns="http://www.w3.org/2000/svg">

                <rect rx="15" ry="15" width="100%" height="100%" fill="red" />
                <circle cx="150" cy="100" r="80" fill="green" />
                <text x="150" y="125" font-size="60" text-anchor="middle" fill="white">Done</text>

              </svg>
            </div>`,
  methods: {
    done: function () {
      // Send done,using url.
      //emit pulse to trigger page refresh
    }
  }
})

Vue.component('download-button', {
  props: ['url'],
  template: `<div>
              <svg version="1.1"
                   baseProfile="full"
                   width="300" height="500"
                   xmlns="http://www.w3.org/2000/svg">

                <rect rx="15" ry="15" width="100%" height="100%" fill="red" />
                <circle cx="150" cy="100" r="80" fill="green" />
                <text x="150" y="125" font-size="60" text-anchor="middle" fill="white">Download</text>

              </svg>
            </div>`,
  methods: {
    download: function() {
      // checkStatus
      // if ok, download
    }
  }
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

Vue.component('upload-handler', {
  data: function () {
    return {
      uploadFieldName: "Photos",
      ourFileList: []
    }
  },
  template: `<div>
              <div class="dropbox">
                <input class="input-file" type="file" multiple :name="uploadFieldName" :disabled="isPosting" @change="filesChange($event.target.name, $event.target.files); fileCount = $event.target.files.length"  accept="image/*">
                <p v-if="isInitial">
                  Drag your file(s) here to begin<br> or click to browse
                </p>
              </div>
              <div v-for="file, index in ourFileList">
              <p> Filename is {{file.name}}, index is {{index}}</p>
            </div>`,
  methods: {
    filesChange: function(fieldName, fileList) {
      // To handle new images being selected
      this.ourFileList = fileList;
    }
  },
  computed: {
    isInitial() {
      return this.ourFileList.length === 0
    }
  }
})

Vue.component('form-tab', {
  data: function () {
    return {
      keyone: "",
      keytwo: "",
      keythree: "",
      mode: "Scramble",
      files: "",
      url: ""
    }
  },
  template: `<div>
            <div class="flex-container-column">
              <div class="box"><input v-model="keyone"></div>
              <div class="box"><input v-model="keytwo"></div>
              <div class="box"><input v-model="keythree"></div>
              </div>
              <upload-handler></upload-handler>
            </div>`,
  methods: {
    post: function() {
      // Validate and post the form, emit the url
    },
    createToken: function() {
      // Create the session token for downloading the files
    }
  }
})

new Vue({
  el: '#VueContainer',
  delimiters: ['[[',']]'],
  data: {
    loading: false,
    view: 'form',
    url: ""}
  })
