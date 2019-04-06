<template id='feed-item'>
	<div class="feed-container">
    <!--you will have to re-write the styles. This modal imports from authentication modal-->
    <!--This div will be shown for poll activities -->
		<div class="feed-card" v-if="activity.type=='poll'" tabindex="0" @click="openPoll">
			<div class="poll">
				<div class="trigger" v-if="activity.trigger" style="margin-bottom: 5px; padding:10px; padding-left:25px;">
					<p style="color:darkgrey; font-size:11px;">{{activity.triggerActor}} {{activity.trigger}}</p>
				</div>
				<div class="" v-if="activity.trigger" style="margin-bottom: 5px; padding:10px; display: flex;">
						<button class="follow-btn">Follow</button>
				</div>


				<div class="avatar-and-details">
					<div class="avatar" @click="openUserProfile">
						<img v-if="activity.userPic == null" src="https://www.w3schools.com/howto/img_avatar.png">
						<img v-if="activity.userPic != null" :src="activity.userPic">                    
					</div>

					<div class="details" @click="openUserProfile">
						<p class="name">{{activity.userName}}</p>
						<div class="flex">
							<p class="username">{{activity.username}}</p>
							<p class="">&middot;</p>
							<p class="time-added">{{activity.timeAdded}}</p>
						</div>
					</div>

					<div class="follow" v-if='!activity.userIsFollowing' @click="followUser">
            Follow
					</div>

    <!---
					<div class="feed-card-option" style="display: flex; ">
						<div class="option-dot"></div>
						<div class="option-dot"></div>
						<div class="option-dot"></div>
					</div>
  --->
				</div>
					<!---<i v-if='!userJustFollowed' class="fas fa-user-plus"></i>
													<p @click='followOrUnfollowUser' style='position:absolute; right: 0; margin-right:18px; color: teal;' v-if='!userIsFollowing'>Follow</p>
					-->
				<h6 class="poll-question">
					<a @click.stop @click.exact="openPoll">{{activity.question}}</a>
				</h6>
				<!--poll info -->
				<div class="poll-info">
					<div v-if="infoHasLink != undefined && infoHasLink == null" class="link-info" style="display:flex; padding: 5px;; flex-direction:row; border:0.5px solid lightgrey; border-radius:10px;">
						<img :src="infoLinkThumb" width="150" height="100" style="margin-right:5px;">
						<div style="display:flex; flex-direction:column">
							<h4>{{infoLinkTitle}}</h4>
							<p>{{infoLinkDescription}}</p>
						</div>
					</div>

					<div v-if="activity.info" style="margin-bottom:5px; white-space:;">{{activity.info}}</div>

					<div v-if="activity.imageInfo">
						<img :src="activity.imageInfo" style=" max-width: 100%; max-height:300px; border-radius:10px">
					</div>
				</div>

			<!--if the poll has ended, just show the results already! -->
				<template v-if="!pollHasEnded" @click.stop>
					<!-- this is the default. Shows when the user has not voted -->
					<template v-if="!isPicturePoll">
						<template v-if="!userHasVoted && !seenPollResults">
							<div class="options" v-for="option in activity.options" :option="option" :key="option.id + activity.id">
								<label>
									<input type="radio" @click="optionChosen(option.id)" name="option" :value="option.id">
									<span class="checkmark"></span>
									{{option.option}}
								</label>
							</div>
						</template>
						<!-- once the user has voted, this template will come up! -->
						<!--<template v-else-if='userHasVoted && !isPicturePoll'>
						-->
						<template v-else-if="userHasVoted || seenPollResults" @click.stop>
							<div class="options">
								<div class="ans-cnt" v-for="option in calculatedScores" :option="option" :key="option.id + activity.id">
									<div class="ans">
										<div class="ans-voted">
											<span class="percent">{{option.percent}}</span>
											<span class="txt">{{option.option}}</span>
										</div>
										<span class="first-bg"></span>
										<span :class="{bg:true}" :style="{width: option.percent}"></span>
									</div>
								</div>
							</div>
						</template>
					</template>

					<template v-else @click.stop>
						<template v-if="!userHasVoted && !seenPollResults">
							<div class="picture-options">
								<label v-for="option in activity.options" :option="option">
									<input type="radio" @click="optionChosen(option.id)" name="option" :value="option.id">
									<img :src="option.image">
										<span class="checkbox"></span>
							
										<span>{{option.option}}</span>
								</label>
								</div>
						</template>

						<template v-else-if="userHasVoted || seenPollResults" @click.stop>
							<div class="picture-options">
								<label v-for="option in calculatedScores" :option="option">
									<input type="radio" @click="optionChosen(option.id)" name="option" :value="option.id">
									<img :src="option.image">
									<label style="background-color: rgba(0, 0, 0, .1);" :style="{width:option.percent}">
										<span style="color:black;font-weight:bold;">{{option.percent}} {{option.option}}</span>
									</label>
								</label>
							</div>
						</template>
					</template>
				</template>

				<template v-else @click.stop>
					<template v-if="!isPicturePoll">
						<div class="options">
							<div class="ans-cnt" v-for="option in calculatedScores" :option="option">
								<div class="ans">
									<div class="ans-voted">
										<span class="percent">{{option.percent}}</span>
										<span class="txt">{{option.option}}</span>
									</div>
									<span class="first-bg"></span>
									<span :class="{bg:true}" :style="{width: option.percent}"></span>
								</div>
							</div>
						</div>
					</template>

					<template v-else @click.stop>
						<div class="picture-options">
							<label v-for="option in calculatedScores" :option="option">
								<input type="radio" @click="optionChosen(option.id)" name="option" :value="option.id">
								<img :src="option.image">

								<!--<span class='checkbox' style='opacity:0'></span>-->
								<label style="background-color: rgba(0, 0, 0, .1);" :style="{width:option.percent}">
									<span style="color:black;font-weight:bold;">{{option.percent}} {{option.option}}</span>
								</label>
							</label>
						</div>
					</template>
				</template>

				<div style="display:flex; flex-direction='row'">
					<p class="votes" @click.stop @click.exact="seeVoters">{{totalVotes}} votes</p>
					<span class="middot">&middot;</span>
					<p class="votes" style="color:darkgrey;cursor:pointer;">{{activity.timeRemaining}}</p>
					<span class="middot">&middot;</span>
					<p class="votes" style="color:darkgery;" @click="openPoll">View Comments</p>
				</div>

				<button @click.exact="vote" @click.stop v-show="!userHasVoted && !seenPollResults && !pollHasEnded" id="vote-btn">
					<i class="far fa-check-circle button-icon"></i>Vote
				</button>
				
				<button @click.stop v-on:click.exact="addComment" v-show="!userHasVoted && !seenPollResults" id="comment-btn">
						<i class="far fa-comment button-icon"></i>Comment
				</button>
				
				<button @click.stop v-on:click,exact="seeResults" v-show="!userHasVoted && !seenPollResults && !pollHasEnded">
					<i class="far fa-chart-bar button-icon"></i>Results
				</button>

				<button @click.stop v-on:click.exact="share"><i class="fas fa-share-alt button-icon"></i>Share</button>
					
				<button @click.stop @click.exact="openBreakDownWindow" v-show="userHasVoted || seenPollResults || pollHasEnded">
					<i class="fas fa-chart-pie button-icon"></i>View Breakdown
				</button>                                 
			<!--	<p style='font-weight:bold; font-size:12px;' v-if='activityIsAlreadyLiked'> {{numOfLikes}} likes</p> -->
			</div>

			<div v-show="activity.numOfComments > 0" style="margin-top:5px; padding:5px; text-align:center;vertical-align:middle; border-top:whitesmoke 0.6px solid;">
			<span style="color:darkgrey" @click="viewComments">View Comments</span>
			</div>
		</div>
		<!---
			
					This is the comment div 
					
		-->
		<div class="feed-card" v-else-if="activity.type=='comment'" tabindex="0" @click="openComment">
			<div class="trigger" v-if="activity.trigger" style="margin-bottom: 5px; padding:10px; padding-left:20px; border-bottom: solid 0.3px lightgrey;">
				<p style="color:darkgrey; font-size:11px;">{{activity.triggerActor}} {{activity.trigger}}</p>
			</div>

			<div class="avatar-and-details">
				<div class="avatar" @click="openUserProfile">
					<img v-if="activity.userPic == null" src="https://www.w3schools.com/howto/img_avatar.png">
					<img v-if="activity.userPic != null" :src="activity.userPic">                    
				</div>

				<div class="details" @click="openUserProfile">
					<p class="name">{{activity.commenter}}</p>
					<div class="flex">
						<p class="username">{{activity.username}}</p>
						<p class="">&middot;</p>
						<p class="time-added">{{activity.timeAdded}}</p>
					</div>
				</div>

				<div class="follow" v-if='!activity.userIsFollowing' @click.stop @click.exact="followUser">
					Follow
				</div>
        <!---
				<div class="feed-card-option" style="display: flex; ">
					<div class="option-dot"></div>
					<div class="option-dot"></div>
					<div class="option-dot"></div>
				</div>-->
			</div>

			<div>
				<h2 class="chosen-option" style="font-weight:bold; text-decoration:underline; margin-top: 5px;">{{activity.option_chosen}}</h2>
				<p class="comment" style="white-space:;">{{activity.comment}}</p>

				<div class="comment-question quote" v-if="activity.poll" tab-index="0" @click.stop @click.exact="openPoll">
					<div style="display:flex;">
						<img class="author-pic" :src="activity.poll.userPic" style="margin-right: 5px; border-radius:50%;">
						<div style='display:flex; flex-direction: column'>
							<p class="author-name" style="font-weight:normal; color:teal;">Poll</p>
							<p class="author-name" style="font-size:bold;">{{activity.poll.userName}}</p>
							<p class="question">{{activity.poll.question}}</p>
						</div>
					</div>
				</div>

				<div class="comment-question quote" v-else-if="activity.opinion" tab-index="0" @click.stop @click.exact="openOpinion">
					<div style="display:flex;">
						<img class="author-pic" :src="activity.opinion.userPic" style="margin-right: 5px; border-radius:50%;">
						<div style='display:flex; flex-direction: column'>
							<p class="author-name" style="font-weight:normal; color:teal;">Opinion</p>
							<p class="author-name" style="font-size:bold;">{{activity.opinion.userName}}</p>
							<p class="question">{{activity.opinion.opinion}}</p>
						</div>
					</div>
				</div>
			</div>

			<button @click.stop @click.exact="reply">
				<i class="fas fa-reply button-icon"></i>Reply
			</button>
			<!--<button @click='like' :id="[activityIsAlreadyLiked ? 'activityIsAlreadyLikedClass' : '']"><i class="far fa-thumbs-up button-icon"></i>Like</button> -->
			<!--<button @click="share"><i class="far fa-share-square button-icon"></i>Share</button> -->
		</div>

		<!---

				This is the opinion card 

		-->
		<div class="feed-card" v-else-if="activity.type=='opinion'" tabindex="0" @click="openOpinion">
			<div class="trigger" v-if="activity.trigger" style="margin-bottom: 5px; padding:10px; padding-left:20px; border-bottom: solid 0.3px lightgrey;">
				<p style="color:darkgrey; font-size:11px;">{{activity.triggerActor}} {{activity.trigger}}</p>
			</div>

			<div class="avatar-and-details">
				<div class="avatar" @click="openUserProfile">
					<img v-if="activity.userPic == null" src="https://www.w3schools.com/howto/img_avatar.png">
					<img v-if="activity.userPic != null" :src="activity.userPic">                    
				</div>

				<div class="details" @click="openUserProfile">
					<p class="name">{{activity.userName}}</p>
					<div class="flex">
						<p class="username">{{activity.username}}</p>
						<p class="">&middot;</p>
						<p class="time-added">{{activity.timeAdded}}</p>
					</div>
				</div>

				<div class="follow" v-if='!activity.userIsFollowing' @click="followUser">
					Follow
				</div>
        <!---
				<div class="feed-card-option" style="display: flex; ">
					<div class="option-dot"></div>
					<div class="option-dot"></div>
					<div class="option-dot"></div>
				</div>

        -->
			</div>  


			<div class="comment hideTooMuchText" style="white-space:">{{activity.opinion}}</div>
			<div style="display:flex; flex-direction:row;">
				<img id="opinionContextImage" v-for="image in activity.contextImage" :image="image" :src="image.imgLink" style="max-width:100%; max-height:200px; border-radius:5px; margin-bottom: 5px;" >
			</div>

			<div v-if="activity.contextPageTitle != undefined && activity.contextPageTitle != null" class="link-info" @click.stop style="display:flex; padding: 10px; height:; flex-direction:row; border:0.5px solid lightgrey; border-radius:10px;">
				<img v-if="activity.contextPageThumb" :src="activity.contextPageThumb" width="100" style="margin-right:5px; height: 100%;">
				<img v-else width="100" style="margin-right:5px; height: 100%; background-color: lightgrey;">

				<div style="display:flex; flex-direction:column">
					<h4 style="font-size: 14px; max-height: 70%; text-overflow: ellipsis; word-wrap:break-word;">{{activity.contextPageTitle}}</h4>
					<p style="font-size:11px; ; text-overflow: ellipsis;">{{activity.contextPageDesc}}</p>
				</div>
			</div>
			
			<p class="votes" @click.stop @click.exact="seeVoters">{{activity.numOfComments}} reactions</p>

			<button @click.stop @click.exact="addComment('Agree')" v-if="!activity.userHasVoted">
				<i class="fa fa-check button-icon" aria-hidden="true"></i>Agree
			</button>

			<button @click.stop @click.exact="addComment('Disagree')" v-if="!activity.userHasVoted">
				<i class="far fa-thumbs-down button-icon"></i>Disagree
			</button>

			<button @click.stop @click.exact v-on:click="share"><i class="fas fa-share-alt button-icon"></i>Share</button>
			
			<button @click.stop @click.exact="openBreakDownWindow" v-show="userHasVoted">
				<i class="fas fa-chart-pie button-icon"></i>View Breakdown
			</button>
		</div>

		<div class="feed-card" v-else-if="activity.type=='reply'" tabindex="0">
			<div class="trigger" v-if="activity.trigger" style="margin-bottom: 5px; padding:10px; padding-left:20px; border-bottom: solid 0.3px lightgrey;">
				<p style="color:darkgrey; font-size:11px;">{{activity.triggerActor}} {{activity.trigger}}</p>
			</div>

			<div class="avatar-and-details">
				<div class="avatar" @click="openUserProfile">
					<img v-if="activity.userPic == null" src="https://www.w3schools.com/howto/img_avatar.png">
					<img v-if="activity.userPic != null" :src="activity.userPic">                    
				</div>

				<div class="details" @click="openUserProfile">
					<p class="name">{{activity.userName}}</p>
					<div class="flex">
						<p class="username">{{activity.username}}</p>
						<p class="">&middot;</p>
						<p class="time-added">{{activity.timeAdded}}</p>
					</div>
				</div>

				<div class="follow" v-if='!activity.userIsFollowing' @click="followUser">
					Follow
				</div>
			<!--	<div class="feed-card-option" style="display: flex; ">
					<div class="option-dot"></div>
					<div class="option-dot"></div>
					<div class="option-dot"></div>
				</div>
			</div> -->

			<p class="comment" style="white-space:">{{activity.reply}}</p>

			<div class="comment-question quote" v-if="activity.comment" tab-index="0" @click="openComment">
				<div style="display:flex;">
					<img class="author-pic" :src="activity.comment.userPic" width="26" height="26" style="margin-right: 5px; border-radius:50%;">
					<div style='display:flex; flex-direction: column'>
						<p class="author-name" style="font-weight:normal; color:teal;">Comment</p>
						<p class="author-name" style="font-size:bold;">{{activity.comment.commenter}}</p>
						<p class="question">{{activity.comment.comment}}</p>
					</div>
				</div>
			</div>
			<!-- <button><i class="far fa-thumbs-up button-icon" :id="[activityIsAlreadyLiked? 'activityIsAlreadyLikedClass' : '']" @click='like'></i>Like</button> -->
			<button @click="reply">
			<i class="fas fa-reply button-icon"></i> Reply
			</button>

			<p style="text-decoration:; color:darkgrey; margin-top:5px; font-weight: bold; font-size:13px; text-decoration:;" @click="openViewConversationPage">View conversation</p>
		</div>

		<div class="feed-card" v-else-if="activity.type=='demo'" tabindex="0" style="text-align:center;">
			<div class="trigger" v-if="activity.trigger" style="margin-bottom: 5px; padding:10px; padding-left:20px; border-bottom: solid 0.3px lightgrey;">
					<p style="color:darkgrey; font-size:11px;">{{activity.triggerActor}} {{activity.trigger}}</p>
			</div>

			<div class="author-details">
					<p style="color;black; font-weight:bold; font-size:12px;">{{activity.title}}</p>
			</div>
		
			<canvas :id="'metricsChart' + activity.id" style="width:100%" height="400"></canvas>
		</div>
	</div>
</template>

<script>
import axios from "axios";
var siteUrl = "";
	const activityPOSTURL = "";

var chart1 = "";

export default {
  name: "FeedItem",
  props: [
    "activity",
    "user_logged_in",
    "show_comment_modal",
    "show_view_comments_modal"
  ],
  delimiters: ["((", "))"],
  data() {
    return {
      //these are for the polls.
      pollHasEnded: this.activity.hasEnded,
      isPicturePoll: this.activity.isPicturePoll,
      justVotedScore: 0,
      chosenOption: 0,
      chosenOptionName: this.getChosenOptionName(),
      infoHasLink: this.activity.hasUrlInfo,
      infoLinkThumb: this.activity.infoPageThumb,
      infoLinkTitle: this.activity.infoPageTitle,
      infoLinkDescription: this.activity.infoPageDescription,
      userIsFollowing: this.activity.userIsFollowing,
      seenPollResults: this.activity.userHasSeenResults,

      activityUnliked: false,
      activityIsAlreadyLikedClass: "activityIsAlreadyLikedClass"
    };
  },

  created() {
    this.addShowMoreTextOrNot();
  },

  mounted() {
    if (this.activity.type == "demo") {
      this.getPollMetrics();
    }
  },

  methods: {
    openComment() {
		if (this.activity.comment.comment_id){
			window.open("" + "/view_comment/" + this.activity.comment.comment_id,"_self");
			return 0;
		}
	    window.open("" + "/view_comment/" + this.activity.id, "_self");
    },
    addShowMoreTextOrNot() {
      /**
      var feedText = this.$refs['feedText' + this.activity.id];
      var feedTextHeight = feedText.style.offsetHeight;
      var feedTextScrollHeight = feedText.style.scrollHeight;

      if (feedTextScrollHeight > feedTextHeight){
        feedText.innerText += "show more";
      }
      **/
    },
    showExtraFeedText() {
      /**

      feedText.classList.remove('hideTooMuchText');
      feedText.classList.add('showTooMuchText')
      **/
    },
    openOpinion() {
      //if the opinion we are trying to opinion is embedded in another activity such as the comment
      if (this.activity.opinion.id) {
        window.open(
          "" + "/opinion/" + this.activity.opinion.id + "/",
          "_self"
        );
        return 0;
      }
      //else if not
      window.open("" + "/opinion/" + this.activity.id + "/", "_self");
      return 0;
    },
    openPoll() {
		// if the activity has poll as on object
		// that is, if the activity type is comment 
      	if (this.activity.poll) {
        	window.open("" + "/poll/" + this.activity.poll.id + "/", "_self");
        	return 0;
      	}
      	window.open( "/poll/" + this.activity.id + "/", "_self");
    },

    openViewConversationPage() {
      window.open(
        "" +
          "/view_conversation/conversation_id=" +
          this.activity.conversationId +
          "/reply_id=" +
          this.activity.id,
        "_self"
      );
    },
    openUserProfile() {
      window.open(
        "" +
          "/profile/" +
          this.activity.userId +
          "/" +
          this.activity.userSlug,
        "_self"
      );
    },

    viewComments() {
      	window.open("" + "/poll/" + this.activity.id + "/", "_self");
	},
	
    seeVoters() {
    	var result = true;
    	if (this.user_logged_in == false) {
        	this.$emit("show_auth_modal", result);
        	return 0;
      	}

      else if(this.activity.type=="poll"){
        this.$emit("act_show_voters_modal", "/voters/" + this.activity.id);
      }

		  else if (this.activity.type=="opinion"){
			  this.$emit("act_show_voters_modal", '/opinion_voters/'+ this.activity.id);
		  }
    },
    reply() {
     	var result = true;
      	if (this.user_logged_in == false) {
        	this.$emit("show_auth_modal", result);
        	return 0;
      	}

      	this.$emit("set_reply_activity_details", this.activity);
    },
    followUser(event) {
        var vm = this;
        if (this.user_logged_in == false) {
            this.$emit("change_activity_to_refer_to", this.activity);

            this.$emit("show_auth_modal", true);
        return 0;
        } 
        
        event.target.innerText = "..."
      	    axios.post(activityPOSTURL + "/follow/" + this.activity.userId, {}).then(response => {
        	  this.userJustFollowed = true;
			      this.userIsFollowing = true;
			      event.target.style.display="none";

			if (this.activity.userName){
				vm.showSnackbar("Followed " + this.activity.userName);

			}
			else {
				vm.showSnackbar("Followed " + this.activity.commenter);
			}
		})
		.catch(error=>{
			event.target.innerText = "+";
		});
    },
	
	unfollowUser() {
      	axios.post(activityPOSTURL + "/unfollow/" + this.activity.userId, {}).then(response => {
        	this.userJustFollowed = false;
        	this.userIsFollowing = false;
        });
    },
    followOrUnfollowUser() {
    	var result = result;
    	if (this.user_logged_in == false) {
        	this.$emit("show_auth_modal", result);
        	return 0;
      	}

      	if (!this.userJustFollowed) {
        	this.followUser();
      	} else {
        	this.unfollowUser();
      	}
    },

    openReply() {
      if (this.user_logged_in == false) {
        var result = true;
        this.$emit("show_auth_modal", result);
        return 0;
      }
      this.$emit("act_show_comment_modal", true);
      this.$emit("set_activity_comment_details", this.activity);

      //this will pass the id of the option that was chosen before
      //the comment button was clicked
      this.$emit("set_option_comment_details", {});
    },

    changeActivityData(id, value) {
      this.$set(this.activity.id, value);
    },

    openBreakDownWindow() {
      if (this.user_logged_in == false) {
        this.$emit("show_auth_modal", true);
        return 0;
      }

      if (this.activity.type == "opinion") {
        window.open(
          "" + "/opinion/demographic-metrics/" + this.activity.id,
          "_self"
        );
      } else {
        window.open(
          "" + "/poll/demographic-metrics/" + this.activity.id,
          "_self"
        );
      }
    },

    showViewCommentsModal() {
      this.$emit("act_show_view_comments_modal", true);
    },

    closeModal() {
      this.$emit("act_close_comment_modal", false);
    },

    like(event) {
      var vm = this;
      if (this.user_logged_in == false) {
        this.$emit("show_auth_modal", true);
        return 0;
      }
      event.target.disabled = true;

      if (!this.activity.userHasLiked) {
        if (this.activity.type == "reply") {
          vm.activity.numOfLikes += 1;

          axios
            .post(activityPOSTURL + "/like/", {
              reply_id: vm.activity.id
            })
            .then(function(response) {
              vm.activity.userHasLiked = true;
              event.target.disabled = false;
            })
            .catch(function(error) {
              vm.activity.userHasLiked = false;
              event.target.disabled = false;
            });
        } else if (this.activity.type == "poll") {
          axios
            .post(activityPOSTURL + "/like/", {
              poll_id: vm.activity.id
            })
            .then(function(response) {
              vm.activity.userHasLiked = true;
              vm.activity.numOfLikes += 1;
              event.target.disabled = false;
            })
            .catch(function(error) {
              event.target.disabled = false;
            });
        } else if (this.activity.type == "comment") {
          event.target.disabled = true;

          axios
            .post(activity + "/like/", {})
            .then(function(response) {
              event.target.disabled = false;

              vm.activity.userHasLiked = true;
              vm.activity.numOfLikes += 1;
            })
            .catch(function(response) {
              event.target.disabled = false;
            });
        }
      } else {
        this.unlike(event, this.activity, this.activity.type, this.activity.id);
      }
    },

    unlike(event, activity, activityType, activityId) {
      var vm = this;
      var result = true;
      if (this.user_logged_in == false) {
        this.$emit("show_auth_modal", result);
        return 0;
      }

      if (activityType == "poll") {
        event.target.disabled = true;

        axios
          .post(activityPOSTURL + "/unlike/", {
            poll_id: activityId
          })
          .then(response => {
            event.target.disabled = false;

            vm.activity.userHasLiked = false;
            vm.activityUnliked = true;
            vm.activity.numOfLikes -= 1;
          })
          .catch(function(response) {
            vm.activity.userHasLiked = true;
            event.target.disabled = false;
          });
      } else if ((activityType = "opinion")) {
        event.target.disabled = true;

        axios
          .post(activityPOSTURL + "/unlike/", {
            opinion_id: activityId
          })
          .then(response => {
            event.target.disabled = false;

            vm.activity.userHasLiked = false;
            vm.activity.numOfLikes -= 1;
          })
          .catch(response => {
            event.target.disabled = false;
          });
      } else if (activityType == "comment") {
        event.target.disabled = true;

        axios
          .post(
            activityPOSTURL +
              "/unlike/" +
              {
                comment_id: activityId
              }
          )
          .then(response => {
            event.target.disabled = false;

            vm.activity.userHasLiked = false;
            vm.activity.numOfLikes -= 1;
          })
          .catch(function(response) {
            event.target.disabled = false;
          });
      }
    },
    share() {
      this.$emit("act_show_shareto_modal", true);
      this.$emit("act_set_activity_to_share", this.activity);
    },

    addComment(option) {
      var result = true;
      if (this.user_logged_in == false) {
        var result = true;
        this.$emit("show_auth_modal", result);
        this.$emit("change_activity_to_refer_to", this.activity);
        return 0;
      }

      if (this.chosenOption == 0) {
        //if no option has been chosen
        //check if the activity is an opinion
        if (this.activity.type != "opinion") {
          alert("Select an option");
          return 0;
        }
      }
      if (this.activity.type == "opinion") {
        var activities = this.activity.options.filter(i => i.option == option);
        this.chosenOption = activities[0].id;
      }

      this.$emit("set_activity_comment_details", this.activity);

      //this will pass the id of the option that was chosen before
      //the comment button was clicked
      this.$emit("set_option_comment_details", this.chosenOption);

      this.$emit("act_show_comment_modal", true);
    },

    optionChosen(optionId) {
      this.chosenOption = optionId;
    },

    getChosenOptionName() {
      var chosenOptionId = this.chosenOption;
      for (var i = 0; i < this.activity.options.length; i++) {
        if (this.activity.options[i].id == chosenOptionId) {
          return this.activity.options.option;
        }
      }
    },

    vote() {
      var vm = this;

      if (this.user_logged_in == false) {
        this.$emit("change_activity_to_refer_to", this.activity);

        this.$emit("show_auth_modal", true);
        return 0;
      }

      if (this.chosenOption == 0) {
        //if no option has been chosen
        alert("Select an option");
        return 0;
      }

      this.activity.totalVotes += 1;
      this.activity.userHasVoted = true;

      for (var i = 0; i < this.activity.options.length; i++) {
        if (this.activity.options[i].id == this.chosenOption) {
          this.activity.options[i].score += 1;
          break;
        }
      }

      var pollID = this.activity.id;
      axios
        .post("" + "/vote/", {
          poll_id: pollID,
          option_id: vm.chosenOption
        })
        .then(function(response) {})
        .catch(function(error) {
          vm.userHasVoted = false;
        });
    },

    comment: function() {
      if (this.user_logged_in == false) {
        this.$emit("change_activity_to_refer_to", this.activity);
        this.$emit("show_auth_modal", true);
        return 0;
      }
    },

    seeResults: function() {
      var vm = this;
      var result = true;

      if (this.user_logged_in == false) {
        this.$emit("change_activity_to_refer_to", this.activity);
        this.$emit("show_auth_modal", result);
        return 0;
      }

      axios
        .post("" + "/viewresults", {
          poll_id: this.activity.id
        })
        .then(function(response) {
          vm.seenPollResults = true;
        })
        .catch(function(error) {
          vm.seenPollResults = false;
        });
    },
    getPollMetrics() {
    	var main_focus = this.activity.main_focus;
      	var sub_focus = this.activity.sub_focus;

      	if (main_focus == "gender") {
        	var labels = ["Male", "Female"];
        	var data = [this.activity["M"].votes, this.activity["F"].votes];

		  	this.makePieChart(labels, data);
		
      	} else if (main_focus == "age_range") {
          	var vm = this;
          	var data = []; //The data to be input in the pie chart
          	var labels = [];
          	this.activity.optionTitles.forEach(title => {
            	labels.push(title); //push the titles into the labels list;
        });

			var ages = [];

			//determine the needed ages
			var i = parseInt(this.activity.lowerBound);
			var upperBound = parseInt(this.activity.upperBound) + 1;
			while (i < upperBound) {
				ages.push(i);
				i++;
			}

			//loop through the optionTitles
			this.activity.optionIds.forEach(id => {
			//store the cumulative votes for each title
			var titleVotes = 0;
			//loop through each age, to get the votes for each title
			ages.forEach(age => {
				titleVotes += vm.activity[age][id].votes;
			});
			//push this to the data for the pie chart
			data.push(titleVotes);
			});

        	this.makePieChart(labels, data);
      	}
    },

    makePieChart(aLabels, aData) {
      //destroy a previous chart

      var ctx = document
        .getElementById("metricsChart" + this.activity.id)
        .getContext("2d");

      var options = {
        legend: {
          display: true,
          position: "bottom",
          labels: {
            fontColor: "#333",
            fontSize: 13
          }
        }
      };
      var data = {
        labels: aLabels,
        datasets: [
          {
            data: aData,
            backgroundColor: [
              "#00796B",
              "orange",
              "#C62828",
              "#8D6E63",
              "#8BC34A",
              "#26A69A",
              "#BF360C",
              "green",
              "#1565C0"
            ],
            borderColor: [
              "#00796B",
              "orange",
              "#C62828",
              "#8D6E63",
              "#8BC34A",
              "#26A69A",
              "#BF360C",
              "green",
              "#1565C0"
            ]
          }
        ]
      };

      chart1 = new Chart(ctx, {
        type: "pie",
        data: data,
        options: options
      });
    }
  },

  computed: {
    userHasVoted() {
      return this.activity.userHasVoted;
    },

    contextImageHeight() {
      var contextImage = document.getElementById("opinionContextImage");
      var width = contextImage.style.width;

      contextImage.style.height = width;
    },

    totalVotes() {
      return this.activity.totalVotes;
    },

    activityIsAlreadyLiked() {
      return this.activity.userHasLiked;
    },

    numOfLikes() {
      return this.activity.numOfLikes;
    },

    calculatedScores() {
      if (this.activity.totalVotes == 0) {
        return this.activity.options.map(a => {
          a.percent = "0%";
          return a;
        });
      }
      return this.activity.options.filter(a => {
        if (!isNaN(a.score) && a.score > 0) {
          a.percent =
            Math.round((parseInt(a.score) / this.activity.totalVotes) * 100) +
            "%";
        } else {
          a.percent = "0%";
        }
        return a;
      });
    }
  }
};
</script>

<style scoped>
.chosen-option {
  font-size: 12px;
}

.name {
	font-weight: bold;
}

.username {
	color: darkgrey;
}

.votes {
  margin-right: 0px;
  cursor: pointer;
}
.middot {
  color: grey;
  margin-right: 5px;
  margin-left: 5px;
}
.quote {
  font-size: 14px;
  margin-top: 5px;
  margin-left: 0px;
  margin-bottom: 5px;
  margin-right: 5px;
  color: black;
  padding: 10px;
  display: block;
  border: 0.5px solid lightgrey;
}

.quote img {
	height: 26px; 
	width: 26px;
}
.comment {
  box-sizing: border-box;
  word-wrap: break-word;
  padding-bottom: 2px;
  width: 100%;
  border-radius: 0;
  margin-top: 0;
  margin-bottom: 5px;
  white-space: pre-wrap;
}


.showTooMuchText {
  height: auto;
}

.top-details {
  display: flex;
  flex-direction: row;
  align-items: center;
}
.author-details {
  box-sizing: border-box;
  position: relative;
  display: flex;
  align-items: center;
  flex-wrap: wrap;
}
.author-name {

  display: flex;
  flex-direction: row;
}
.follow-btn-container {
  align-self: flex-end;
}

.name, .username, .time-added, .action {
  line-height: 1.0;
}


.follow-btn {
  font-weight: bold;
  border: 0; 
  background-color: transparent;
  padding: 1px; 
  font-size: 12px;
  cursor: pointer; 
  border: 1px solid black; 

}
 
.follow-icon {
    font-weight: bold; 
    color: teal; 
    font-size: 14px; 
    text-align: center; 
    padding: 2px 7px;
    border-radius: 3px; 
    border: teal 1px solid;
}

    .avatar-and-details {
        display: flex;
		align-items: center;
		
    }

    .avatar {
        margin-right: 10px;
        vertical-align: middle;
    }

    .avatar img {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        vertical-align: middle;
    }

    .details { 
		width: 80%;
	}


    .details p {
        margin-block-start: 3px;
        


    }
    .details .flex {
        display: flex;
    }

    .details .name {
        font-weight: bold;
        font-size: 13px;
        
    }

    .details .flex p {
        font-size: 12px;
        color: darkgrey;
        margin-right: 2px;
    }

	.feed-card-option {
		width: 20px; 
		display: flex; 
		justify-content: space-between;
	}

	.follow {
    padding: 5px 5px;
    text-align: center; 
		vertical-align: middle;
		border-radius: 4px; 
		color: black;
    font-weight: bold;
    font-size: 12px;
		background-color: lightgrey;
	}
	.feed-card-option .option-dot { 
		width: 4px; 
		height: 4px; 
		background-color: lightgrey;
		border-radius: 50%;
	}
</style>
