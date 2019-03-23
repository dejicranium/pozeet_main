<template id="notification-template">
  <div id='sub-container'>
    <div
      class="notification-card"
      v-for="notification in notifications"
      :notification="notification"
      tabindex="0"
      :key="notification.url"
      @click="goToNotificationOrigin(notification.url)"
    >
      <p v-html="notification.text"></p>
    </div>
  </div>
</template>


<script>
import vue from "vue";
import axios from "axios";

var userId = document.getElementById("user-id-signifier").innerHTML;
var siteUrl = "";

export default {
  name: "Notification",
  data() {
    return {
      notifications: [],
      unseenNotifications: []
    };
  },

  methods: {
    flattenUnseenNotifications() {
      this.unseenNotifications = this.unseenNotifications.join(",");
    },
    getNotifications() {
      var vm = this;
      axios.get("" + "/notifs/" + userId).then(response => {
        vm.notifications = response.data.notifs;
        vm.unseenNotifications = response.data.unseenNotifs;

        if (vm.unseenNotifications != []) {
          vm.flattenUnseenNotifications();

          axios.post("" + "/mark-as-seen", {
            notifications: vm.unseenNotifications
          });
        }
      });
    },

    markNotificationsAsSeen() {
      this.flattenUnseenNotifications();
      alert(this.unseenNotifications);
      var vm = this;
    },

    //takes you to the page where the notification originated from
    goToNotificationOrigin(notificationUrl){
        window.open("" + notificationUrl, '_self');
    }
  },

  created() {
    this.getNotifications();
  }
};
</script>


<style scoped>
.notification-card {
  background-color: white;
  padding: 30px 16px;
  box-shadow: lightgrey 1px;
  border-radius: 2px;
  border: 0.3px solid lightgray;
  font-size: 14px;
  margin-bottom: 2px;
}
</style>






