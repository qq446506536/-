<template>

	<div class="btn-danger">
		<button class="btn-lg-danger"
		@click="callback"
		>点击测试</button>


    <input type="text" name="courseid" 
      v-model='courseid'
    >
    <input type="text" name="priceid"
      v-model = 'priceid'
    >


	</div>
</template>

<script>
import axios from 'axios'
export default {

  name: 'Luffy',

  data () {
    return {
        courseid:'',
        priceid:''
    }
  },
  methods:{
  	callback:function(){
  		console.log(66);
  		axios({
        method:'post',
        url:'http://127.0.0.1:8000/api/v1/shopcar/',
        data:{

          courseid:this.courseid,
          priceid:this.priceid
        }
        ,
        headers:{
                  'Content-Type':'application/json'
                },
        responseType: 'json'

      })
  		.then(function(res){
  			alert(res);
  			console.log(res);
  		})

  	}

  }
}
</script>

<style lang="css" scoped>
</style>