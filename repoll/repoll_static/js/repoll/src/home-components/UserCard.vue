<template>
    <div class="card-container">
        <div class="image">
            <img :src="user.userPic"/>
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
var siteUrl = "";
	const activityPOSTURL = "";

    export default {
        name: 'UserCard',
        props: ['user'],
        data(){
            return {
                listLoading: false,
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
            width: 44px;
            height: 44px;
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
            white-space: nowrap;
        }
        .detail .username {
            color: darkgrey;
            text-overflow: ellipsis;
            -ms-text-overflow: ellipsis;
            -o-text-overflow: ellipsis;
            overflow: hidden;
            white-space: nowrap;
        }
        .follow {
            padding: 5px 5px;
            display: flex;
            align-items: center;
        }
        .follow button {
            border: 0; 
            border-radius: 3px; 
            background-color: teal;
            color: white;
            height: 30px;
            width: 59px;
        }

        .follow .unfollow-btn {
            border: 0.5px solid grey;
            border-radius: 3px; 
            height: 30px;
            width: 59px;            
            background-color: white;
            color: black;
        }
</style>

