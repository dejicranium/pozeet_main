<template>
    <div class="card-container">
        <div>
            <img src="/static/rename.svg" v-show="listLoading"/>
        </div>
        <div class="image">
            <img src="https://pbs.twimg.com/profile_images/1081905771028320256/yajLUZzZ_400x400.jpg"/>
        </div>
        <div class="detail">
            <div class="name">{{user.userName}}</div>
            <div class="username">{{user.username}}</div>
        </div>
        <div class="follow">
            <button class="button follow-btn" @click="followUser" v-if='!userIsFollowing'>Follow</button>
            <button class="button unfollow-btn" @click="unfollowUser" v-if='userIsFollowing'>Unfollow</button>

        </div>  
    </div>
</template>

<script>
    import axios from 'axios';
var siteUrl = "http://ec2-18-218-17-23.us-east-2.compute.amazonaws.com:6543";
	const activityPOSTURL = "http://ec2-18-218-17-23.us-east-2.compute.amazonaws.com:6543";

    export default {
        name: 'UserCard',
        props: ['user'],
        data(){
            return {
            }
        },
        computed: {
            userIsFollowing: {
                get: function(){
                    return this.user.userIsFollowing;
                },
                set: function(newValue){
                    this.user.userIsFollowing = newValue;
                }
            }
        },
        methods: {
            followUser(event){
                var vm = this;
                event.target.disabled = true;
                axios.post(activityPOSTURL + "/follow/" + this.user.userId, {
                }).then(response =>{
                    vm.userIsFollowing = true;
                    event.target.disabled = false;
                }).catch(error=>{
                    event.target.disabled = false;
                });

            },
            unfollowUser(event){
                var vm = this;
                event.target.disabled = true;
                axios.post(activityPOSTURL + "/unfollow/" + this.user.userId, {
                }).then(response=>{
                    vm.userIsFollowing = false;
                    event.target.disabled = false;
                }).catch(error=>{
                    event.target.disabled = false;
                });
            },
        }
    }
</script>

<style scoped>
        .card-container {
            display: flex;
            flex-direction: row;
            box-sizing: border-box;
            -ms-flex-direction: row;
            align-items: stretch;
            padding: 5px 5px;
            justify-content: center;
        }
        .image {
            align-items: center;
            justify-content: center;
            padding: 5px 5px;
        }
        .image img {
            max-width: 44px;
            max-height: 44px;
            border-radius: 50%;
        }

        .detail {
            display: flex; 
            flex-direction: column;
            justify-content: center;
            padding: 5px 5px;
            font-size: 14px;
            width: 100px;
        }
        .detail :first-child {
            font-weight: bold;
        }
        .detail div {
            overflow-x: hidden;
            overflow-y: hidden;
            text-overflow: ellipsis;
            -ms-text-overflow: ellipsis;
            -o-text-overflow: ellipsis;
        }
        .detail .name {
            text-overflow: ellipsis;
            -ms-text-overflow: ellipsis;
            -o-text-overflow: ellipsis;
            overflow: hidden;
        }
        .detail .username {
            color: darkgrey;
        }
        .follow {
            padding: 5px 5px;
            display: flex;
            align-items: center;
        }
        .follow button {
            border: 0; 
            border-radius: 3px; 
            padding: 8px 8px;
            background-color: teal;
            color: white;
        }

        .follow .unfollow-btn {
            border: 0.5px solid grey;
            border-radius: 3px; 
            padding: 8px 8px;
            background-color: white;
            color: black;
        }
</style>

