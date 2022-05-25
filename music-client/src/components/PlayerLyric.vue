<template>
    <div class="lyric">
        <div class="lyric_inner" ref="lyric_inner">
            <p 
                v-for="(lyric, index) in lyricArr" 
                :key="index"
                :class="{on: index == lineNo}"
            >
            {{lyric.content}}</p>
        </div>
    </div>
</template>

<script setup>
    import { computed, ref, watch, nextTick } from 'vue'
    import { useStore } from 'vuex'

    const store = useStore()
    const lyric_inner = ref(null)
    
    const lyricArr = computed(() => store.state.song.lyricArr)      //歌词数组
    const lineNo = computed(() => store.state.song.lineNo)          //歌曲当前播放行

    watch(lineNo, value => {
        //初始化歌词偏移为0
        if(value <= 3) {
            nextTick(function() {
                lyric_inner.value.style = "transform: translateY(0)"
            })
        }
        
        //播放行数大于3时歌词开始滚动
        if(value > 3) {
            nextTick(function() {
                lyric_inner.value.style = "transform: translateY(" + (-58 * (value - 3)) + "px)"
            })
        }
    }, { immediate: true })
</script>

<style lang="less" scoped>
    /* 歌词 */
    .lyric {
        position: absolute; 
        bottom: 25%;        
        left: 50%;
        transform: translateX(-50%);    
        width: 1157px;      
        height: 350px;
        margin: 0 auto;     
        z-index: 2;         
        overflow: hidden;
        .lyric_inner {
            line-height: 58px;  
            text-align: center; 
            font-size: 22px;    
            color: #fff;      
            user-select: none;  
            transition: transform 0.2s ease-out 0s; 
            .on {
                color: #008fd9;
            }
        }   
    }
</style>