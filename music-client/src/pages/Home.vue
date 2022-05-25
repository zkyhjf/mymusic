<template>
    <Header/>

    <!-- 轮播图 -->
    <div class="banner" v-if="state.banners.length !== 0">
        <!-- 虚化的背景 -->
        <img class="bg" :src="state.banners[state.currentIndex].imageUrl">

        <!-- 轮播图主体 -->
        <div class="container">
            <ul>
                <li class="item" 
                    v-for="(item, index) in state.banners" 
                    :key="item.songid"
                    :class="index == state.currentIndex ? 'active' : ''">
                    <a :href="`/player?songid=${item.songid}`" target="player">
                        <img :src="item.imageUrl">
                    </a>
                </li>
            </ul>

            <!-- 左按钮 -->
            <div class="prev" @click="prevItem"></div>

            <!-- 右按钮 -->
            <div class="next" @click="nextItem"></div>

            <!-- 轮播图指示器 -->
            <ol class="indicator">
                <li class="btn" 
                    v-for="(item, index) in state.banners" 
                    :key="item.songid" 
                    :class="index == state.currentIndex ? 'active' : ''"
                    @click="state.currentIndex = index">
                </li>
            </ol>
        </div>
    </div>

    <!-- 排行榜 -->
    <Suspense>
        <template #default>
            <div class="toplist container">
                <div class="index_hd">
                    <span class="index_title">排行榜</span>
                    <router-link to="/toplist">更多</router-link>
                </div>
                
                <ul class="toplist_list">
                    <TopListItem :category="1"/>
                    <TopListItem style="background-position-x: -224px" :category="2"/>
                    <TopListItem style="background-position-x: -448px" :category="3"/>
                    <TopListItem style="background-position-x: -672px" :category="4"/>
                </ul>
            </div>
        </template>
    </Suspense>
</template>

<script setup>
    import Header from '@/components/Header'
    import { defineAsyncComponent, reactive, onMounted, onBeforeUnmount } from 'vue'
    import { httpManager } from '@/api'
    const TopListItem = defineAsyncComponent(() => import('@/components/TopListItem'))

    const state = reactive({
        //轮播图数据
        banners: [
            {"songid": 1942989841, "imageUrl": "http://p1.music.126.net/ZbNptetcUImo4dOci5jh4g==/109951167377415576.jpg"},
            {"songid": 1944400288, "imageUrl": "http://p1.music.126.net/foZET3jZMzkLPIr3txqKTA==/109951167377427847.jpg"},
            {"songid": 1941258524, "imageUrl": "http://p1.music.126.net/bILA-yRotgu9udT8LY7wQA==/109951167377432239.jpg"},
            {"songid": 1942728752, "imageUrl": "http://p1.music.126.net/aa6XZv6k_Uyyg57e4CwVWw==/109951167377437715.jpg"},
            {"songid": 1944487721, "imageUrl": "http://p1.music.126.net/hAZFOCnJd8W-DxSybWil7A==/109951167377641623.jpg"},
            {"songid": 1940334604, "imageUrl": "http://p1.music.126.net/M1v0Q5GpoX3kBujHys70bg==/109951167372891401.jpg"}
        ],
        currentIndex: 0     //当前轮播图索引
    })

    let timer;            //定时器

    onMounted(() => {
        //设置定时器
        setTimer()
    })

    onBeforeUnmount(() => {
        //清除定时器
        clearInterval(timer)
    })

    //设置定时器，每5秒切换下一张轮播图
    function setTimer() {
        timer = setInterval(() => {
            nextItem()
        }, 5000)
    }

    //切换上一张轮播图
    function prevItem() {
        clearInterval(timer)
        if(state.currentIndex == 0) {
            state.currentIndex = state.banners.length - 1
        } else {
            state.currentIndex--
        }
        setTimer()
    }

    //切换下一张轮播图
    function nextItem() {
        clearInterval(timer)
        if(state.currentIndex == state.banners.length - 1) {
            state.currentIndex = 0
        } else {
            state.currentIndex++
        }
        setTimer()
    }
</script>

<style lang="less" scoped>
    /* 轮播图 */
    .banner {
        position: relative;     
        height: 370.37px;          
        overflow: hidden; 
        .bg{
            position: absolute;     
            top: -50%;                      
            left: -50%;
            width: 200%;            
            height: 200%;
            filter: blur(75px);    
        }
        .container {
            position: relative;    
            height: 370.37px; 
            .item {
                position: absolute;     
                left: 0;                
                top: 0;                 
                opacity: 0;            
                z-index: 1;
                /* 显示图片 */
                &.active {
                    opacity: 1;     
                    z-index: 2;    
                    transition: opacity 1s;
                }
                img {
                    width: 1000px;       
                    height: 370.37px; 
                }
            }
            /* 轮播图左按钮 */
            .prev {
                position: absolute;     
                top: 50%;  
                transform: translateY(-50%);     
                left: -74px;           
                width: 37px;            
                height: 63px;
                background: url('../assets/images/sprite.png') 0px -10px;  
                cursor: pointer; 
                &:hover {
                     background: url('../assets/images/sprite.png') 0px -80px; 
                }       
            } 
            /* 轮播图右按钮*/
            .next {
                position: absolute;     
                top: 50%;  
                transform: translateY(-50%);           
                right: -74px;          
                width: 37px;            
                height: 63px;
                background: url('../assets/images/sprite.png') 0px -158px; 
                cursor: pointer;
                &:hover {
                    background: url('../assets/images/sprite.png') 0px -228px; 
                }        
            } 
            /* 轮播图指示器 */ 
            .indicator {
                position: absolute;    /* 设置定位方式为绝对定位 */  
                bottom: 20px;          
                left: 50%; 
                transform: translateX(-50%);        
                z-index: 3;            /* 设置元素的层级 */
                li {
                    float: left;           
                    width: 10px;           
                    height: 10px;
                    margin: 0 15px;         
                    border-radius: 50%;     
                    background-color: rgba(255,255,255,.43);
                    &.active, &:hover {
                        background-color: #fff;
                    } 
                } 
            }      
        }
    }

    /* 排行榜 */
    .index_hd {
        position: relative;     
        height: 114px;          
        line-height: 114px;     
        text-align: center; 
        .index_title {
            font-size: 30px;        
            font-weight: bold;     
            letter-spacing: 10px;   
        }
        a {
            position: absolute;     
            height: 20px;           
            right: 0; 
            &:hover {
                color: #008fd9;       
                text-decoration: underline; 
            }   
        }   
    }

    .toplist_list {
        height: 500px;          
        display: flex;
        justify-content: space-between;
    }
</style>