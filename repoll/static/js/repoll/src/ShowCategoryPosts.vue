<template>
        <div id="sub-container">
			<div style="margin-bottom:50px;">
				<button style='background-color:teal; color:white; border:none; margin-bottom: 10px; padding: 10px; position:absolute; right:0;' v-if="!categoryAlreadySubscribedTo" @click="subscribeToCategory">Subscribe</button>
				<button style='background-color:teal; color:white; border:none; margin-bottom: 10px; padding: 10px; position:absolute; right:0;' v-else @click="unsubscribeFromCategory">Unsubscribe</button>

			</div>


			<div>
				<reply 
					:activity="activityToReplyTo" 
					:show_reply_modal='showReplyModal'>
				</reply>


				<feed-item v-for="activity in activities" 
					:activity='activity'
					ref='something' 
					:user_logged_in='userLoggedIn'
					:show_comment_modal='showCommentModal'
					@act_close_comment_modal='closeModal'
					@act_show_comment_modal='showCommModal'
					@set_activity_comment_details='setActivityCommentDetails'
					@set_option_comment_details='setOptionCommentDetails'
					@show_auth_modal="showAuthModal"
					@act_show_view_comments_modal='showViewComments'
					@act_show_voters_modal='mShowUsersModal'
					@change_activity_to_refer_to='changeActivityToReferTo'
					:key="'index' + activities.indexOf(activity) + '-' + activity.id"
					@set_activity_respondent_details='setActivityRespondentDetails'
					@set_reply_activity_details='setReplyActivityDetails'>	
				</feed-item>

				<add-new-comment-modal 
					:show_comment_modal='showCommentModal' 
					:activity='activityToCommentOn'
					@close_add_comment_modal='closeModal'
					:option='optionToCommentOn'
					@activity_voted='changeActivityJustVoted'>
				</add-new-comment-modal>

			</div>
			<authentication-modal :activity_to_refer="activity_to_refer" :categories="sortedCategoriesList" :show_authentication_modal="showAuthenticationModal" @close_auth_modal="closeModal"></authentication-modal>	
        </div>
</template>

<script>

var siteUrl = "";
const activityPOSTURL = "";

var categoryId =  document.getElementById('categoryId').innerHTML;

import axios from 'axios';
import Reply from './home-components/Reply.vue';
import FeedItem from './home-components/FeedItem.vue';
import AddComment from './home-components/AddComment.vue';
import AuthenticationModal from './home-components/AuthenticationModal';

export default {
    name: 'ShowCategoryPosts',
    components: {
        "reply": Reply, 
        "feed-item": FeedItem,
		"add-new-comment-modal": AddComment,
      'authentication-modal': AuthenticationModal, 

    },
    
		data(){
			return{
				user: {},

				activity_to_refer: {},
				loading: true,
				loadingMoreContent: false,
				loadingMoreContentFailed: false,
				locations: true,
				sidebarContentSelectedClass: 'sidebar-content-selected',

				activities: [],
				notifications: [],
				categories: [],
				noOfNewNotifications: 0,
			
				categoryAlreadySubscribedTo: false,

				userLoggedIn: false,
				userName: '',
				userPic: '',

				optionToCommentOn: 0,
				activityToReplyTo: {},
				activityToCommentOn: {},

				usersModalUrlToLoad: '',
				
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
				showCreateNewPollModal: false,
				showSubscriptions:false,
				showCreateNewOpinionModal: false,
				activityToGetRespondents: {},
				activityToVoteOn: {},
			}
		},

		computed:{
			sortedSubscriptionsList(){
				var sortedSubscriptions = this._sortCategoryList(this.subscriptions);
				return sortedSubscriptions;
			},

			sortedCategoriesList(){
				var sortedCategories = this._sortCategoryList(this.categories);
				return sortedCategories;
			},
		},

		methods:{
            changeUserData(id, value){
                this.$set(this.user, id, value);
            },
			actShowSubscriptions(newValue){
				this.showSubscriptions = true;
			},
			openSidebar(){
				this.showSidebar = true;
			},

			changeActivityToReferTo(activity){
				this.activity_to_refer = activity;
			},

			loadMoreContent: function(){
				axios.get("" + '/get/latest').then(response=>{
					response.data.activities.forEach(activity=>{
						this.activities.push(activity);
					});
					}).catch(error=>{
						this.loadingMoreContentFailed = true;
					});
			},

			goToNotificationsPage: function(){
				window.open("" +  '/notifications', '_self');
				return ;
			},

			getNoOfNewNotifications: function(){
				var vm = this;
				axios.get("" + '/notifs/' + this.user.id).then(response=>{
					vm.noOfNewNotifications = response.data.unseen;
				});
			},

			openPollsVotedIn: function(){
				window.open("" + '/polls_voted_in/', '_self');

			},

			openProfile: function(){
				window.open("" + '/profile/{{user.id}}/{{user.slug}}', '_self');
			},
			
			_sortCategoryList(list){
				list.sort(function(a, b){
					if (a.categoryName < b.categoryName) return -1;
					if (a.categoryName > b.categoryName) return 1;
				})
				return list;
			},

			getNotifications(){
				var vm = this;
				axios.get("" + '/notifs/' + this.user.id).then(response=>{
					vm.notifications.push(response.data.notifs);
				});
			},

			mShowNewSelectionModal(){
				this.showNewSelectionModal = true; 
			},
		
			mShowUsersModal(urlToLoad){
				this.showUsersModal =  true;
				this.usersModalUrlToLoad = urlToLoad;
			},

			showNewPollModal(){
				if (!this.userLoggedIn){
					this.showAuthenticationModal = true;
					return;
				}
				this.showCreateNewPollModal = true;
			},
			showNewOpinionModal(){
				if (this.userLoggedIn == false){
					this.showAuthenticationModal = true; 
					return ;
				}
				this.showCreateNewOpinionModal = true;
			},
			showViewComments(value){
				this.showViewCommentsModal = true;
			},
			
			toggleSubscriptions(){
			},

			toggleShowCategories(){
				this.showCategories = !this.showCategories;
			},
			toggleAuthModal(intent){

				this.showAuthenticationModal = !this.show_auth_modal;
			},

			closeAddCommentModal(newData){
				this.showCommentModal = newData;
			},


			closeModal(newData){
				this.showCommentModal = false;
				this.showAuthenticationModal = false;
				this.showSidebar = false;
				
				this.showCommentModal == false;
				this.showCreateNewOpinionModal = false;
				this.showCreateNewPollModal = false;
				this.showReplyModal = false;
				
			},

			setActivityCommentDetails(activity){
				this.activityToCommentOn = activity;
			},

			setReplyActivityDetails(activity){
				this.activityToReplyTo = activity;
				this.showReplyModal = true;
			},

			setActivityRespondentDetails(activity){
				this.activityToGetRespondents = activity;
				this.showRespModal();
			},

			setOptionCommentDetails(optionId){
				this.optionToCommentOn = optionId;
			},

			showCommModal(newData){
				this.showCommentModal = true;
			},

			showAuthModal(newData){
				this.showAuthenticationModal = newData;
			},
			
			showRespModal(){
				this.showRespondentsModal = true;
			},

			subscribeToCategory(){
				/**
				var category = this.categories.filter(c=> c.categoryId==categoryId);
				var category = category[0]; //because the above returns a list of one object;
				var categoryIndex = this.categories.indexOf(category); //we need the index of the category so we can remove it from list of categories

				this.subscriptions.push(category);
				this.categories.splice(categoryIndex, 1);**/
				axios.post(activityPOSTURL + "/subscribe/category/" + categoryId).then(response=>{
					this.categoryAlreadySubscribedTo = true;

					window.location.reload();
				});

				
			},

			unsubscribeFromCategory(){
				axios.post(activityPOSTURL + "/unsubscribe/category/" + categoryId).then(response=>{
					this.categoryAlreadySubscribedTo = false;

				});
			},

			goToCategoryPage(categoryId){
				window.open("" + '/polls/category_id=' + categoryId);
			},

			addToActivitiesList(activityObject){
				this.activities.unshift(activityObject);
			},

			changeActivityData(activity, key, value){
				this.$set(activity, key, value);
			},

			changeActivityJustVoted(activityDetailsList){
				var activityId = activityDetailsList[0];
				var optionId = activityDetailsList[1];
				var type = activityDetailsList[2];

				var vm = this;
				var activityInstances = this.activities.filter(a=>a.id==activityId &&a.type==type);
				activityInstances.forEach(function(activity){
					activity.totalVotes += 1;
					vm.$set(activity, 'userHasVoted', true);

					activity.options.forEach(function(option){
						if (option.id == optionId){
							option.score += 1;
						}
					});
				});
                
			},

			getDocHeight() {
    			var D = document;
    			return Math.max(
       		 	D.body.scrollHeight, D.documentElement.scrollHeight,
        		D.body.offsetHeight, D.documentElement.offsetHeight,
        	D.body.clientHeight, D.documentElement.clientHeight
    	);
		},

		},

		//this is what happens when you load the page.
		//automaticall
		created(){
			var vm = this;

			axios.get("" + '/get/polls/category_id=' + categoryId).then(response => {
			//this will give a list of polls
			var response_list = response.data.activities;
			this.activities = response_list;
			this.userName = response.data.userName;
			this.userLoggedIn = response.data.userLoggedIn; 
			this.categoryAlreadySubscribedTo = response.data.userIsSubscribed; 


			
			});
			//get categories data
			axios.get("" + '/categories').then(response => {
				this.categories = response.data.categories;
			});

			//axios.get("" + '/show_subscriptions').then(response => {
			//	this.subscriptions = response.data.subscriptions;
			//});
			

		},

}
</script>

