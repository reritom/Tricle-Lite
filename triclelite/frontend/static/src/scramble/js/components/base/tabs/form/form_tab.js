const UploadHandler = () => import('./tab_components/upload_handler.js');

export default {
  name: "FormTab",
  components: {
    UploadHandler
  },
  data: function () {
    return {
      keys: ["", "", ""],
      keyvis: ["password", "password", "password", "password"],
      mode: "Scramble",
      files: "",
      url: "",
      zipcode: "",
      sessiontoken: "",
      loading: false,
      keyview: true,
      fileview: false
    }
  },
  template: `<div>
            <div v-show="loading">
              <p>We are loading</p>
            </div>

            <div v-show="!loading">

            <button :class="getKeyviewClass()" @click="keyview = !keyview">Your keys</button>
            <form v-show="keyview">
              <div class="flex-container-column">

                <div class="input-group" v-for="key, index in keys">
                    <input class="form-control pwd pwd-input" :type="keyvis[index]" v-model="keys[index]" :placeholder="placeholderVal(index)" v-on:keydown.tab="toggleExpansion(index)">
                    <span class="input-group-btn">
                      <button class="btn btn-default reveal icon-btn" @click="toggleKeyVisibility($event, index)" v-html="visVal(index)" :tabindex="-1">
                      </button>
                    </span>
                </div>

                <!--div class="input-group">
                  <input class="form-control pwd pwd-input" v-model="zipcode" :type="keyvis[3]" :placeholder="placeholderVal(3)">
                  <span class="input-group-btn">
                    <button class="btn btn-default reveal icon-btn" @click="toggleKeyVisibility($event, 3)" v-html="visVal(3)">
                    </button>
                  </span>
                </div-->

                <div class="box btn-holder">
                  <div class="row">
                    <div class="col col-md-6">
                      <button @click="selectMode($event, 'Scramble')" :class="getClass('S')">Scramble</button>
                    </div>
                    <div class="col col-md-6">
                      <button @click="selectMode($event, 'Unscramble')" :class="getClass('U')">Unscramble</button>
                    </div>
                  </div>
                </div>

              </div>
            </form>
            <div class="box btn-holder">
              <button :class="getPostClass()" :disabled="!fullFormIsValid" @click="post($event)">Go!</button>
            </div>
              <button :class="getFileviewClass()" @click="fileview = !fileview"> Your Files </button>
              <upload-handler v-show="fileview" v-on:filesadded="files = $event"></upload-handler>
            </div>

            </div>`,
  computed:{
    fullFormIsValid () {
      if ((this.keys[0].length < 3) || (this.keys[1].length < 3) || (this.keys[2].length < 3) || (this.files.length < 1)) {
        return false
      }
      else {
        return true
      }
    },
    formIsValid () {
      if ((this.keys[0].length < 3) || (this.keys[1].length < 3) || (this.keys[2].length < 3)) {
        return false
      }
      else {
        return true
      }
    },
    fileFormIsValid () {
      if (this.files.length < 1) {
        return false
      }
      else {
        return true
      }
    }
  },
  methods: {
    toggleKeyVisibility(event, index){
      event.preventDefault();
      console.log("Toggling the visibility for" + index);
      console.log("This key is " + this.keyvis[index]);

      if (this.keyvis[index] === 'password'){
        // we will instead toggle it to visible, but in doing so, any other visible ones need to be hidden

        var newlist = [];
        for (var i=0; i<this.keyvis.length; i++){
          newlist.push('password');
        }
        newlist[index] = 'text';
        this.keyvis = newlist;
      }
      else {
        var newlist = [];
        for (var i=0; i<this.keyvis.length; i++){
          newlist.push(this.keyvis[i]);
        }

        newlist[index] = 'password';
        this.keyvis = newlist;
      }
    },
    toggleExpansion(index) {
      if (index !== 2) {
        return
      }
      else {
        this.keyview = false;
        this.fileview = true;
      }
    },
    getClass(mode) {
      if (mode === "U") {
        return {
          'btn': true,
          'btn-holder-btn': true,
          'btn-primary': (this.mode === "Unscramble") ? true : false
        }
      }
      else if (mode === "S"){
        return{
          'btn': true,
          'btn-holder-btn': true,
          'btn-primary': (this.mode === "Scramble") ? true : false
        }
      }
    },
    getPostClass() {
      return{
        'btn': true,
        'btn-block': true,
        'btn-default': (!this.fullFormIsValid) ? true : false,
        'btn-success': (this.fullFormIsValid) ? true : false
      }
    },
    getKeyviewClass() {
      return {
        'btn btn-block': true,
        'btn-default': !this.formIsValid,
        'btn-success': this.formIsValid
      }
    },
    getFileviewClass() {
      return {
        'btn btn-block': true,
        'btn-default': !this.fileFormIsValid,
        'btn-success': this.fileFormIsValid
      }
    },
    selectMode(event, mode) {
      event.preventDefault();

      this.mode = mode;
    },
    visVal(index) {
      if (this.keyvis[index] === 'password') {
        return '<i class="fa fa-eye"></i>'
      }
      else {
        return '<i class="fa fa-eye-slash"></i>'
      }
    },
    placeholderVal(index) {
      if (index === 0) {
        return "First key"
      }
      else if (index === 1){
        return "Second key"
      }
      else if (index === 2){
        return "Third key"
      }
      else {
        return "Zipfile password (optional)"
      }
    },
    post: function(event) {
      event.preventDefault();

      // Validate and post the form, emit the url
      if (!this.fullFormIsValid){
        // This shouldn't happen, the button is only visible if the form is valid
        return
      }
      console.log("Posting the form");
      var formData = new FormData();
      this.createToken();

      formData.append("retrieve_token", this.sessiontoken);
      formData.append("key_one", this.keys[0]);
      formData.append("key_two", this.keys[1]);
      formData.append("key_three", this.keys[2]);
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
