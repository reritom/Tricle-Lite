const DownloadButton = () => import('./tab_components/down_button.js');
const DoneButton = () => import('./tab_components/done_button.js');

export default {
  name: "EndTab",
  components: {
    DownloadButton,
    DoneButton
  },
  props: ['url', 'sessiontoken'],
  template: `<div>
            <div class="flex-container-row">
              <download-button :url="url" :sessiontoken="sessiontoken" v-on:refreshpulse="$emit('refreshpulse')"></download-button>
              <done-button :url="url" v-on:refreshpulse="$emit('refreshpulse')"></done-button>
            </div>
            </div>`
};
