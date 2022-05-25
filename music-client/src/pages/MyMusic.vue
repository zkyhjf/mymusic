<template>
    <Header/>
        <!-- 个人信息 -->
    <div class="user_info">
        <div class="user_info_wrap">
            <div class="user_icon"></div>
            <p class="username">{{loginUsername}}</p>
        </div>
    </div>

    <!-- 歌曲列表 -->
    <SongList class="container" :songList="songList"/>
</template>

<script setup>
    import Header from '@/components/Header'
    import SongList from '@/components/SongList'
    import { useStore } from 'vuex'
    import { computed, onMounted, ref } from 'vue'
    import { httpManager } from '@/api'

    const store = useStore()
    const songList = ref([])

    //登录用户名
    const loginUsername = computed(() => {
        return store.state.user.loginUser.username
    })

    onMounted(async () => {
        //获取用户收藏歌曲
        const { data: res } = await httpManager.getFavorites()
        if(res.status === 200) {
            songList.value = res.data
        }
    })
</script>

<style lang="less" scoped>
    /* 个人信息 */ 
    .user_info {
        height: 315px;                                          
        background: url(../assets/images/bg_profile.jpg);  
        background-size: cover;  
        .user_info_wrap {
            width: 110px;          
            height: 315px;
            margin: 0 auto;         
            padding-top: 50px;      
            box-sizing: border-box;
            .user_icon {
                width: 110px;                               
                height: 110px;
                border-radius: 50%;                         
                background: url(../assets/images/user-icon.jpg);   
                background-size: cover;                     
                border: 4px solid #fff;                   
                box-sizing: border-box;                     
            }
            .username {
                font-size: 30px;            
                color: #fff;              
                text-align: center;         
                overflow: hidden;          
                white-space: nowrap;        
                text-overflow: ellipsis;   
            }
        }                     
    }
</style>