<template>
<div>
	<div class="tab-header">
		<div class="tab polls" @click="changeActivityToShow('polls')">
			<p>>Poll</p>
		</div>
		<div class="tab opinions" @click="changeActivityToShow('opinions')">
			<p>Opinion</p>
		</div>
		<div class="tab comments" @click="changeActivityToShow('comments')">
			<p>Comments</p>
		</div>
	</div>

	<div class="trending-body">
		<!-- for each type of content -->
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
          	@set_reply_activity_details="setReplyActivityDetails">
		</feed-item>

	</div>
</div>
</template>



<script>
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

	import axios from "axios";
	export default {
		name: 'Trending',
		components: {
			'feed-item': FeedItem,

		},
		data(){
			return {
				activitiesList: [],
				activitiesToShow: 'polls',
				userLoggedIn: null,
				//this denotes the page that should be gotten: pagination
				// the default is 1
				pollPage: 1, 
				opinionPage: 1, 
				commentsPage: 1, 
			}
		},
		computed: {
			activities(){
				if (this.activitiesToShow == "polls"){
					var polls = activitiesList.filter(activity=>activity.type=="poll");
					return polls;
				}
				else if (this.activitiesToShow == "comments") {
					var comments = activitiesList.filter(activity=>activity.type=="comment");
					return comments;
				}
				else if (this.activitiesToShow == "opinions") {
					var opinions = activitiesList.filter(activity=>activity.type=="opinion");
				}
			}
		},
		created() {
			//always load the polls first, as we assume that is the entry point.
			this.getPolls();
		},
		methods: {
			makeTabActive(activityType){
				/** 
				 * Indicates the active tab and puts a colored border-bottom to signify which tab is active
				 * We know the tab that is active through the 'activeType' parameter
				 * The name of the activityType is also the class of the tab, this method makes it useful in the 'changeActivityToShow' function
				*/

				// first make sure that the other tabs don't have a colored border bottom;
				var tabs = document.getElementsByClassName('tab');
				tabs.forEach(tab=>{
					tab.style.borderBottom = "0px";
				});

				// go ahead to give the selected tab a border bottom;
				var tab = document.getElementsByClassName(activityType)[0];
				tab.style.borderBottom = "2px teal solid";
			},

			changeActivityToShow(activityType){
				//make sure that the tab that has just being clicked is made active
				this.makeTabActive(activityType);

				// the activitiesToShow enables our computed property "activities" to change. 
				// this will tell the feed-item component the kind of activities to show;
				this.activitiesToShow = activityType;
			},
			getPolls() {
				var vm = this; 
				//always load the polls first, as we assume that is the entry point.
				axios.get("/trending_polls").then(response=>{
					vm.activitiesList.push(response.data.polls);
				});
			},
			getOpinions(){
				var vm = this; 
				axios.get("/trending_opinions").then(response=>{
					vm.activitiesList.push(response.data.opinions);
				});
			},
			getComments(){
				var vm = this; 
				axios.get("/trending_comments").then(response=>{
					vm.activitiesList.push(response.data.comments);
				});
			},
			showCommModal(newData) {
				this.showCommentModal = true;
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
			addToActivitiesList(activityObject) {
      			this.activities.unshift(activityObject);
			},
			showAuthModal(newData) {
				this.showAuthenticationModal = newData;
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
			closeAddCommentModal(newData) {
				this.showCommentModal = newData;
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
			setActivityToShare(activity) {
				this.activityToShare = activity;
			},
			changeUserData(id, value) {
				this.$set(this.user, id, value);
			},
		}
	}

</script>

<style scoped>
	.tab-header{
		display: flex;
		flex-direction: row;
		box-shadow: 0 4px 2px -2px lightgray;
		justify-content: space-evenly;
		flex-wrap: wrap;

	}

	.tab{
		padding: 10px 10px 10px 5px;
		font-size: 12px;
		text-align: center;
		cursor: pointer;
		font-weight: 500;
		min-width: 20px;
		font-weight: 200;
	}

	.trending-body {
		margin-top: 10px;
	}


</style>
