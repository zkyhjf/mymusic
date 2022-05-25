<template>
    <div class="player">
        <!-- 背景-->
        <img :src="song.pic" class="player_bg">

        <!-- 灰色遮罩 -->
        <div class="player_mask"></div>

        <!-- 歌曲播放列表界面 -->
        <div class="player_list" v-if="!state.isOnly">
            <!-- 播放列表 -->
            <PlayerList 
                :songList="state.songList" 
                :currentIndex="state.currentIndex" 
                :isPlaying="state.isPlaying" 
                @playMusic="playMusic"
                @deleteMusic="deleteMusic"
            />

            <!-- 歌曲信息 -->
            <div class="song_info fr">
                <div class="song_cover">
                    <img :src="song.pic" alt="" class="song_pic">
                </div>
                <div class="song_name">歌曲名：{{song.title}}</div>
                <div class="song_author">歌手：{{song.author}}</div>
            </div>
        </div>
        
        <!-- 显示歌词界面 -->
        <PlayerLyric v-if="state.isOnly"/>

        <!-- 播放器底部操作栏 -->
        <div class="player_footer">

            <!-- 上一首按钮 -->
            <a class="btn btn_prev" @click="prevMusic">
                <span class="icon_txt">上一首</span>
            </a>

            <!-- 播放按钮 -->
            <a class="btn btn_play" @click="state.isPlaying = !state.isPlaying" ref="btn_play">
                <span class="icon_txt">播放</span>
            </a>

            <!-- 下一首按钮 -->
            <a class="btn btn_next" @click="nextMusic">
                <span class="icon_txt">下一首</span>
            </a>
            
            <!-- 音乐播放信息显示 -->
            <div class="player_music">
                <div class="player_music_top">
                    <!-- 歌曲名称及作者 -->
                    <div class="player_music_info fl">
                        <a href="" class="title">{{song.title}}</a> -
                        <a href="" class="author">{{song.author}}</a>
                    </div>
                    <div class="player_music_time fr">
                        <span class="current_time">{{formatTime(song.currentTime)}}</span> /
                        <span class="duration">{{formatTime(song.duration)}}</span>
                    </div>
                </div>
                <div class="player_progress" @mousedown="clickProgress" ref="playerProgress">
                    <div class="player_progress_inner">
                        <div class="player_progress_play" ref="progressBar">
                            <i 
                                class="player_progress_dot" 
                                @mousedown.stop="pullProgress"
                            ></i>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 音乐播放循环 -->
            <a class="btn btn_list" title="列表循环">
                <span class="icon_txt">列表循环</span>
            </a>

            <!-- 添加喜欢按钮 -->
            <a class="btn btn_like" @click="operateFavorites" ref="btn_like">
                <span class="icon_txt">喜欢</span>
            </a>

            <!-- 下载按钮 -->
            <a class="btn btn_download" :href="`/song/download?songid=${song.id}`">
                <span class="icon_txt">下载</span>
            </a>

            <!-- 显示模式 -->
            <a class="btn btn_only" @click="state.isOnly = !state.isOnly" ref="btn_only">
                <span class="icon_txt">打开纯净模式</span>
            </a>

            <!-- 音量控制 -->
            <div class="player_progress player_voice">
                <!-- 音量开关按钮 -->
                <a class="btn btn_voice">
                    <span class="icon_txt">关闭声音</span>
                </a>

                <!-- 音量进度条 -->
                <div class="player_progress_inner">
                    <div class="player_progress_play">
                        <i class="player_progress_dot"></i>
                    </div>
                </div>
            </div>
        </div>

        <!-- 音乐播放器 -->
        <audio preload="auto" :src="song.url" ref="audio"></audio>
    </div>
</template>

<script setup>
    import { useStore } from 'vuex'
    import { useRouter } from 'vue-router'
    import { computed, onMounted, reactive, ref, watch } from 'vue'
    import PlayerList from '@/components/PlayerList'
    import PlayerLyric from '@/components/PlayerLyric'
    import { httpManager } from '@/api'
    import { ElMessage } from 'element-plus'

    const state = reactive({
        songList: [],               //当前播放列表
        currentIndex: 0,            //当前播放歌曲索引
        isPlaying: false,           //当前歌曲是否正在播放
        isOnly: false,              //是否为纯净模式
        isPulling: false,           //用户是否正拖动进度条
        isFirst: true,              //是否为初次加载
        isFavorites: false          //是否为用户收藏
    })

    const audio = ref(null)
    const progressBar = ref(null)
    const playerProgress = ref(null)
    const btn_play = ref(null)
    const btn_only = ref(null)
    const btn_like = ref(null)

    const store = useStore() 
    const router = useRouter()
    const props = defineProps({ songid: String })
    const song = computed(() => store.state.song.song)  //当前播放歌曲 

    //设置当前播放歌曲id
    store.commit('song/setSongid', props.songid)

    watch(() => song.value.id, value => {
        //获取歌曲详细信息
        getSongDetail(value)

        //获取歌曲收藏状态
        if(localStorage.getItem('token')) {
            httpManager.checkFavorites(value)
                .then(res => {
                    state.isFavorites = res.data.data.is_favorites
                }, () => {
                    state.isFavorites = false
                })
        }
    }, { immediate: true })

    //当前播放歌曲索引改变时跳转至对应歌曲
    watch(() => state.currentIndex, index => {
        if(!state.isFirst) {
            //设置当前播放歌曲id
            store.commit('song/setSongid', state.songList[index].id)

            //设置当前歌曲播放行为0
            store.commit('song/setLineNo', 0)

            //更改路由
            router.replace({ path: '/player', query: { songid: song.value.id } })
        }
    })

    //根据播放状态决定是否播放歌曲
    watch(() => state.isPlaying, flag => {
        if(flag) {
            audio.value.play()
            btn_play.value.style = "background-position: -78px -44px"
        } else {
            audio.value.pause()
            btn_play.value.style = "background-position: -48px -45px"
        }
    })

    //修改播放模式
    watch(() => state.isOnly, flag => {
        if(flag) {
            btn_only.value.style = "background-position: -48px -355px"
        } else {
            btn_only.value.style = "background-position: -48px -326px"
        }
    })

    //修改歌曲收藏状态
    watch(() => state.isFavorites, flag => {
        if(flag) {
            btn_like.value.style = "background-position: -78px -140px"
        } else {
            btn_like.value.style = "background-position: -48px -140px"
        }
    })

    onMounted(() => {
        if(state.isFirst) {
            state.isFirst = false
        }

        document.onkeyup = e => {
            //按空格控制歌曲播放
            if(e.key === ' ') {
                state.isPlaying = !state.isPlaying
            }

            //按左箭头切换上一曲
            if(e.key === 'ArrowLeft') {
                prevMusic()
            }

            //按右箭头切换下一曲
            if(e.key === 'ArrowRight') {
                nextMusic()
            }
        }

        audio.value.oncanplay = () => {
            //播放歌曲
            audio.value.play()

            //获取歌曲总时长
            store.commit('song/setDuration', audio.value.duration)

            //保存歌曲信息到本地存储
            savePlaySongData(song.value.id, song.value.title, song.value.author, song.value.duration)
        
            //获取当前播放歌曲索引
            getCurrentIndex()
        }

        audio.value.ontimeupdate = () => {
            if(!state.isPulling) {
                //获取歌曲当前播放时长
                const currentTime = audio.value.currentTime
                store.commit('song/setCurrentTime', currentTime)

                //计算当前播放进度
                const progress = currentTime / song.value.duration
                progressBar.value.style = "width:" + progress * 100 + "%"

                //计算当前歌词所在行
                if(!state.isPulling) {
                    store.dispatch('song/getLineNo')
                }
                
                //自动播放下一首
                if(progress == 1) {
                    nextMusic()
                }
            }
        }

        //同步歌曲播放状态
        audio.value.onplay = () => {
            state.isPlaying = true
        }

        audio.value.onpause = () => {
            state.isPlaying = false
        }
    })

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

    //根据歌曲id获取歌曲详情
    async function getSongDetail(songid) {
        const { data: res } = await httpManager.getSongDetail(songid)
        store.commit('song/setSong', res.data)
        store.dispatch('song/parseLyric')
    }

    //保存当前播放歌曲信息到本地存储
    function savePlaySongData(songid, title, author, duration) {
        //获取本地存储中的播放列表
        const data = localStorage.getItem("playSongData")

        //将播放列表转换为json对象
        let playSongData = JSON.parse(data)

        if(playSongData === null) {
            //播放列表为空则初始化播放列表
            playSongData = {songList: []}
        }

        //获取歌曲数组
        let songList = playSongData.songList

        //判断歌曲数组中是否包含当前歌曲
        let flag = false;
        songList.forEach(song => {
            if(song.id === songid) {
                flag = true
            }
        })

        //歌曲数组中不包含当前歌曲，则将当前歌曲添加到数组开头
        if(!flag) {
            songList.unshift({id: songid, title, author, duration})
        }

        //保存数据到本地存储
        localStorage.setItem("playSongData", JSON.stringify({songList}))

        state.songList = songList
    }

    //用户点击进度条修改歌曲播放进度
    function clickProgress(e) {
        const dx = e.currentTarget.getBoundingClientRect().x           //获取进度条在屏幕中的位置
        const progress = (e.pageX - dx) / e.currentTarget.clientWidth;  //计算当前进度

        if(progress > 0) {
            //修改进度条显示效果
            progressBar.value.style = "width:" + progress * 100 + "%"

            //修改歌曲已播放时长
            audio.value.currentTime = audio.value.duration * progress
        }
    }

    //用户拖动进度条修改进度
    function pullProgress() {
        //修改正在拖动进度条为true
        state.isPulling = true
        const dx = playerProgress.value.getBoundingClientRect().x           //获取进度条在屏幕中的位置
        
        document.onmousemove = (e) => {
            //计算显示进度宽度
            const width = e.pageX - dx
            
            //计算进度值
            let progress = width / playerProgress.value.clientWidth
            
            //控制进度范围为0~1
            if(progress < 0) {
                progress = 0
            }
            if(progress > 1) {
                progress = 1
            }

            //修改进度条显示效果
            progressBar.value.style = "width:" + progress * 100 + "%"

            //计算歌曲已播放时长
            store.commit('song/setCurrentTime', song.value.duration * progress)
        }

        document.onmouseup = () => {
            //修改正在拖动进度条为false
            state.isPulling = false

            //歌曲跳转至最终进度
            audio.value.currentTime = song.value.currentTime

            //清除鼠标移动和点击回调
            document.onmousemove = null
            document.onmouseup = null
        }
    }

    //获取当前播放歌曲索引
    function getCurrentIndex() {
        for (let i = 0; i < state.songList.length; i++) {
            if(state.songList[i].id === song.value.id) {
                state.currentIndex = i
                return
            }
        }
    }

    //切换至上一首
    function prevMusic() {
        if(state.currentIndex === 0) {
            state.currentIndex = state.songList.length - 1
        } else {
            state.currentIndex--
        }
        setScrollPosition()
    }

    //切换至下一首
    function nextMusic() {
        if(state.currentIndex === state.songList.length - 1) {
            state.currentIndex = 0
        } else {
            state.currentIndex++
        }
        setScrollPosition()
    }

    //设置歌曲列表滚动条位置
    function setScrollPosition() {
        store.commit('song/setScrollTop', (state.currentIndex - 4) * 50)
    }

    //播放指定索引的歌曲
    function playMusic(index) {
        if(index === state.currentIndex) {
            state.isPlaying = !state.isPlaying
            return
        }
        state.currentIndex = index
    }

    //删除指定索引的歌曲
    function deleteMusic(index) {
        //删除歌曲
        state.songList.splice(index, 1)

        //将删除后的歌曲列表保存至本地存储
        localStorage.setItem("playSongData", JSON.stringify({ songList: state.songList }))

        //更新当前播放索引
        //删除歌曲索引小于当前播放歌曲索引
        if(index < state.currentIndex) {
            state.currentIndex--
        }

        //播放列表为空
        if(state.songList.length === 0) {
            song.value = {}
            return
        }

        //删除当前播放歌曲
        if(index === state.currentIndex) {
            if(index < state.songList.length) {
                song.value.id = state.songList[index].id
            } else {
                song.value.id = state.songList[index - 1].id
            }
        }
    }

    //操作收藏歌曲
    function operateFavorites() {
        //根据是否保存token判断用户是否登录
        const token = localStorage.getItem('token')
        if(!token) {
            return ElMessage.error('请登录')
        }
        
        if(state.isFavorites) {
            //当前歌曲为用户收藏，进行取消用户收藏操作
            httpManager.deleteFavorites(song.value.id)
                .then(
                    () => { state.isFavorites = false }, 
                    () => { state.isFavorites = false }
                )
        } else {
            //当前歌曲不为用户收藏，进行添加用户收藏操作
            httpManager.addFavorites(song.value.id)
                .then(
                    () => { state.isFavorites = true }, 
                    () => { state.isFavorites = false }
                )
        }
    }
</script>

<style lang="less" scoped>
    .player {
        position: absolute;    
        width: 100%;            
        height: 100%;
        background-color: rgba(0, 0, 0, .6);
        overflow: hidden; 
        .player_bg {
            position: absolute; 
            top: 0;
            left: 0;   
            width: 100%;        
            height: 100%;       
            filter: blur(65px); 
            opacity: .6;        
            transform: scale(1.5);
            background-color: #fff;
        }  
        .player_mask {
            position: absolute; 
            top: 0;             
            left: 0;
            width: 100%;       
            height: 100%;
            background-color: rgba(0,0,0,.35); 
            z-index: 2;        
        }
        .player_list {
            position: absolute; 
            top: 11%;           
            bottom: 25%;        
            left: 50%;
            transform: translateX(-50%);    
            width: 1157px;      
            margin: 0 auto;     
            z-index: 2;
            /* 歌曲信息 */
            .song_info {
                width: 340px;           
                height: 285px;
                .song_cover {
                    position: relative;     
                    text-align: center; 
                    /* 添加专辑修饰图 */
                    &::after {
                        position: absolute;     
                        content: '';           
                        left: 86px;             
                        top: 0;
                        width: 201px;           
                        height: 180px;
                        background: url(../assets/images/album_cover.png);   
                    }
                    img {
                        width: 186px;          
                        height: 186px;
                    }    
                }
                .song_name, .song_author {
                    width: 100%;           
                    height: 40px;
                    text-align: center;     
                    line-height: 40px;     
                    color: #fff;           
                    font-size: 15px;       
                    /* 单行文本溢出显示省略号 */
                    overflow: hidden;       
                    white-space: nowrap;
                    text-overflow: ellipsis;
                }
                .song_name {
                    margin-top: 15px; 
                }
            }          
        }
        /* 播放器底部操作栏 */
        .player_footer {
            position: fixed;    
            bottom: 0;          
            left: 50%;          
            transform: translateX(-50%);    
            width: 1157px;     
            height: 11%;
            z-index: 3;  
            .btn {
                opacity: .8;       
                cursor: pointer;
                background-image: url(../assets/images/sprite.png);
                &:hover {
                    opacity: 1;
                }
            }  
            .btn_prev {
                position: absolute; 
                top: 8px;              
                left: 0;
                width: 19px;        
                height: 20px;
                background-position: -48px -74px;   
            } 
            .btn_play {
                position: absolute; 
                top: 4px;             
                left: 65px;
                width: 21px;       
                height: 29px;
                background-position: -48px -45px;    
            }
            .btn_next {
                position: absolute;  
                top: 8px;            
                left: 132px;
                width: 19px;         
                height: 20px;
                background-position: -48px -96px;    
            }
            .player_music {
                position: absolute; 
                top: 0;            
                left: 215px;
                width: 495px;       
                height: 40px;
                font-size: 14px;    
                font-family: poppin;    
                color: #fff;           
                user-select: none;
                .player_music_top {
                    height: 28px;  
                    .player_music_info {
                        width: 300px;
                        /* 单行文本溢出显示省略号 */
                        overflow: hidden;
                        white-space: nowrap;    
                        text-overflow: ellipsis; 
                        a {
                            font-size: 14px;        
                            font-family: poppin;    
                            color: #fff;
                        }
                    }         
                }
            }
            .player_progress {
                height: 5px;           
                padding-top: 2px;      
                cursor: pointer; 
                .player_progress_inner{
                    position: relative;     
                    height: 2px;            
                    background-color: rgba(255,255,255,.4);
                    .player_progress_play {
                        position: absolute;    
                        top: 0;                 
                        left: 0;
                        height: 2px;            
                        width: 0%;             
                        background-color: #fff; 
                        .player_progress_dot {
                            position: absolute;     
                            top: -4px;             
                            right: -4px;
                            width: 10px;           
                            height: 10px;
                            border-radius: 50%;    
                            background-color: #fff; 
                        }
                    }
                }       
            }
            .btn_list {
                position: absolute;     
                top: 4px;               
                right: 378px;       
                width: 26px;                 
                height: 25px;
                background-position: -48px -249px;   
            }
            .btn_like {
                position: absolute;     
                top: 5px;               
                right: 320px;
                width: 23px;            
                height: 21px;
                background-position: -48px -140px;   
            }
            .btn_download {
                position: absolute;     
                top: 4px;               
                right: 260px;
                width: 22px;            
                height: 21px;
                background-position: -48px -164px;   
            }
            .btn_only {
                position: absolute;     
                top: 3px;               
                right: 150px;
                width: 74px;            
                height: 26px;
                background-position: -48px -326px;   
            }
            .player_voice {
                position: absolute;    
                top: 0;                
                right: 0px;
                width: 80px;           
                padding-top: 13px;     
                .btn_voice {
                    position: absolute;     
                    top: 4px;              
                    left: -31px;
                    width: 26px;            
                    height: 21px;
                    background-position:  -48px -188px; 
                }
                .player_progress_play{
                    width: 100% !important;       
                }
            }
            
        }
        .icon_txt {
            font: 0/0 a;       
        }
        /* 隐藏音乐播放器标签 */
        audio {
            width: 0;
            height: 0;
        }
    }
</style>