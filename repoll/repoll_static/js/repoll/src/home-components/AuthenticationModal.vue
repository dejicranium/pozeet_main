<template id="modal-template">
	<transition name="modal">
		<div class="modal-mask" v-show='show_authentication_modal' v-on:click='closeModal'>
			<div class="modal-container" v-on:click.stop>

				<!--there should be an if condition here
					to decide what to show to the user in the header.
					Basically, we'll need to check the leadingIntent-->
			
			
				<div class="modal-header" style='display:flex; flex-direction:row; color:grey; font-size: 15px;padding:0px;  height:50px;'>					
					<div :id='[intent=="login" ? "selected-tab" : "t"]' @click='intent="login"'>Sign in</div>
					<div :id='[intent=="register" ? "selected-tab" : "t"]' @click='intent="register"'>Register</div>
				</div>

				<div class="modal-body">
					
					<div class='login' v-if="intent=='login'">

						<p class='error' style='color:red; font-size:12px; margin-bottom: 10px;'>{{loginError}}</p>
						<form name='login-form' id='login-form'>
						<label class="form-label">
							Email <br>
							<input class="form-control" v-model='email' name='email'>
						</label><br>

						<label class="form-label">
								Password<br>
							<input class="form-control final-input" type='password' v-model='password' name='password'>
						</label><br>

						<button class='' type='submit' value="Login" @click='completeLogin'>Login</button>
					</form>
					</div>


					<div class='register' v-else>
							<p class='required' v-show='registrationError'>{{registrationErrorText}}</p>
						
							<form id='register-form' name='register-form' enctype="multipart/form-data">
							<div class='first-stage' v-if='registerStage == "first"'>
								<div class='name-div'>
									<div class='first-name-div' >
										<label for="first-name" class='form-label'>First Name <span class='required'>*</span></label><br>
										<input v-model='firstName' id='first-name' class='form-control' name='firsName' type="text" requiredd/>
									</div>
							
									<div class='last-name-div'>
										<label for='last-name' class='form-label'>Last Name <span class='required'>*</span></label><br> 	
										<input v-model='lastName' id='last-name' class='form-control' type="text" name='latName' required/>
									</div>

								</div>

								<label for="username" class="form-label">Username <span class='required'>*</span></label> 
								<input v-model='userName' id='username' class='form-control' type='text' name='uername' required/>

								<label for="password" class="form-label">Password <span class='required'>*</span></label> 
								<span style='font-size:10px; color:teal'> 8 or more characters</span>
								<input v-model='password' id='password' class='form-control' type='password' name='assword' required/>
						

								<label for="email" class='form-label'>Email Address <span class='required'>*</span></label> 
								<input v-model='email' id='email' class='form-control' type='text' name='eail' required/>

								<label for="phone" class="form-label">Phone Number <span class='required'>*</span></label> 
								<input v-model='phone' id='phone' class='form-control final-input' type='text' name='pone' required/>
								
								<button @click='nextRegistrationStage' type='button'>Proceed</button>

						</div>

						<div class='second-stage' v-else-if="registerStage =='second'">
						
							<div style='margin-bottom:10px'>
								<span class='' style='text-align: justify; font-size:12px; color:teal'>Please Note: We'll never, EVER, show any of these information in your profile except at your request</span>
								<span class='' style='font-size:12px; text-align:justify; color:teal'>These details are needed for analysis</span>
							</div>
							<div>
								
								<label for='sex' class='form-label'>Sex <span class='required'>*</span></label>
								<select id='sex' name='sx' v-model='sex' class='form-control'>
									<option value='Female'>Female</option>
									<option value="Male">Male</option>
								</select>
							</div>
							<div style='display:flex; flex-direction: column; width: 100%'>
								<label for="" class="form-label">Date of Birth <span class='required'>*</span></label> 
								<div style='display:flex; flex-direction: row;'>
									<select class='form-control' style='width:40%; margin-right:2px;' name='birhMonth' v-model='birthMonth'>
								  		<option value="" selected disabled hidden>Month</option>
										<option>January</option>
										<option>February</option>
										<option>March</option>
										<option>April</option>
										<option>May</option>
										<option>June</option>
										<option>July</option>
										<option>August</option>
										<option>September</option>
										<option>October</option>
										<option>November</option>
										<option>December</option>
									</select>
									
									<input v-model='birthDate' style="width:20%; margin-right:2px;" id='day' name='birthDate' class='form-control' type='number' placeholder='day'/>
									<select name='birthYear' v-model='birthYear' style='width:40%' class="form-control">
								  		<option value="" selected disabled hidden>Year</option>
										<option v-for='year in years' :year='year' :value='year'> {{year}}</option>
									</select>

								</div>
								<label for="" class="form-label">Location <span class='required'>*</span></label> 
								<div style='display:flex; flex-direction: row;'>
									<select class='form-control' style='width:50%; margin-right:2px;' name='country' v-model='chosenCountry'>
								  		<option value="" selected disabled hidden>Country</option>

										<option v-for='location in locations' :location='location' :value='location.id'> {{location.country}}</option>

									</select>
									
									<select name='subUnit' v-model='subUnit' style='width:50%' class="form-control final-input">
								  		<option value="" selected disabled hidden>Sub-unit</option>
										<option v-for='subUnit in relevantSubUnits' :subUnit='subUnit' :value='subUnit.id' v-model='subUnit.id'> {{subUnit.name}}</option>


									</select>

								</div>
							</div>

							<button @click='nextRegistrationStage' type='button'>Proceed</button>

						</div>
					
						<div class='third-stage' v-if="registerStage =='third'">
							<label class='form-label' style='font-weight:bold;margin-bottom:10px;'>Subscribe to (at least 10): </label>
							<div class='registration-categories-selection' style='margin-top:10px;'>
								<label v-for='category in categories' :category='category' @click='toggleChooseCategory(category.categoryId)'>
									<input type='checkbox' value='category.categoryId' @click.stop/> {{category.categoryName}}
									<span class='checkmark' @click.stop></span>
								</label>

							</div>
							<div class="proceed-container">
								<button type='button' @click='nextRegistrationStage'>Proceed</button>
							</div>
						</div>


					<div class='final-stage' v-if="registerStage =='fourth'" style='display:flex; flex-direction: column; text-align:center'>
						<span style='color: teal; font-size: 14px; margin-bottom:5px;'>Choose Profile Picture</span>
						
						<div style='text-align:center;'>
						<img id="profilePicDisplay" width='200' height='200' style='border-radius: 50%'/>
          				<input type="file"
               				id="profilePicInput" @click='changeProfilePic' name="profilePic"
               				accept="image/png, image/jpeg" />

						</div>
						<button class="proceed-btn" type='button' @click='completeRegistration' > <i class="fa fa-circle-o-notch fa-spin" v-if=''></i>Register</button>

					</div>
					</form>
				</div>

				
		</div>
			</div>



			
		</div>
	</transition>
</template>
	

<script>
	const siteUrl = "http://ec2-18-218-17-23.us-east-2.compute.amazonaws.com:6543";


	import axios from 'axios';
	export default { 
		name: 'Authentication Modal', 
		props: ['show_authentication_modal', 'categories', "activity_to_refer"],
		delimiters: ['((', '))'],
		data(){
			return{
				leadingIntent: '', //know what action user wanted to take before wanting to authenticate
				intent: 'login', //to know whether user wants to login or register
				loginProgressing: false, 
				loginError: '',
				registerStage: 'first',
				email: '',
				password: '',
				firstName: '',
				lastName: '',
				userName:'',
				password: '',
				phone: '',
				birthMonth: '',
				sex: '',
				birthDate: '',
				birthYear: '',
				registrationError: false, 
				registrationErrorText: '',
				registrationCategories: '',
				chosenCategories: [],
				years: [],
				locations: [], 
				chosenCountry: 0,
				subUnit: 0,

				
			}


		},
		

		computed:{
			relevantSubUnits(){
				if (this.chosenCountry != 0){
					var country = this.locations.filter(c=>c.id==this.chosenCountry);
					var subUnits = country[0]['subUnits'];
					return subUnits;
				}
				else{
					return [];
				}
			},

		},
		methods:{

			toggleChooseCategory(id){
				//check if the category is already there
				var category = this.chosenCategories.filter(element=>element == id)[0];
				if (category){
					//get the index, so we can remove it from the item.
					var categoryIndex = this.chosenCategories.indexOf(id);
					this.chosenCategories.splice(categoryIndex);
				}
				else{
					this.chosenCategories.push(id);
				}
			},

			flattenCategories(){
				var categories = new Set(this.chosenCategories);
				var newCategories = Array.from(categories);

				this.registrationCategories = newCategories.join(",");

			},

			verifyFirstRegistrationStage(){
				var allFieldsFilled = this.email != '' && this.password != '' && this.firstName != '' && this.lastName != '' && this.userName != '' && this.password != '' && this.phone != '';
				return allFieldsFilled;
			},

			emailIsEligible(){
				  var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  					return re.test(this.email);
				
			},


			passwordIsEligible(){
				return this.password.length > 7;
			},

			userNameIsEligible(){
				return this.userName.length > 2;
			},

			nextRegistrationStage(event){
				event.preventDefault();
				var stage = this.registerStage;
				var canMoveToNextStage = true;
				var vm = this;

				if (stage == 'first' ){
					var allFieldsFilled = this.verifyFirstRegistrationStage();
					var passwordIsAcceptable = this.passwordIsEligible();
					var userNameIsAcceptable = this.userNameIsEligible();

					if (!allFieldsFilled){
						canMoveToNextStage = false;
						this.registrationError = true;
						this.registrationErrorText ='Please complete all fields';

					}

					else if(!this.emailIsEligible){
						canMoveToNextStage = false;
						this.registrationError = true;
						this.registrationErrorText = 'Email address is not a valid';
					}


					else if (!userNameIsAcceptable){
						canMoveToNextStage = false;
						this.registrationError = true;
						this.registrationErrorText = "Username must be more than 2 characters"
					}

					else if (!passwordIsAcceptable){
						canMoveToNextStage = false;
						this.registrationError = true;
						this.registrationErrorText = "Password must be at least 8 characters";
					}

					if (canMoveToNextStage){
						//no error
						this.registrationError = false;
						this.registrationErrorText ='';

						axios.post("" + '/verify_first_register', {
							stage: '1', //sends this to server
							email: vm.email,
							phone: vm.phone,
							username: vm.userName,

						}).then(response=>{
							//go to the next stage;
							vm.registerStage = 'second';
						}).catch(error=>{
							vm.registrationError = true;
							vm.registrationErrorText = error.response.data['error'];
						});
					}

					
					
				}
				else if (stage == 'second'){
					canMoveToNextStage = true; 

					if (this.sex == '' || this.birthDate == '' || this.birthMonth == '' || this.birthYear == ""){
						canMoveToNextStage = false;
						this.registrationError = true;
						this.registrationErrorText = "Please fill all fields";
					}

					else if(this.birthDate.length > 2){
						canMoveToNextStage = false;
						this.registrationError = true; 
						this.registrationErrorText = "Your birthday looks incorrect";
					}

					//else if(this.birthYear.length < 4 || this.birthYear > 4){
					//	canMoveToNextStage = false;
					//	this.registrationError = true;
					//	this.registrationErrorText = "Your birth year looks incorrect"
					//}

					if (canMoveToNextStage){
						this.registerStage = 'third';
						this.registrationError = false;
						this.registrationErrorText = "";
					}
				}

				else if (stage == 'third'){
					canMoveToNextStage = true; 

					if (this.chosenCategories.length < 10){
						canMoveToNextStage = false;
						this.registrationError = true; 
						this.registrationErrorText = 'Please choose at least 10 categories';
					}

					if (canMoveToNextStage){
						this.registerStage = "fourth";
						this.registrationError = false;
						this.registrationErrorText = "";
					}
				}
			},
			closeModal(){
				this.$emit('close_auth_modal', false);
			},

			changeIntent(){
				intent = this.intent;
				if (intent=='login'){

					//make sure we empty the email and password if user already inserted them
					this.email = '';
					this.password = '';
					this.intent = 'register';
				}
				else{
					this.intent = 'login';
				}
			},
			
			changeProfilePic(){
				var profilePicInput = document.getElementById('profilePicInput');
				var profilePicDisplay = document.getElementById('profilePicDisplay');

				profilePicInput.addEventListener('input', function(){
					var images = profilePicInput.files;
					profilePicDisplay.src = window.URL.createObjectURL(images[0]);
				});
			},

			completeLogin: function(event){
				var vm = this;
				event.preventDefault();
				var target = event.target;
				target.disabled = true;

				target.innerHTML = '...';
				
				if (this.email == '' || this.password  == ''){
					this.loginError='Please fill complete details';
					return 0;
				}

				var form = document.getElementById('login-form');
				var formData = new FormData(form);
				
				var request = new XMLHttpRequest();
				request.open("POST", "" + '/xhr_login');
				request.open("POST", siteUrl + 'xhr_login');
				request.onreadystatechange = function(){
					if (request.readyState == XMLHttpRequest.DONE){
						if(request.status == 200){
								vm.$emit('close_auth_modal', false);
								target.innerHTML = 'Sign in';
								target.disabled = false;
								if (this.activity_to_refer){
									//@need_to_change: if the url for accessing pols change
									window.location.assign("" + "/" + vm.activity_to_refer.type + "/" + vm.activity_to_refer.id + "/");
								}
								else{
									window.location.reload();
								}
						}	
						else {
							vm.loginError = 'Email or password is incorrect';
							target.innerHTML = 'Sign in';
							target.disabled = false;

						
						}
					
					}
				}
				
				request.send(formData);
				
				//axios.post('http://localhost:6543/login', {
				//	xhr_login_email: this.email, 
				//	xhr_login_password: this.password,
				//}).then(function(response){
				//	vm.$emit('close_auth_modal', false);
				//	window.location.reload();
				//}).catch(function(error){
				//	alert(error);
				//});
			},
			completeRegistration: function(event){
				var vm = this;
				this.flattenCategories();
				event.preventDefault();

				vm.changeButtonContent(event.target, '...');
				event.target.disabled = true;
				var form = document.getElementById('register-form');
				var formData = new FormData(form);

				formData.append('firstName', this.firstName);
				formData.append('lastName', this.lastName);
				formData.append('email', this.email);
				formData.append('password', this.password);
				formData.append('phone', this.phone);
				formData.append('username', this.userName);
				formData.append('sex', this.sex);
				formData.append('birthDate', this.birthDate);
				formData.append('birthMonth', this.birthMonth);
				formData.append('birthYear', this.birthYear);
				formData.append('country', this.chosenCountry);
				formData.append('subUnit', this.subUnit);
				formData.append('categories', vm.registrationCategories);
				

				var request = new XMLHttpRequest();
				request.open("POST", "" + '/xhr_register');
				request.onreadystatechange = function(){
					if (request.readyState == XMLHttpRequest.DONE){
						if(request.status == 200){
								vm.$emit('close_auth_modal', false);
								window.location.reload();
								vm.changeButtonContent(event.target, 'Register');
								event.target.disabled = false;
						}
						else {
							vm.changeButtonContent(event.target, 'Register');
							alert("somethign went wrong");
							event.target.disabled = false;
						}
					}
				}
				request.send(formData);
						
			},
			 

		},
		
		mounted(){
			for (let i=2005; i > 1930; i--){
				this.years.push(i);
			}

			axios.get("" + '/get-locations').then(response=>{
				this.locations = response.data.locations;
			});
		},

	}


</script>


<style scoped>
	.modal-container .modal-body{
		position: relative;
		padding-bottom: 20px;
	}

	.modal-container .modal-body .final-input{
		margin-bottom: 30px;
	}
	.modal-container .modal-body button{
		position: absolute;
		right: 0; 
		bottom: 0;
		margin-right: 20px; 
	}
	.third-stage {
		display: flex;
		flex-direction: column;
	}

	.final-stage {
		align-items: center;
		justify-content: center;
	}

	.final-stage button{
		position: relative; 
		margin-right: 0;
	}
	.proceed-container {
		display: flex;
		flex-direction: column;
		justify-self: flex-end;
	}
	.proceed-container button {
		align-self: flex-end;
		position: relative;
	}



</style>