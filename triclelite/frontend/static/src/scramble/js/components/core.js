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
      view: 'app'
    }
  },
  template: `<div class="container">
                <button @click="view='app'">App</button>
                <button @click="view='help'">Help</button>

                <div id="BaseView" v-show="view==='app'">
                    <base-component></base-component>
                </div>

                <div id="HelpView" v-show="view==='help'">
                    <help-tab></help-tab>
                </div>
            </div>`
};
