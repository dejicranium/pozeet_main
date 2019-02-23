import Vue from "vue";
import Conversation from "./Conversation.vue";
import ConvoComment from "./view-converstation-components/ConvoComment";
import axios from "axios";

Vue.config.devtools = true;

new Vue({
  el: "#container",
  components: { comment: ConvoComment },
  delimiters: ["((", "))"],
  render: h => h(Conversation)
});
