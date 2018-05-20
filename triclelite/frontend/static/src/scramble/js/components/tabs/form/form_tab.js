const UploadHandler = () => import('./tab_components/upload_handler.js');

export default {
  name: "FormTab",
  components: {
    UploadHandler
  },
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
};
