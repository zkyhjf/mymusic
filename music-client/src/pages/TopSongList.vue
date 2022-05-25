<template>
    <!-- 歌曲列表 -->
    <div class="songlist fl" v-if="topList.length > 0">
        <div class="head">
            <ul>
                <li>序号</li>
                <li>歌曲</li>
                <li>歌手</li>
            </ul>
        </div>

        <ul>
            <li v-for="(song, index) in topList" :key="song.id">
                <a class="song_item" :href="`/player?songid=${song.id}`" target="player">
                    <div class="song_rank">{{index+1}}</div>
                    <div class="song_name">
                        <img :src="song.pic" loading="lazy">
                        {{song.title}}
                    </div>
                    <div class="song_author">{{song.author}}</div>
                </a>
            </li>
        </ul>
    </div>
</template>

<script setup>
    //排行榜歌曲列表
    import { httpManager } from '@/api'
    import { ref, watch, reactive } from 'vue'

    const props = defineProps({ category: String })

    //排行榜查询参数
    const queryInfo = reactive({
        category: props.category,
        size: 100
    })
    
    //获取排行榜歌曲数据
    const topList = ref([])
    watch(() => props.category, async category => {
        queryInfo.category = category
        const { data: res } = await httpManager.getTopList(queryInfo)
        topList.value = res.data
    }, { immediate: true })
</script>

<style lang="less" scoped>
    /* 歌曲列表 */
    .songlist {
        width: 763px;                  
        background-color: #fbfbfb;      
        border: 1px solid #d3d3d3;      
        box-sizing: border-box; 
        .head {
            height: 46px;          
            background: #fafafa;    
            font-size: 15px;       
            color: #999; 
            li {
                float: left;       
                line-height: 46px; 
                &:first-child {
                    width: 100px;       
                    text-align: center;
                }
                &:nth-child(2) {
                    width: 300px;       
                    text-align: center; 
                }
                &:nth-child(3) {
                    width: 250px;           
                    padding-left: 100px;   
                }
            }          
        }
        .song_item {
            display: block;             
            height: 54px;              
            padding: 10px 0;           
            color: #333;
            &:hover {
                background-color: #f6f6f6;  
            }  
            div {
                float: left;       
                height: 54px;     
                line-height: 54px; 
                &.song_rank {
                    width: 100px;     
                    font-weight: bold; 
                    text-align: center; 
                }
                &.song_name {
                    width: 300px;           
                    padding-left: 66px;    
                    box-sizing: border-box; 
                    img {
                        width: 50px;        
                        height: 50px;
                        margin-right: 15px; 
                    }
                }
                &.song_author {
                    width: 200px;           
                    padding-left: 100px;    
                }
                &.song_name, &.song_author {
                    overflow: hidden;          
                    white-space: nowrap;        
                    text-overflow: ellipsis;
                } 
            }           
        }
    }
</style>