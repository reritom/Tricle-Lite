const FormTab = () => import('./tabs/form/form_tab.js');
const StartButton = () => import('./tabs/start/start_button.js');
const EndTab = () => import('./tabs/end/end_tab.js');

export default {
  name: "App",
  components: {
    FormTab,
    StartButton,
    EndTab
  },
  data: function () {
    return {
      view: 'notstarted',
      sessiontoken: "",
      url: ""
    }
  },
  template: `<div class="container">

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
};
