<template>
  <div>
    <div id="container">
      <div id="navbar">
        <div class="menu" v-on:click="openSidebar" v-show="userLoggedIn">
          <div></div>
          <div></div>
          <div></div>
        </div>

        <div class="navbar-actions">
          <!-- if user is not logged in -->
          <ul v-if="userLoggedIn == false" style="float:left;">
            <li
              @click="toggleAuthModal('login')"
              style="color:teal; margin-right:16px; color:teal; font-size:14px; "
            >Sign in / Register</li>
          </ul>
          <!-- if user is logged in -->
          <ul v-if="userLoggedIn">
            <li @click="goToNotificationsPage" style="color:teal">
              <span :data-notifications='noOfNewNotifications'>Notifs</span>
              <span
                class="notification-number"
                v-show="noOfNewNotifications > 0"
              >+ {{noOfNewNotifications}}</span>
            </li>
            <li @click="revealSearchBar" style="color:teal;">
              <span>Search</span>
            </li>
          </ul>
        </div>
      </div>

      <div class="search" v-show="showSearchBar">
        <div class="search__container">
          <input type="text" placeholder="Search keyword">
          <span class="search__button">Search</span>
          <span class="search__button" @click="hideSearchBar">Cancel</span>
        </div>
      </div>

      <div class="body-container">
        <div class="new-post" v-if="userLoggedIn">
          <div @click="showNewOpinionModal">
            <p>What's on your mind?</p>
            <h4>New Opinion</h4>
          </div>

          <div @click="showNewPollModal">
            <p>What's your question?</p>
            <h4>New Poll</h4>
          </div>
        </div>

        <div style="width:20px; height:auto; margin:0 auto;">
          <!---		<img src="..../static/rename.svg" style='moargin:0 auto; width:20px;height:20px;' v-show='loading' /> -->
        </div>
        <sidebar
          :categories="categories"
          :toggle_show_categories="toggleShowCategories"
          @close_modal="closeModal"
          :show_sidebar="showSidebar"
          :user="user"
        ></sidebar>
        <feed-item
          v-for="activity in activities"
          :activity="activity"
          :user_logged_in="userLoggedIn"
          :show_comment_modal="showCommentModal"
          @act_close_comment_modal="closeModal"
          @act_show_comment_modal="showCommModal"
          @set_activity_comment_details="setActivityCommentDetails"
          @set_option_comment_details="setOptionCommentDetails"
          @show_auth_modal="showAuthModal"
          @act_show_view_comments_modal="showViewComments"
          @act_show_voters_modal="mShowUsersModal"
          @act_show_shareto_modal="showShareToModal"
          @change_activity_to_refer_to="changeActivityToReferTo"
          :key="'index' + activities.indexOf(activity) + '-' + activity.id"
          @set_activity_respondent_details="setActivityRespondentDetails"
          @act_set_activity_to_share="setActivityToShare"
          @set_reply_activity_details="setReplyActivityDetails"
        ></feed-item>
        <users-modal
          :show_users_modal="showUsersModal"
          :url_to_load="usersModalUrlToLoad"
          @act_close_users_modal="closeModal"
        ></users-modal>

        <new-opinion-modal
          :show_opinion_modal="showCreateNewOpinionModal"
          @act_add_to_activities="addToActivitiesList"
          @close_new_opinion_modal="closeModal"
        ></new-opinion-modal>

        <share-to-modal
          :show_shareto_modal="showShareToModal_"
          @act_close_shareto_modal="closeModal"
          :activity="activityToShare"
        ></share-to-modal>

        <add-new-comment-modal
          :show_comment_modal="showCommentModal"
          :activity="activityToCommentOn"
          @close_add_coment_modal="closeModal"
          :option="optionToCommentOn"
          @act_add_to_activities="addToActivitiesList"

          @activity_voted="changeActivityJustVoted"
        ></add-new-comment-modal>

        <reply
          :activity="activityToReplyTo"
          :show_reply_modal="showReplyModal"
          @close_modal="closeModal"
        ></reply>

        <authentication-modal
          :activity_to_refer="activity_to_refer"
          :categories="sortedCategoriesList"
          :show_authentication_modal="showAuthenticationModal"
          @close_auth_modal="closeModal"
        ></authentication-modal>
        <show-new-poll-modal
          :show_new_poll_modal="showCreateNewPollModal"
          :categories="sortedCategoriesList"
          @act_add_to_activities="addToActivitiesList"

          @close_new_poll_modal="closeModal"
        ></show-new-poll-modal>
        <comments :show_view_comments_modal="showViewCommentsModal"></comments>

        <div
          style="width:20px; height:auto; margin:0 auto; display:none;"
          v-show="loadingMoreContent"
        >
          <img src="https://s3.us-east-2.amazonaws.com/pozeet-static/rename.svg" style="margin:0 auto; width:20px;height:20px;">
        </div>

        <div v-if="!loadingMoreContent || loadingMoreContentFailed" style="text-align:center;">
          <button class="show-more-btn" style="font-size:12px;" @click="loadMoreContent">Show More</button>
        </div>
      </div>

      <div id="snackbar"></div>
    </div>
  </div>
</template>




<script>
import axios from "axios";
import Chart from "chart.js";
import Reply from "./home-components/Reply.vue";
import AddComment from "./home-components/AddComment.vue";
import AuthenticationModal from "./home-components/AuthenticationModal.vue";
import Comments from "./home-components/Comments.vue";
import FeedItem from "./home-components/FeedItem.vue";
import NewOpinion from "./home-components/NewOpinion.vue";
import NewPoll from "./home-components/NewPoll.vue";
import UsersModal from "./home-components/UsersModal.vue";
import Sidebar from "./home-components/Sidebar.vue";
import ShareToModal from "./home-components/ShareToModal";

const siteUrl = "";
const userId = document.getElementById("user-id-signifier").innerHTML;
const userSlug = document.getElementById("user-slug-signifier").innerHTML;

export default {
  name: "App",
  delimiters: ["((", "))"],
  components: {
    reply: Reply,
    sidebar: Sidebar,
    "feed-item": FeedItem,
    "users-modal": UsersModal,
    "new-opinion-modal": NewOpinion,
    "add-new-comment-modal": AddComment,
    "authentication-modal": AuthenticationModal,
    "show-new-poll-modal": NewPoll,
    "comments": Comments,
    "share-to-modal": ShareToModal
  },

  data: function() {
    return {
      msg: "what",
      user: {},

      activity_to_refer: {},
      loading: true,
      loadingMoreContent: false,
      loadingMoreContentFailed: false,
      locations: true,
      sidebarContentSelectedClass: "sidebar-content-selected",

      //search data
      showSearchBar: false,
      searchText: "",
      //activities, notification and categories
      activities: [],
      notifications: [],
      categories: [],
      noOfNewNotifications: 0,

      userLoggedIn: null, 		//set to null so it doesn't appear when getting data
      userName: "",
      userPic: "",

      optionToCommentOn: {},
      activityToReplyTo: {},
      activityToCommentOn: {},

      usersModalUrlToLoad: "",

      showUsersModal: false,
      showNotificationModal: false,
      showRespondentsModal: false,
      showNewSelectionModal: false,
      showAuthenticationModal: false,
      showReplyModal: false,
      showCommentModal: false,
      showSidebar: false,
      showCategories: false,
      showViewCommentsModal: false,
      showShareToModal_: false,

      showCreateNewPollModal: false,
      showCreateNewOpinionModal: false,
      activityToGetRespondents: {},
      activityToVoteOn: {},
      activityToShare: null,

      xhrPageId: 1
    };
  },

  computed: {
    sortedCategoriesList() {
      var sortedCategories = this._sortCategoryList(this.categories);
      return sortedCategories;
    }
  },

  methods: {
    setActivityToShare(activity) {
      this.activityToShare = activity;
    },
    changeUserData(id, value) {
      this.$set(this.user, id, value);
    },

    openSidebar() {
      this.showSidebar = true;
    },
    revealSearchBar() {
      this.showSearchBar = true;
      //add different margin bottom to the navbar
      var navbar = document.getElementById("navbar");
      navbar.style.marginBottom = "0px";
    },
    hideSearchBar() {
      this.showSearchBar = false;
    },

    changeActivityToReferTo(activity) {
      this.activity_to_refer = activity;
    },

    loadMoreContent: function() {
      this.loadingMoreContent = true;
      axios
        .get("/get/latest/?page=" + this.xhrPageId)
        .then(response => {
          this.xhrPageId += 1;
          this.loadingMoreContent = false;
          response.data.activities.forEach(activity => {
            this.activities.push(activity);
          });
        })
        .catch(error => {
          this.loadingMoreContentFailed = true;
        });
    },

    goToNotificationsPage: function() {
      window.open( "/notifications", "_self");
      return;
    },

    getNoOfNewNotifications: function() {
      var vm = this;
      axios.get("" + "/notifs/" + userId).then(response => {
        vm.noOfNewNotifications = response.data.unseen;
      });
    },

    openPollsVotedIn: function() {
      window.open("" + "/polls_voted_in/", "_self");
    },

    _sortCategoryList(list) {
      list.sort(function(a, b) {
        if (a.categoryName < b.categoryName) return -1;
        if (a.categoryName > b.categoryName) return 1;
      });
      return list;
    },

    getNotifications() {
      var vm = this;
      axios.get("" + "/notifs/" + userId).then(response => {
        vm.notifications.push(response.data.notifs);
      });
    },

    showShareToModal() {
      this.showShareToModal_ = true;
    },

    mShowNewSelectionModal() {
      this.showNewSelectionModal = true;
    },

    mShowUsersModal(urlToLoad) {
      this.showUsersModal = true;
      this.usersModalUrlToLoad = urlToLoad;
    },

    showNewPollModal() {
      if (!this.userLoggedIn) {
        this.showAuthenticationModal = true;
        return;
      }
      this.showCreateNewPollModal = true;
    },
    showNewOpinionModal() {
      if (this.userLoggedIn == false) {
        this.showAuthenticationModal = true;
        return;
      }
      this.showCreateNewOpinionModal = true;
    },

    showViewComments(value) {
      this.showViewCommentsModal = true;
    },

    toggleShowCategories() {
      this.showCategories = !this.showCategories;
    },
    toggleAuthModal(intent) {
      this.showAuthenticationModal = !this.show_auth_modal;
    },

    closeAddCommentModal(newData) {
      this.showCommentModal = newData;
    },

    closeModal(newData) {
      this.showCommentModal = false;
      this.showAuthenticationModal = false;
      this.showSidebar = false;
      this.showCommentModal == false;
      this.showCreateNewOpinionModal = false;
      this.showCreateNewPollModal = false;
      this.showReplyModal = false;
      this.showShareToModal_ = false;
      this.showUsersModal = false;
    },

    setActivityCommentDetails(activity) {
      this.activityToCommentOn = activity;
    },

    setReplyActivityDetails(activity) {
      this.activityToReplyTo = activity;
      this.showReplyModal = true;
    },

    setActivityRespondentDetails(activity) {
      this.activityToGetRespondents = activity;
      this.showRespModal();
    },

    setOptionCommentDetails(optionId) {
      this.optionToCommentOn = optionId;
    },

    showCommModal(newData) {
      this.showCommentModal = true;
    },

    showAuthModal(newData) {
      this.showAuthenticationModal = newData;
    },

    showRespModal() {
      this.showRespondentsModal = true;
    },

    goToCategoryPage(categoryId) {
      window.open("" + "/polls/category_id=" + categoryId);
    },

    addToActivitiesList(activityObject) {
      this.activities.unshift(activityObject);
    },

    changeActivityData(activity, key, value) {
      this.$set(activity, key, value);
    },

    changeActivityJustVoted(activityDetailsList) {
      var activityId = activityDetailsList[0];
      var optionId = activityDetailsList[1];
      var type = activityDetailsList[2];

      var vm = this;
      var activityInstances = this.activities.filter(
        a => a.id == activityId && a.type == type
      );
      activityInstances.forEach(function(activity) {
        activity.totalVotes += 1;
        vm.$set(activity, "userHasVoted", true);

        activity.options.forEach(function(option) {
          if (option.id == optionId) {
            option.score += 1;
          }
        });
      });
    },

    getDocHeight() {
      var D = document;
      return Math.max(
        D.body.scrollHeight,
        D.documentElement.scrollHeight,
        D.body.offsetHeight,
        D.documentElement.offsetHeight,
        D.body.clientHeight,
        D.documentElement.clientHeight
      );
    }
  },

  //this is what happens when you load the page.
  //automaticall
  created() {
    this.getNoOfNewNotifications();

    var vm = this;
    axios.get("" + "/get/latest/?page=" + vm.xhrPageId).then(response => {
      //this will give a list of polls
      var response_list = response.data.activities;
      this.activities = response_list;
      this.userName = response.data.userName;
      this.userPic = response.data.userPic;
      this.userLoggedIn = response.data.user_logged_in;
      this.loading = false;
      this.loadingMoreContent = false;

      //increase xhrPageId
      vm.xhrPageId += 1;
    });

    //get categories data
    axios.get("" + "/categories").then(response => {
      this.categories = response.data.categories;
    });

    axios.get("" + "/user/details/" + userId).then(response => {
      this.changeUserData("id", response.data.id);
      this.changeUserData("slug", response.data.slug);
      this.changeUserData("userPic", response.data.userPic);
      this.changeUserData("fullname", response.data.userName);
      this.changeUserData("userPic", response.data.userPic);
      this.changeUserData("num_of_followed", response.data.num_of_followed);
      this.changeUserData("num_of_followers", response.data.num_of_followers);
    });

    window.onscroll = () => {
      var loader = document.getElementById("loadingMoreContent");
      var scrollTop =
        window.pageYOffset ||
        (document.documentElement || document.body.parentNode || document.body)
          .scrollTop;
      var winheight =
        window.innerHeight ||
        (document.documentElement || document.body).clientHeight;
      var docHeight = this.getDocHeight();
      var trackLength = docHeight - winheight;
      var pctScrolled = Math.floor((scrollTop / trackLength) * 100); // gets percentage scrolled (ie: 80 or NaN if tracklength == 0)

      if (pctScrolled == 95) {
        this.loadingMoreContent = true;

        axios
          .get("" + "/get/latest/?page=" + this.xhrPageId)
          .then(response => {
            this.xhrPageId += 1;
            this.loadingMoreContent = false;
            response.data.activities.forEach(activity => {
              this.activities.push(activity);
            });
          })
          .catch(error => {
            this.loadingMoreContentFailed = true;
          });
        console.log(pctScrolled);
      }
    };
  }
};
</script>

<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

h1,
h2 {
  font-weight: normal;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #42b983;
}

.notification-number {
  color: red;
}

.search {
  background-color: white;
  padding: 5px 5px;
  margin-bottom: 20px;
  box-sizing: border-box;
}

.search__container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-sizing: border-box;
}

.new-post {
  margin-bottom: 10px;
}

.search__container input {
  border: 1px whitesmoke solid;
  border-radius: 4px;
  min-height: 30px;
  padding-left: 10px;
}

.search__container span {
  padding: 5px 5px;
  background-color: grey;
  opacity: 0.5;
  color: white;
  cursor: pointer;
}

.show-more-btn {
  color: white; 
  border: 0; 
  background-color: teal;
  border-radius: 3px;
  padding: 2px;
  
}
</style>

<style>
