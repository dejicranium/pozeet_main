	<template id='comment-template'>
  <div class="body-container">
    <div class="comment-card" :id="[isInnerReply? 'innerReply' : '']">
      <div class="avatar" @click="openUserProfile">
        <img v-if="reply.userPic == null" src="https://www.w3schools.com/howto/img_avatar.png">
        <img v-else :src="reply.userPic">
      </div>

      <div class="beside-avatar-box">
          <div class="author-details" @click="openUserProfile">
              <p class="name" style="font-weight:bold; margin-right:5px; font-size: 13px; display:inline;">{{reply.userName}}</p>
              <p class="name" style="margin-right:5px; color:darkgrey; font-size: 13px; display:inline;">({{reply.username}})</p>
              <p class="name" style="color:darkgrey; font-size: 13px; display:inline;">{{reply.timeAdded}}</p>
              <div style="display:block;">
                  <p v-if="isInnerReply" style="color:lightgrey; font-size:13px;">Replying to {{reply.userRepliedTo}}</p>
              </div>
          </div>
        <div class="reason">
          <p class="comment">{{reply.reply}}</p>
        </div>

        <button
          v-if="!showReplyReplies && reply.numOfReplies > 0"
          style="font-size:13px; color:teal; background-color:transparent;border:0;"
          @click="getReplyReplies"
        >Show Replies</button>
        <p
          v-if="showReplyReplies"
          style="font-size:13px; color:teal;"
          @click="showReplyReplies = false"
        >Hide replies</p>

        <div class="action-buttons">
          <button @click="addReply">Reply</button>

          <!--<button>Like</button> -->
          <!-- <button >Share </button> -->
        </div>
      </div>
    </div>
    <div class="addReplyReplyBox" v-show="intent == 'toReplyReply'">
      <form id="comment-form">
        <textarea
          type="text"
          v-model="replyReplyText"
          placeholder="Reply"
          @click="autoResize"
          name="reply"
          id="comment-form"
        ></textarea>
        <button type="button" @click="replyReply">Reply</button>
      </form>
    </div>

    <div style="padding-left: 20px;">
      <convo-comment v-show="showReplyReplies" v-for="reply in replyReplies" :reply="reply"></convo-comment>
    </div>
  </div>
</template>



<script>
import axios from "axios";
var siteUrl = "";
const activityPOSTURL = "";

//import ConvoComment from './ConvoComment';
export default {
  name: "convo-comment",
  props: ["reply"],
  data() {
    return {
      numOfShares: this.reply.numOfShares,
      numOfLikes: this.reply.numOfShares,
      intent: "",
      replyReplyText: "",
      replyReplies: [],
      showReplyReplies: false,
      isInnerReply: this.reply.type == "replyReply"
    };
  },
  computed: {
    commentClass() {
      return this.isInnerReply ? "innerReply" : "";
    }
  },

  methods: {
    autoResize(event) {
      event.preventDefault();
      var textarea = event.target;
      textarea.addEventListener("input", function() {
        var currentHeight = textarea.offsetHeight;
        var scrollHeight = textarea.scrollHeight;
        if (scrollHeight > currentHeight) {
          textarea.style.height = scrollHeight + "px";
        }
      });
    },
    openUserProfile() {
      window.open("" + "/profile/" + this.reply.userId + "/" + this.reply.userSlug, "_self");
    },
    getReplyReplies(event) {
      var vm = this;
      var button = event.target;
      button.disabled = true;
      if (this.replyReplies.length == 0) {
        axios
          .get("" + "/replies/reply_id=" + this.reply.id)
          .then(response => {
            var replies = response.data.replies;

            replies.forEach(reply => {
              this.flattenReplyReplies(reply);
            });
          })
          .then(response => {
            vm.showReplyReplies = true;
            button.disabled = false;
          })
          .catch(error => {
            button.disabled = false;
          });
      } else {
        this.showReplyReplies = true;
      }
    },

    flattenReplyReplies(reply) {
      this.replyReplies.push(reply);
      /** 
	  if (reply.replies == [] || reply.replies == null) {
        return 0;
      } else {
        reply.replies.forEach(nestedReply => {
          this.flattenReplyReplies(nestedReply);
        });
	  }
	  **/
    },

    addReply() {
      if (this.intent == "") {
        this.intent = "toReplyReply";
      } else {
        this.intent = "";
      }
    },

    replyReply(event) {
      var replyButton = event.target;
      replyButton.disabled = true;
      var vm = this;

      axios
        .post(activityPOSTURL + "/reply-reply", {
          reply_id: vm.reply.id,
          reply: vm.replyReplyText
        })
        .then(response => {
          replyButton.disabled = false;
          vm.intent = "";
          vm.replyReplyText = "";

          showSnackbar("Reply added!");
          window.location.reload();
        })
        .catch(error => {
          replyButton.disabled = false;
        });
    },

    share() {
      var vm = this;
      axios
        .post(activityPOSTURL + "/share/", {
          reply_id: vm.reply.id
        })
        .then(response => {})
        .catch(error => {});
    }
  }
};
</script>
<style scoped>
#innerReply {
  margin-top: 5px;
}

#comment-form {
  display: flex;
  flex-direction: column; 
  -ms-flex-direction: column;
}

#comment-form button {
  align-self: flex-end;
}
.comment {
  box-sizing: border-box;
  word-wrap: break-word;
  padding-bottom: 2px;
  width: 100%;
  border-radius: 0;
  white-space: pre-wrap;
  text-overflow: ellipsis;
  overflow: hidden;
  max-height: 120px;
}
</style>
