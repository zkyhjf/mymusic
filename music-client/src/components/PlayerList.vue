<template>
    <div class="songlist fl">
        <ul class="songlist_header">
            <li class="songlist_header_name fl">歌曲</li>
            <li class="songlist_header_author fl">歌手</li>
            <li class="songlist_header_time">时长</li>
        </ul>

        <ul class="songlist_list" ref="songListRef">
            <li class="songlist_item" 
                v-for="(song, index) in songList" 
                :key="song.songid"
                :class='{playing: currentIndex == index && isPlaying}'
            >
                <div class="songlist_number">{{index+1}}</div>
                <div class="songlist_songname fl">
                    <span class="songname_content">{{song.title}}</span>
                    <a class="songlist_play fr" @click="handlePlay(index)">
                        <span class="icon_txt">播放</span>
                    </a>
                </div>
                <div class="songlist_artist fl">{{song.author}}</div>
                <div class="songlist_time">{{formatTime(song.duration)}}</div>
                <a class="songlist_delete" @click="handleDelete(index)"><span class="icon_txt">删除</span></a>
            </li>
        </ul>
    </div>
</template>

<script setup>
    import { watch, ref, nextTick, onMounted } from 'vue'
    import { useStore } from 'vuex'

    const props = defineProps({
        songList: Array,
        currentIndex: Number,
        isPlaying: Boolean
    })

    const store = useStore()
    const emit = defineEmits(['playMusic', 'deleteMusic'])
    const songListRef = ref(null)
    const isFirst = ref(true)

    watch(() => props.currentIndex, () => {
        if(isFirst.value) {
            //在下一次 DOM 更新结束后执行其指定的回调
            nextTick(function() {
                setScrollPosition()
            })
        }
    })

    watch(() => store.state.song.scrollTop, value => {
        songListRef.value.scrollTop = value
    })

    onMounted(() => {
        if(props.currentIndex !== 0) {
            setScrollPosition()
        }
    })

    //播放指定歌曲
    function handlePlay(index) {
        emit('playMusic', index)
    }

    //删除指定索引的歌曲
    function handleDelete(index) {
        emit('deleteMusic', index)
    }

    //指定滚动条位置
    function setScrollPosition() {
        if(isFirst.value) isFirst.value = false
        songListRef.value.scrollTop = (props.currentIndex - 4) * 50
    }

    //播放时间格式化
    function formatTime(time) {
        //无时间，显示00:00
        if(typeof(time) == "undefined") return "00:00"
        var minute = parseInt(time / 60);   //计算分钟数
        var second = parseInt(time % 60);   //计算秒数

        //转换时间格式，长度为2位，不足补零
        var minuteStr = (Array(2).join('0') + minute).slice(-2);
        var secondStr = (Array(2).join('0') + second).slice(-2);
        return minuteStr + ":" + secondStr;
    }
</script>

<style lang="less" scoped>
    /* 歌曲播放列表界面 */
    .icon_txt {
        font: 0/0 a;        
    }
    ::-webkit-scrollbar {
        width: 8px;           
        height: 10px;
    }
    ::-webkit-scrollbar-track {
        background: transparent;   
    }
    ::-webkit-scrollbar-thumb {
        background-color: rgba(0,0,0,.1);    
        border-radius: 5px;                   
    }
    ::-webkit-scrollbar-thumb:hover {
        background-color: rgba(0,0,0,.3);   
    }
    /* 播放列表 */
    .songlist {
        width: 680px;       
        height: 100%;
        user-select: none; 
        .songlist_header {
            position: relative; 
            height: 50px;      
            padding-left: 50px; 
            color: #fff;     
            font-size: 15px;    
            z-index: 2;        
        }
        .songlist_list {
            height: 100%;        
            width: 688px;
            overflow-x: hidden;  
            overflow-y: scroll;  
            .songlist_item {
                position: relative;     
                width: 100%;            
                height: 50px;
                padding-left: 50px;    
                box-sizing: border-box;
                color: #fff;            
                font-size: 15px;       
                z-index: 2;  
                .songlist_number {
                    position: absolute;     
                    left: 5px;              
                    top: 0;
                    width: 36px;            
                    height: 50px;
                    line-height: 50px;     
                    text-align: right;     
                } 
                /* 正在播放的歌曲前添加波浪动态图  */
                &.playing .songlist_number {
                    left: 30px;             
                    top: 20px;
                    width: 10px;            
                    height: 10px;
                    background: url(../assets/images/wave.gif);  
                    /* 隐藏文字 */
                    text-indent: -99px;
                    overflow: hidden;
                } 
                .songname_content {
                    display: inline-block;  
                    width: 220px;           
                } 
                .songlist_play {
                    display: none;                  
                    width: 36px;                    
                    height: 36px;
                    margin-top: 7px;                
                    background: url(../assets/images/sprite.png) -289px 0px;   
                    cursor: pointer; 
                    &:hover {
                        background-position: -329px 0px;
                    }              
                }
                .songlist_delete {
                    display: none;                  
                    position: absolute;             
                    top: 7px;                       
                    right: 56px;
                    width: 36px;                   
                    height: 36px;
                    background: url(../assets/images/sprite.png) -289px -160px;    
                    cursor: pointer; 
                    &:hover {
                        background-position: -329px -160px;
                    }       
                }
                /* 鼠标悬浮显示播放和删除按钮，隐藏播放时间 */  
                &:hover .songlist_play {
                    display: inline-block; 
                } 
                &:hover .songlist_delete {
                    display: inline-block;       
                }
                &:hover .songlist_time{
                    display: none;                
                }
                /* 正在播放的歌曲添加暂停按钮 */ 
                &.playing .songlist_play {
                    background-position: -289px -200px;
                    &:hover {
                        background-position: -329px -200px;
                    }
                } 
            }
        }
        .songlist_header_name, .songlist_songname {
            width: 305px;          
            height: 50px;
            line-height: 50px;      
            padding-right: 40px;    
            box-sizing: border-box; 
        }
        .songlist_header_author, .songlist_artist {
            width: 26%;             
            height: 50px;
            line-height: 50px;      
        }
        .songlist_header_time, .songlist_time {
            position: absolute;    
            top: 0px;              
            right: 38px;    
            width: 50px;            
            height: 50px;
            line-height: 50px;     
        }
    }
    .songlist_item .songname_content, .songlist_item .songlist_artist {
        /* 单行文本溢出显示省略号 */
        overflow: hidden;
        white-space: nowrap;
        text-overflow: ellipsis;
    }
</style>