<template>
    <li class="toplist_list_item">
        <router-link :to="`/toplist/${category}`">
            <h3 v-if="category == 1">飙升榜</h3>
            <h3 v-if="category == 2">新歌榜</h3>
            <h3 v-if="category == 3">原创榜</h3>
            <h3 v-if="category == 4">热歌榜</h3>
            <img class="icon" src="@/assets/images/cover_play.png">
            <div class="toplist_line"></div>
            <ul class="songlist">
                <li v-for="(song, index) in topList" :key="song.id">
                    <div class="number">{{index+1}}</div>
                    <div class="songname">{{song.title}}</div>
                    <div class="author">{{song.author}}</div>
                </li>
            </ul>
        </router-link>
    </li>
</template>

<script setup>
    //首页排行榜显示项
    import { httpManager } from '@/api'
    import { reactive } from 'vue'

    const props = defineProps({ category: Number })     //排行榜类别

    //排行榜查询参数
    const queryInfo = reactive({
        category: props.category,
        size: 4
    })

    //获取排行榜前四名歌曲数据
    const { data: res } = await httpManager.getTopList(queryInfo)
    const topList = res.data
</script>

<style lang="less" scoped>
    .toplist_list_item {
        position: relative;                          
        float: left;                                 
        height: 500px;                               
        width: 224px;
        background: url(../assets/images/bg_toplist.jpg);
        &:hover .toplist_line {
            visibility: hidden;                        
        }
        &:hover .icon {
            visibility: visible;                        
            opacity: 1;                                 
            transform: scale(1);                        
            transition: all 0.6s;                       
        }
        a {
            display: block;            
            height: 100%;              
            width: 100%;
            color: #fff;
            h3 {
                font-size: 25px;            
                font-weight: normal;        
                text-align: center;       
                padding-top: 35px; 
            }
            .icon {
                display: block;            
                width: 49px;                
                height: 49px;
                margin: 25px auto;         
                visibility: hidden;         
                transform: scale(0.8);      
                opacity: 0.2;              
                transition: all 0.1s;       
            }
            .toplist_line {
                position: absolute;        
                top: 120px;                 
                left: 50%;
                transform: translateX(-50%);    
                width: 36px;                   
                height: 2px;
                background-color: #fff;      
            }
            .songlist {
                width: 164px;              
                margin-left: 30px;          
                font-size: 15px;           
                white-space: nowrap; 
                li {
                    position: relative;        
                    margin-bottom: 25px;
                    .number {
                        position: absolute;        
                        top: 0;                     
                        left: 0;
                    }
                    .songname, .author{
                        margin-left: 20px;         
                        overflow: hidden;          
                        text-overflow: ellipsis;    
                    }
                }       
            }
        }
    }
</style>