<template>
      
    <div id='body-container'>
        <div id="follow-btn-container" v-if='!user.user_is_self'>   
			<button class='follow-btn' @click='unfollowUser' v-show="userIsFollowing">Unfollow</button>
			<button class='follow-btn' @click='followUser' v-show="!userIsFollowing">Follow</button>
		
        </div>
            <div class="follow-details">
                <div class="following f-detail">
                    <p class="figure" >{{user.num_of_followed}}</p>

                    <p> following</p>
                </div>

                <div class="followers f-detail" @click="mShowUsersModal('/followers')">
                    <p class="figure" id='followers_number'>{{user.num_of_followers}} </p>
					<p>followers</p>
                </div>
            </div>

                <div class="other-details">
                     <div class="tab-header">
                       
                        <div class="tab poll" onclick="showTabContent(this, 'polls')">
                            <p>Polls</p>
                        </div>

                        <div class="tab" onclick="showTabContent(this, 'opinions')" @click='getPosts'>
                            <p>Opinions</p>
                        </div>

                        <div class="tab" onclick="showTabContent(this, 'c_and_s')" @click='getCommentsAndReplies'>
                            <p>Comments & Replies</p>
                        </div>

                        <div class="tab" onclick="showTabContent(this, 'l_and_s')" @click='getLikesAndShares'>
                            <p>Likes & Shares</p>
                        </div>
                        
                    </div>

                    <div class='tab-content'>
                        <div id="polls" class='t-content'>
                            <feed-item v-for='activity in activities.polls' :activity='activity'
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
			@set_activity_respondent_details='setActivityRespondentDetails'
			@set_reply_activity_details='setReplyActivityDetails'></feed-item>
                        </div>

                        <div id='opinions' class='t-content'>
                            <feed-item v-for='activity in activities.opinions' :activity='activity'
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
			@set_activity_respondent_details='setActivityRespondentDetails'
			@set_reply_activity_details='setReplyActivityDetails'                            
                            ></feed-item>
                        </div>


                        <div id='c_and_s' class='t-content'>
                            <feed-item v-for='activity in activities.c_and_s' :activity='activity'
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
			@set_activity_respondent_details='setActivityRespondentDetails'
			@set_reply_activity_details='setReplyActivityDetails'
                            ></feed-item>
                        </div>

                        <div id='l_and_s' class='t-content'>
                            <feed-item v-for='activity in activities.l_and_s' :activitiy='activity'
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
			@set_activity_respondent_details='setActivityRespondentDetails'
			@set_reply_activity_details='setReplyActivityDetails'>
            </feed-item>
                        </div>

                    </div>


                </div>
		<add-new-comment-modal 
		:show_comment_modal='showCommentModal' 
		:activity='activityToCommentOn'
		@close_add_coment_modal='closeModal'
		:option='optionToCommentOn'
		@activity_voted='changeActivityJustVoted'>
		</add-new-comment-modal>
	
		<reply 
			:activity="activityToReplyTo" 
			:show_reply_modal='showReplyModal'
			@close_modal='closeModal'>
		</reply>

		<users-modal :show_users_modal="showUsersModal" :url_to_load="usersModalUrlToLoad">

		</users-modal>
        </div>
</template>

<script>

    var userId = parseInt(document.getElementById('userId').innerHTML);
var siteUrl = "";
	const activityPOSTURL = "";


import FeedItem from './home-components/FeedItem.vue';
import AddComment from "./home-components/AddComment.vue";
import Reply from "./home-components/Reply.vue";
import UserModal from './home-components/UsersModal.vue';

import axios from 'axios';
export default {
    name: "Profile", 
    components: {'feed-item': FeedItem,
                'add-new-comment-modal': AddComment,
				'reply': Reply,
				'users-modal': UserModal},
    data(){
        return {

			//show users modal?

            activities: {
                polls: [],
                opinions: [],
                c_and_s: [],
                l_and_s: [],
            },
            likesAndShares: [],
            commentsAndReplies: [],
			num_of_followers: 0,
            is_following: false,
            user: {}, 
            followText: '',
            userIsFollowing: null,
					
				activity_to_refer: {},
				loading: true,
				loadingMoreContent: false,
				loadingMoreContentFailed: false,
				locations: true,
				sidebarContentSelectedClass: 'sidebar-content-selected',
				notifications: [],
				categories: [],
				noOfNewNotifications: 0,

				userLoggedIn: false,
				userName: '',
				userPic: '',

				optionToCommentOn: {},
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
				showCreateNewOpinionModal: false,
				activityToGetRespondents: {},
				activityToVoteOn: {},					
					

            }

                
        },
    methods:{			

        changeUserData(id, value){
            this.$set(this.user, id, value);
            	
		},
        changeActivitiesData(id, value){
            this.$set(this.activities, id, value);
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
				axios.get("" + '/notifs/' + userId).then(response=>{
					vm.noOfNewNotifications = response.data.unseen;
				});
			},

			openPollsVotedIn: function(){
				window.open("" + '/polls_voted_in/', '_self');

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
				axios.get("" + '/notifs/' + userId).then(response=>{
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

		followUser(event){
            var vm = this;
            event.target.disabled = true;
			axios.post(activityPOSTURL + "/follow/" + userId, {
			}).then(response =>{
                vm.user.num_of_followers +=1;
                vm.userIsFollowing = true;
                event.target.disabled = false;
			}).catch(error=>{
                event.target.disabled = false;
            });

		},

		unfollowUser(event){
            var vm = this;
            event.target.disabled = true;
			axios.post(activityPOSTURL + "/unfollow/" + userId, {}).then(response=>{

            }).then(response=>{
                vm.user.num_of_followers -= 1;
                vm.userIsFollowing = false;
                event.target.disabled = false;
            }).catch(error=>{
                event.target.disabled = false;
            });
        },
        
        followOrUnfollowUser(){
            if (this.userIsFollowing){
                this.unfollowUser();
            }
            else{
                this.followUser();
            }
        },


        getCommentsAndReplies(){
			if (this.activities.c_and_s.length < 1){
                	axios.get("" + '/comments_and_replies/user_id=' + userId).then(response=> {						
                        this.changeActivitiesData('c_and_s', response.data.c_and_s);
                    });
				}
            },

            getLikesAndShares(){
                axios.get("" + '/likes_and_shares/user_id=' + userId).then(response => {
                    this.changeActivitiesData('l_and_s', response.data.l_and_s);
                });
            },
                getPosts(){
                    //if there are no opinions already
                    if (this.activities.opinions.length < 1){
                        axios.get("" + '/posts/user_id=' + userId).then(response => {
                            this.changeActivitiesData('opinions', response.data.opinions);
							//this.activities.opinions = [],
                            //this.activities.opinions = response.data.opinions;
                        });
                    }
                },

            },

            created(){
                var vm = this;
				//get number of followers 
                axios.get("" + '/polls/user_id=' + userId).then(response =>{
                    vm.changeActivitiesData('polls', response.data.activities.polls);
                
                });

				axios.get("" + '/user/details/' + userId).then(response=>{
					vm.is_following = response.data.is_following;
                    vm.changeUserData('num_of_followed', response.data.num_of_followed);
					 vm.changeUserData('num_of_followers', response.data.num_of_followers); 
					 vm.changeUserData('user_is_self', response.data.user_is_self);               
                    vm.userIsFollowing = response.data.is_following;
                    vm.userLoggedIn = response.data.userLoggedIn;
                });
            
            },
    

        }

</script>

<style scoped>
    #follow-btn-container{
        text-align: center;
    }
</style>

