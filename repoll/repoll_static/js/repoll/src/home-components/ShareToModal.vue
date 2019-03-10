<template>
    <transition>
        <div class="modal-mask" v-if="show_shareto_modal" @click="closeModal">
            <div class="modal-container" @click.stop> 
                <div class="content">
                    <div class="twitter social" @click="shareToTwitter">
                        <img @click="share('twitter')" src="https://s3.us-east-2.amazonaws.com/pozeet-static/twitter_logo.png" class="twitter_logo social_logo"/>
                        <p @click="shareToTwitter" class="content_icon">Twitter</p>
                    </div>
                    <div class="whatsapp social" @click="shareToTwitter">
                        <img @click="share('whatsapp')" src="https://s3.us-east-2.amazonaws.com/pozeet-static/whatsapp_logo.png" class="whatsapp_logo social_logo"/>
                        <p @click="shareToTwitter" class="content_icon">Whatsapp</p>
                    </div>
                </div>

                <div class="share__input">
                    <input :value="activityLink" class="share__input__link" id="copyText" readonly/>
                    <button class="share__input__button">COPY</button>
                </div>
            </div>       
        </div>    
    </transition>    
</template>

<script>
var siteUrl = "";
export default {
    name: 'ShareToModal', 
    props: ['show_shareto_modal', 'activity', ],
    data(){
        return{
        }
    },
    methods:{
        copyLink(){
           var copyText  = document.getElementById('copyText');
            copyText.select();

            document.execCommand("copy");
        },

        closeModal(){
            this.$emit('act_close_shareto_modal', false);
        },

        share(site){
            if (site == "twitter"){
                if (this.activity.type == "poll"){
                    var pollQuestion = this.activity.question;
                    var goToUrl = siteUrl + "http://ec2-18-218-17-23.us-east-2.compute.amazonaws.com:6543/poll/" + this.activity.id + "/";
                    var shareText = "Pozeet: " + pollQuestion + ". Contribute and see what people are saying.";
                
                    window.open("https://twitter.com/intent/tweet?text=" + shareText + "&url=" + goToUrl, "_");
                }
                else if (this.activity.type == "opinion") {
                    var opinion  = this.activity.opinion;
                    var goToUrl = siteUrl + "http://ec2-18-218-17-23.us-east-2.compute.amazonaws.com:6543/opinion/" + this.activity.id + "/";
                    var shareText = opinion + ".Pozeet: See what people are saying about this opinion";
                    window.open("https://twitter.com/intent/tweet?text=" + shareText + "&url=" + goToUrl, "_");

                }
            }

            else if (site == "whatsapp"){
                if (this.activity.type == "poll"){
                    var pollQuestion = this.activity.question;
                    var goToUrl = siteUrl + "/poll/" + this.activity.id + "/";
                    var shareText = "Pozeet: " + pollQuestion + ". Contribute and see what people are saying.";
                
                    window.open("whatsapp://send?text=" + shareText + " " + goToUrl, "_");
                }

                else if (this.activity.type == "opinion"){
                    var opinion = this.activity.opinion;
                    var goToUrl = siteUrl + "/opinion/" + this.activity.id + "/";
                    var shareText = opinion + ". Pozeet: See what people are saying about this opinion";
                    window.open("whatsapp://send?text=" + shareText + " " + goToUrl, "_");
                }
            }            
        }
    },

    computed: {
        activityLink(){
            if (this.activity.type == "poll"){
                return siteUrl + '/poll/' + this.activity.id + '/';
            }
            else if (this.activity.type == "opinion"){
                return siteUrl + "/opinion/" + this.activity.id +'/';
            }
        }
    }

}


</script>

<style scoped>
    .modal-container{
        margin-top: 45%;
        padding: 10px;
    }
    .info{
        height: 20px; 
        border-bottom: solid lightgrey 1px;
        color:darkgrey;
        padding: 5px;
        font-size: 14px;
        
    }
    .content {
        display: flex;
        justify-content: center; 
        margin-bottom: 10px;
    }
    .social {
        display: flex; 
        flex-direction: column;
        justify-content: center;
        align-items: center;
        margin-right: 10px;
    }
    .social_logo {
        height: 45px; 
        width: 45px;
        margin-bottom: 5px;
    }

    .content_icon {
        font-size: 12px;
    }

    .share__input {
        background-color: whitesmoke;
        padding: 5px;
        display:flex; 
        flex-direction: row;
        -ms-flex-direction: row;
        justify-content: center; 
        align-items: center;
    }

    .share__input__link {

    }

    .share__input__button {
        padding:2px;
        background-color: teal; 
        color: white;
    }


</style>
