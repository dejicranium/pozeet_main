
<template>
    <div id="sub-container">
            <div class='chart-container' v-for='metrics in metricsData' >
                <p class='chartTitle' v-cloak>{{metrics.title}}</p>
            </div>

            <canvas id='metricsChart' width='200' height='200'></canvas>  


            <div id='choice-of-metrics-div'>
                <p id="metricsError"></p>
                <div id='main-focus-choice-div'>
                    <p class='criterion-text'>Criterion:</p> 
                    <select v-model='newMainFocus'> 
                        <option>Gender</option>
                        <option>Age</option>
                        <option>Age Range</option>
                    </select>

                    <input type='number' class='mainFocusAgeSelection' v-show='showMainFocusAgeSelectionBoxes' placeholder='Age' v-model='m_f_objs'/>
                    
                    <div v-show='showMainFocusAgeRangeSelectionBoxes' class='mainFocusAgeRangeSelection'>
                        <input type='number' v-model='ageUpperBound'/> -
                        <input type='number' v-model='ageLowerBound'/>
                    </div>
                </div>

                <div id='sub-focus-choice-div'>
                    <p v-show='subFocusSelectionTextOne' 
                        class='sub-focus-selection-text' v-cloak> {{subFocusSelectionTextOne}}
                    </p>
                   
                    <select v-show='subFocusSelectionTextOne' v-model='newSubFocus'>
                        <option v-for='criterion in allowedSubFocusCriterion' v-if='criterion.option'> <span style='font-weight:bold;' v-cloak>{{criterion.option}}</span></option>
                        <option v-for="criterion in allowedSubFocusCriterion" v-if='!criterion.option' v-cloak> {{criterion}} </option>
                    </select>

                    <p v-show='subFocusSelectionTextTwo' 
                        class='sub-focus-selection-text'>{{subFocusSelectionTextTwo}}
                    </p>

                    <input type='number' class='subFocusAgeSelection' v-show='showSubFocusAgeSelectionBoxes' placeholder='Age'/>
                    
                    <div v-show='showSubFocusAgeRangeSelectionBoxes' class='subFocusAgeRangeSelection'>
                        <input type='number'/> 
                        <br>to<br>
                        <input type='number'/>
                    </div>               
                </div>
            </div> 
            <div class="go-div">
                <button @click='getMetrics' type='button' class='goBtn'>Go</button>
            </div>




    </div>



</template>


<script>
    import axios from 'axios';
    import Chart from 'chart.js';

    var opinion = document.getElementById('hidden-question-signifier').innerHTML;
    var opinionId = document.getElementById('hidden-id-signifier').innerHTML;
var siteUrl = "";

export default {
    name: 'ShowOpinionMetrics',
        //we need to be able to destroy this chart, so we make it global
        data(){
                //metrics data will be a list of object
                //each object will contain the main_focus, and sub_focus, 
                //the canvas in #app shall populate based on this list
            return{
                loading: true,
                opinion: {},
                 metricsData: [{title: 'Voters on opinion'},],
                    s_f: '',
                    chart1: '',
                    m_f: '',
                    newMainFocus: '',
                    newSubFocus: '',
                    s_f_objs: '',
                    m_f_objs: 'som',
                    showMainFocusAgeSelectionBoxes: false,
                    showMainFocusAgeRangeSelectionBoxes: false,
                    subFocusSelectionTextOne: '',
                    subFocusSelectionTextTwo: '',
                    showSubFocusAgeSelectionBoxes: false,
                    showSubFocusAgeRangeSelectionBoxes: false,
                    allowedSubFocusCriterion: [],
                    ageUpperBound: 0,
                    ageLowerBound: 0,


                }
            },

            methods:{
                changeOpinionData(id, value){
                    this.$set(this.opinion, id, value);
                },

                createNewChartCanvas(){
                    var length = this.chartIds.length;
                    var newChartId = 'metricsChart' +length+1; 
                    this.chartIds.push(newChartId);
                    //return the name of the new Chart Canvas
                    return newChartId;
                },
                
                getOpinionDetails(){
                    var vm = this;
                    axios.get('/opinion/' + opinionId).then(response=>{
                        vm.changeOpinionData('options', response.data.options);
                        vm.changeOpinionData('opinion', response.data.opinion);

                    });
                },
 
                makePieChart(aLabels, aData){
                    if (this.chart1){
                        this.chart1.destroy();
                    }
                    var ctx = document.getElementById('metricsChart').getContext('2d');


                    var options = {
                        legend:{
                            display: true, 
                            position: "bottom",
                            labels:{
                                fontColor: '#333',
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
                                    "green",
                                    "orange",
                                    "#C62828",
                                    "#8D6E63",
                                    "#8BC34A",
                                    "#26A69A",
                                    "#BF360C",
                                    "#1565C0",
                                    "#00796B",


                            
                                ],
                                borderColor: [
                                    'green', 
                                    'orange',
                                    "#C62828",
                                    "#8D6E63",
                                    "#8BC34A",
                                    "#26A69A",
                                    "#BF360C",
                                    "#1565C0",
                                    "#00796B",

                                ]
                            }
                        ]
                    };

                        
                        
                        chart1 = new Chart(ctx, {
                        type: "pie",
                        data: data,
                        options: options,
                    });

                },
 
                getMetrics(){
                    var vm =this;
                    var responseAction = "";

                    //get the response type
                    if (this.newSubFocus == "Agree"){
                        responseAction = "agreed";
                    }

                    else {
                        responseAction = "disagreed";
                    }

                    //global errorText
                    var errorText =  document.getElementById('metricsError');

                    if (this.m_f == 'age_range'){
                        this.m_f_objs = this.ageUpperBound + '-' + this.ageLowerBound;
                        //if the lower bound is higher than the upperbound, raise an erro
                        if (this.ageUpperBound > this.ageLowerBound) {
                            errorText.innerHTML = "Age lower bound cannot be higher than age higher bound";
                            return 0;
                        }
                    }

                    //if the main focus is age and the value of age is less than -1, raise an error
                    if (this.m_f == 'age' && this.m_f_objs < 0){
                        errorText.innerHTML = "Age cannot be negative";
                        return 0;
                    }

                    axios.get("" + '/get-metrics/' + opinionId,{
                        params:{
                            m_f: this.m_f, 
                            s_f: this.s_f, 
                            m_f_objs: this.m_f_objs,
                            s_f_objs: this.s_f_objs,
                        }
                    }).then(response=>{
                        //if it is a success, first of all do not show any error;
                        errorText.innerHTML = "";
                        if (vm.m_f =='gender' && vm.s_f=='option'){
                            var labels = ["Male", "Female"];
                            var data = [response.data['M'].votes, response.data['F'].votes];
                            vm.metricsData[0].title = 'Sex of users who ' + responseAction + " to the opinion above";
                            vm.makePieChart(labels, data);
                            vm.m_f=='gender';
                            
                        }

                        else if(vm.m_f=='age' && vm.s_f=='option'){
                            vm.m_f = 'age';
                            var age = vm.m_f_objs
                            vm.metricsData[0].title = "Users, " + age + " years of age, who " + responseAction + " to the opinion above";                            var labels = ["Voters " + age + " years of age"]
                            var data = [response.data[age].votes] 
                            
                            vm.makePieChart(labels, data);
                            vm.m_f = 'age';
                        }

                        else if(vm.m_f=='age' && vm.s_f == 'options'){
                            vm.m_f='age';
                            var age = vm.m_f_objs
                            var options = vm.opinion.options.map(option=>option.option);
                            var option_ids = vm.opinion.options.map(option=>option.id);
                            vm.metricsData[0].title = "Votes of users, " + age + " years of age, in opinion ";

                            var labels = options
                            var data = []
                            option_ids.forEach(function(id){
                                var age = vm.m_f_objs;
                                var new_data = response.data[age][id].votes;
                                data.push(new_data);
                            });

                            vm.makePieChart(labels, data);

                            vm.m_f = 'age';                            
                        }

                        else if(vm.m_f=='age_range' && vm.s_f == 'option'){
                            vm.m_f='age_range';
                            var ages = [];
                            var i = vm.ageUpperBound;
                            var upperBound = parseInt(vm.ageLowerBound) + 1;
                            while(i < upperBound){
                                ages.push(i);
                                i++;
                            }
                 
                            var labels = ['Voters between ' + vm.ageUpperBound + ' and ' + vm.ageLowerBound + ' of age'];
                            var pre_data = []; //contains string numbers;
                            var data = [];
                            var age_vote = 0;
                            
                            ages.forEach(function(age){
                                age_vote += parseInt(response.data[age].votes);
                            });


                            data.push(age_vote);

                            vm.makePieChart(labels, data);

                            vm.m_f = 'age_range';                            
                        }

                        else if(vm.m_f=='age_range' && vm.s_f == 'options'){
                            vm.m_f='age_range';
                            var ages = [];
                            var i = parseInt(vm.ageUpperBound);
                            var upperBound = parseInt(vm.ageLowerBound) + 1;
                            while(i < upperBound){
                                ages.push(i);
                                i++;
                            }  
                            var options = vm.opinion.options.map(option=>option.option);
                            var optionsId = vm.opinion.options.map(option=>option.id);
                            var data = [];
                            
                            //iterate through the options
                            optionsId.forEach(id=>{
                                var idVotes = 0; 
                                ages.forEach(age => {
                                    idVotes += response.data[age][id].votes;
                                });
                                data.push(idVotes);
                            });
                            var labels = options;
                            vm.metricsData[0].title = "Votes of users, between ages " + vm.ageUpperBound + "-" + vm.ageLowerBound;

                            vm.makePieChart(labels, data);

                            vm.m_f = 'age_range';                            
                        }
                    });
                },
            },

            watch:{

                newMainFocus: function(val){
                    if (val == 'Age'){
                        this.showMainFocusAgeSelectionBoxes = true;
                        this.showSubFocusAgeRangeSelectionBoxes = false;
                        this.showSubFocusAgeSelectionBoxes = false;
                        //this.allowedSubFocusCriterion = this.opinion.options.map(i=>i.option);
                        this.allowedSubFocusCriterion.unshift('All Options');
                        this.m_f = '';
                        this.m_f = 'age';

                    }
                    else{
                        this.showMainFocusAgeSelectionBoxes = false;
                        
                    }
                    if (val == "Age Range"){
                        this.showMainFocusAgeRangeSelectionBoxes = true;
                        this.showSubFocusAgeRangeSelectionBoxes = false;
                        this.showSubFocusAgeSelectionBoxes = false;
                        //this.allowedSubFocusCriterion = this.opinion.options.map(i=>i.option);
                        this.allowedSubFocusCriterion.unshift('All Options');
                        this.m_f ='age_range';
                    }

                    else{
                        this.showMainFocusAgeRangeSelectionBoxes = false;
                  
                    }
                    if (val == 'Gender'){
                        this.showSubFocusAgeRangeSelectionBoxes = false;
                        this.showSubFocusAgeSelectionBoxes = false;
                        
                        //give each option a new value so we can render
                        this.allowedSubFocusCriterion = this.opinion.options.map(i=>i.option);
                        //this.allowedSubFocusCriterion.unshift('All Options');

                        this.m_f = 'gender';
                        
                    }


                    if (val != ''){
                        this.subFocusSelectionTextOne = 'Insights into ';
                    }

                    else{
                        this.subFocusSelectionTextOne = '';
                    }


                    var isOption = this.opinion.options.filter(option=>option.option == val).length !=0;

                    if (isOption){
                        this.subFocusSelectionTextTwo= 'of voters: ';
                        this.allowedSubFocusCriterion = ['Gender', 'Age', 'Age Range'];
                        this.m_f = this.opinion.options.filter(option=>option.option == val)[0].id;

                    }
                    else{
                        this.subFocusSelectionTextTwo = '';
                    
                    }
                },


                newSubFocus: function(val){
                    if (val == 'Age'){
                        this.newSubFocus = 'age';
                        this.showSubFocusAgeSelectionBoxes = true;
                        this.showSubFocusAgeRangeSelectionBoxes = false;
                        this.s_f = "age";
                    }
                    else if (val == 'Age Range'){
                        this.showSubFocusAgeRangeSelectionBoxes = true;
                        this.showSubFocusAgeSelectionBoxes = false;
                        this.s_f = 'age range';
                    }
                    else if (val == 'All Options'){
                        this.showSubFocsusAgeRangeSelectionBoxes = false;
                        this.showSubFocusAgeSelectionBoxes = false;
                        this.s_f = 'options';
                        this.s_f_objs = 'options';

                    }
                    else{
                        this.showSubFocsusAgeRangeSelectionBoxes = false;
                        this.showSubFocusAgeSelectionBoxes = false; 
                        var chosenOption =  val;
                        var optionMatch = this.opinion.options.filter(option=>option.option == chosenOption);
                        this.s_f = 'option';
                        this.s_f_objs = optionMatch[0].id;
                    }
                }

            },

            mounted(){
                
                //first ge poll details
                this.getOpinionDetails();
                var vm  = this;
                             
                axios.get('/get-metrics/' + opinionId, {
                    params: {
                        m_f: 'gender',
                        s_f: 'poll',
                        m_f_objs: 'M',
                        s_f_objs: opinionId,
                    }


                }).then(response=>{
                     vm.makePieChart(["Male", "Female"], [response.data['M']['votes'], response.data['M']['votes']]);


                });

                vm.loading = false;
            },
}


</script>

<style scoped>

.chart-title {
    word-wrap: break-word;
    overflow: hidden;
    text-overflow: ellipsis;
}
.go-div {
    display: flex;

    width: 100%;

    justify-content: flex-end;
}

.go-div button {
    justify-self: flex-end;

    font-size: 12px;

    padding: 8px 20px;

    background-color: teal;

    color: white;

    border-radius: 0%;
}

#metricsError {
    color: red; 
    font-size: 12px;
    line-height: 1.5;
}
</style>
