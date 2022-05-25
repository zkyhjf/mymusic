<template>
    <!-- 歌曲列表 -->
    <div class="songlist">
        <div class="head">
            <ul>
                <li>序号</li>
                <li>歌曲</li>
                <li>歌手</li>
            </ul>
        </div>

        <ul>
            <li v-for="(song, index) in songList" :key="song.id">
                <a class="song_item" :href="`/player?songid=${song.id}`" target="player">
                    <div class="song_rank">{{index+1}}</div>
                    <div class="song_name">  
                        <img :src="song.pic">
                        {{song.title}}
                    </div>
                    <div class="song_author">{{song.author}}</div>
                </a>
            </li>
        </ul>
    </div>
</template>

<script setup>
    //搜索与我的音乐歌曲列表
    defineProps({
        songList: Array
    })
</script>

<style lang="less" scoped>
    /* 歌曲列表 */
    .songlist {
        width: 1000px;                  
        background-color: #fff;         
        border: 1px solid #d3d3d3;      
        margin-bottom: 50px; 
        .head {
            height: 46px;          
            background: #fafafa;    
            font-size: 15px;       
            color: #999;
            li {
                float: left;          
                line-height: 46px;
                &:first-child {
                    width: 150px;         
                    text-align: center; 
                }
                &:nth-child(2) {
                    width: 450px;          
                    text-align: center; 
                }
                &:nth-child(3) {
                    width: 300px;         
                    text-align: center; 
                }
            }
        }  
        .song_item {
            display: block;         
            height: 54px;           
            padding: 10px 0;         
            color: #333;
            div {
                float: left;        
                height: 54px;       
                line-height: 54px;
                &.song_rank {
                    width: 150px;       
                    font-weight: bold; 
                    text-align: center; 
                }
                &.song_name {
                    width: 450px;           
                    padding-left: 132px;     
                    box-sizing: border-box; 
                    img {
                        width: 50px;            
                        height: 50px;
                        margin-right: 20px; 
                    }
                }
                &.song_author {
                    width: 300px;          
                    text-align: center;     
                }
            }
            .song_name, .song_author {
                overflow: hidden;           
                white-space: nowrap;        
                text-overflow: ellipsis; 
            }
            &:hover {
                background-color: #f6f6f6;  
            }
        }        
    }
</style>