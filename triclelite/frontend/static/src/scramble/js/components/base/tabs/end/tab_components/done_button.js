export default {
  name: "DoneButton",
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
};
