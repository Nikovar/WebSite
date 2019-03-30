<template>
    <div id="hello">
        <h2>{{message}}</h2>
    </div>
</template>
 
<script>
export default {
    name: 'temp',
    data () {
        return {
            message: 'Как тебе такое, Илон Маск?'
        }
    }
}
</script>
 
<style>
    #hello {
        font-family: Verdana;
        color: navy;
    }
</style>
