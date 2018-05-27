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
      helpbuttonval: 'Help'
    }
  },
  methods: {
    toggleView: function() {
      if (this.view === 'app') {
        this.view = 'help';
        this.helpbuttonval = 'Back to app';
      }
      else {
        this.view = 'app';
        this.helpbuttonval = 'Help';
      }
    }
  },
  template: `<div>
                  <!-- As a heading -->
                <nav class="navbar navbar-dark bg-dark">
                <span class="navbar-brand mb-0 h1">Tricle</span>
                <span class="mb-0 h2">Tricle</span>
                </nav>

                <div id="nav">
                  <div id="brand">Tricle - a SERES product</div>

                  <div id="help">
                    <button @click="toggleView()">{{helpbuttonval}}</button>
                  </div>
                </div>

                <div id="BaseView" v-show="view==='app'">
                    <base-component></base-component>
                </div>

                <div id="HelpView" v-show="view==='help'" @click="toggleView()">
                    <help-tab></help-tab>
                </div>
            </div>`
};
