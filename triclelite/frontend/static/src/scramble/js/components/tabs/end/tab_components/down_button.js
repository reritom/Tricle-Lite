export default {
  name: "DownloadButton",
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
};
