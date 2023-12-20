<template>
  <div id="post">
    <h1>帖子</h1>
  </div>
</template>

<script>
export default {
    name:"Post" ,
    mounted(){
        this.$http.getPostList(1).then(res =>{
            console.log(res);
        })
    }
}
</script>

<style scoped>

</style>