<template>
    <Header/>
        
    <!-- 搜索信息 -->
    <div class="search_info">
        <div class="search_input">
            <input type="text" placeholder="搜索音乐" :value="state.keyword" @keyup.enter="handleEnter">
        </div>
        <div class="search_tips">
            热门搜索：
            <a href="javascript:;" @click="handleClick">张杰</a>
            <a href="javascript:;" @click="handleClick">删了吧</a>
            <a href="javascript:;" @click="handleClick">星辰大海</a>
            <a href="javascript:;" @click="handleClick">漠河舞厅</a>
            <a href="javascript:;" @click="handleClick">致你</a>
        </div>
    </div>

    <SongList class="container" :songList="state.songList"/>
</template>

<script setup>
    import Header from '@/components/Header'
    import SongList from '@/components/SongList'
    import { httpManager } from '@/api'
    import { reactive, ref, watch } from 'vue'
    import { useRouter } from 'vue-router'

    const router = useRouter()
    const props = defineProps({ keyword: String })
    const state = reactive({
        songList: [],
        keyword: props.keyword
    })

    watch(() => props.keyword, keyword => {
        searchMusic(keyword)
    }, { immediate: true })

    //用户在输入框回车
    function handleEnter(e) {
        searchMusic(e.target.value)
    }

    //用户点击关键词
    function handleClick(e) {
        searchMusic(e.target.text)
    }

    //根据关键词搜索音乐
    async function searchMusic(keyword) {
        const { data: res } = await httpManager.searchMusic(keyword)
        router.push({
            path: '/search',
            query: { keyword }
        })
        state.keyword = keyword
        state.songList = res.data
    }
</script>

<style lang="less" scoped>
    /* 搜索信息 */
    .search_info {
        height: 247px;                                  
        background: url(../assets/images/bg_search.jpg);      
        background-size: cover;                         
        padding-top: 90px;                              
        box-sizing: border-box; 
        .search_input {
            position: relative;            
            width: 554px;                   
            height: 45px;       
            margin: 0 auto;
            input {
                width: 554px;                  
                height: 45px;
                border-radius: 5px;             
                padding-left: 10px;             
                padding-right: 35px;          
                box-sizing: border-box; 
            }
            /* 添加搜索图标 */
            &::after {
                position: absolute;             
                top: 14.5px;                   
                right: 10px;
                content: '';                  
                width: 16px;                  
                height: 16px;
                background: url(../assets/images/sprite.png) -167px -16px;      
            }
        }
        .search_tips {
            display: flex;                  
            justify-content: center;        
            width: 554px;                 
            height: 21px;
            margin: 15px auto;              
            color: #fff;                    
            font-size: 15px; 
            a {
                color: #fff;                    
                margin-right: 20px; 
                &:last-child {
                    margin-right: 0; 
                }
            }
        }                       
    }
</style>