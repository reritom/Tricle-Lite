Vue.component('done-button', {
  props: ['url'],
  template: `<div @click="done">
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
      // Send done, using url.
      //emit pulse to trigger page refresh
      var done_url = "/api/done/" + this.url + "/";
      this.$http.get(done_url)
          .then((response) => {
            this.$emit('refreshpulse');
          })
          .catch((err) => {
            console.log(err)
          })
    }
  }
})

Vue.component('download-button', {
  props: ['url', 'sessiontoken'],
  template: `<div @click="download">
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
      var status_url = "/api/status/" + this.url + "/";
      this.$http.get(status_url)
          .then((response) => {
            if (response.data.status && response.data.data.valid){
              console.log("Download status OK, trying to download");
              window.location = "/api/down/" + this.url + "/?token=" + this.sessiontoken;
            }
            else {
              console.log("Download limit reached");
              this.$emit('refreshpulse');
            };
          })
          .catch((err) => {
            console.log(err)
          })
    }
  }
})

Vue.component('start-button', {
  template:`<div class="flex-container-row">
            <div @click="$emit('starting')">
              <svg version="1.1"
                   baseProfile="full"
                   width="300" height="500"
                   xmlns="http://www.w3.org/2000/svg">

                <rect rx="15" ry="15" width="100%" height="100%" fill="red" />
                <circle cx="150" cy="100" r="80" fill="green" />
                <text x="150" y="125" font-size="60" text-anchor="middle" fill="white">Start</text>

              </svg>
              </div>
            </div>`
})

Vue.component('end-tab', {
  props: ['url', 'sessiontoken'],
  template: `<div>
            <div class="flex-container-row">
              <download-button :url="url" :sessiontoken="sessiontoken" v-on:refreshpulse="$emit('refreshpulse')"></download-button>
              <done-button :url="url" v-on:refreshpulse="$emit('refreshpulse')"></done-button>
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
                <input class="input-file" type="file" multiple :name="uploadFieldName" @change="filesChange($event.target.name, $event.target.files)"  accept="image/*">
                <p v-if="isInitial">
                  Drag your file(s) here to begin<br> or click to browse
                </p>
                <p v-else>
                  Add some more files if you want
                </p>
              </div>
              <button @click="removeAll()">Remove all selected files</button>
              <div class="flex-container-row-ns">
              <div class="box-preview" v-for="file, index in ourFileList" @click="removeOne(index)">
              Deselect {{file.name}}
              </div>
              </div>
            </div>`,
  methods: {
    filesChange: function(fieldName, fileList) {
      // To handle new images being selected
      if (this.ourFileList.length === 0){
        this.ourFileList = Array.prototype.slice.call(fileList);
      }
      else {
        // We merge any of the unique files added
        console.log(typeof(fileList));
        console.log(fileList);
        this.ourFileList = this.mergeObjects(this.ourFileList, fileList);
      }
    },
    mergeObjects: function(first, second) {
      // This method merges a list (first) with a filelist (second) to make a list with no duplicates
      var third = [];

      // Create a list for each
      var first_list = Array.prototype.slice.call(first);
      var second_list = Array.prototype.slice.call(second);

      // Create a list with the existing file names
      var existing_filenames = []
      for (var i = 0; i < first_list.length; i++) {
        existing_filenames.push(first_list[i].name);
      }

      console.log(first_list);
      console.log(second_list);

      // Merge the lists
      var third = first_list.concat(second_list.filter(function (item) {
          // For each of the new files name, if it is in the existing filename list, filter it.
          // Then concat the existing file list, with the filtered new list
          return existing_filenames.indexOf(item.name) < 0;
      }));

      return third
    },
    removeAll: function() {
      // Remove all selected files
      this.ourFileList = [];
    },
    removeOne: function(index) {
      // Remove a single selected file based on its index
      Vue.delete(this.ourFileList, index);
    }
  },
  watch: {
    ourFileList() {
      this.$emit('filesadded', this.ourFileList)
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
      url: "",
      zipcode: "",
      sessiontoken: "",
      loading: false
    }
  },
  template: `<div>
            <div v-show="loading">
              <p>We are loading</p>
            </div>
            <div v-show="!loading">
              <div class="flex-container-column">
                <div class="box"><input v-model="keyone"></div>
                <div class="box"><input v-model="keytwo"></div>
                <div class="box"><input v-model="keythree"></div>
                <div class="box"><input v-model="zipcode"></div>
                <div class="box">
                    <!-- Scramble radio boxes -->
                    <input type="radio" id="scramble" value="Scramble" v-model="mode">
                    <label for="scramble">Scramble</label>
                    <input type="radio" id="unscramble" value="Unscramble" v-model="mode">
                    <label for="unscramble">Unscramble</label>
                </div>
                <div class="box"><button v-show="formIsValid" @click="post()">I am a button</button></div>
                </div>
                <upload-handler v-on:filesadded="files = $event"></upload-handler>
            </div>
            </div>`,
  computed:{
    formIsValid () {
      if ((this.keyone.length < 3) || (this.keytwo.length < 3) || (this.keythree.length < 3) || (this.files.length === 0)) {
        return false
      }
      else {
        return true
      }
    }
  },
  methods: {
    post: function() {
      // Validate and post the form, emit the url
      if (!this.formIsValid){
        // This shouldn't happen, the button is only visible if the form is valid
        return
      }
      console.log("Posting the form");
      var formData = new FormData();
      this.createToken();

      formData.append("retrieve_token", this.sessiontoken);
      formData.append("key_one", this.keyone);
      formData.append("key_two", this.keytwo);
      formData.append("key_three", this.keythree);
      formData.append("zipcode", this.zipcode);
      formData.append("mode", this.mode);
      formData.append("images", this.files);

      // append the files to FormData
        Array
          .from(Array(this.files.length).keys())
          .map(x => {
            formData.append('images', this.files[x], this.files[x].name);
          });


      this.$http.post('/api/post', formData)
          .then((response) => {
            console.log(response);
            if (response.data.status === true) {
              console.log(response);
                this.url = response.data.data.url;
                this.triggerLoad();
            }
          })
          .catch((err) => {
            console.log(err)
          })


    },
    createToken: function() {
      // Create the session token for downloading the files
      console.log("Generation token");
      this.sessiontoken = ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
        (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
      )
    },
    triggerLoad: function() {
      // This triggers the files to be processed on the server
      console.log("Triggering the load");
      this.loading = true;
      var load_url = "/api/load/" + this.url + "/";

      this.$http.get(load_url)
          .then((response) => {
            console.log(response);
            if (response.data.status === true) {
                console.log("Load successful");
                this.$emit('urlcreated', this.url);
                this.$emit('sessioncreated', this.sessiontoken);
                this.$emit('ready');
            }
            this.loading = false;
          })
          .catch((err) => {
            console.log(err);
            console.log("Load failed");
            this.loading = false;
          })

    }
  }
})

Vue.component('main-view', {
  data: function () {
    return {
      view: 'notstarted',
      sessiontoken: "",
      url: ""
    }
  },
  template: `<div>

                <div id="FormView" v-if="view==='form'">
                    <form-tab v-on:urlcreated="url = $event" v-on:sessioncreated="sessiontoken = $event" v-on:ready="view='end'"></form-tab>
                </div>

                <div id="NotStartedView"  v-if="view==='notstarted'">
                  <start-button v-on:starting="view='form'"></start-button>
                </div>

              <div id="EndView"  v-if="view==='end'">
                <end-tab :url="url" :sessiontoken="sessiontoken" v-on:refreshpulse="view='notstarted'"></end-tab>
              </div>

            </div>`
})

new Vue({
  el: '#VueContainer',
  delimiters: ['[[',']]']
  })
