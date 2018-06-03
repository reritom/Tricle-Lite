const BaseComponent = () => import('./base/base.js');
const HelpTab = () => import('./help/help_tab.js');

export default {
  name: "App",
  components: {
    BaseComponent,
    HelpTab
  },
  data: function () {
    return {
      view: 'app',
      helpbuttonval: '<i class="fa fa-question"></i>'
    }
  },
  methods: {
    toggleView: function() {
      if (this.view === 'app') {
        this.view = 'help';
        this.helpbuttonval = '<i class="fa fa-angle-left"></i>';
      }
      else {
        this.view = 'app';
        this.helpbuttonval = '<i class="fa fa-question"></i>';
      }
    }
  },
  template: `<div>
                  <!-- As a heading -->
                <nav class="navbar navbar-dark bg-dark">
                <span class="navbar-brand mb-0 h1">Tricle by seres</span>
                <span class="mb-0 h2" @click="toggleView()" v-html="helpbuttonval"></span>
                </nav>

                    <div id="BaseView" v-show="view==='app'">
                    <base-component></base-component>
                </div>

                <div id="HelpView" v-show="view==='help'" @click="toggleView()">
                    <help-tab></help-tab>
                </div>
            </div>`
};
