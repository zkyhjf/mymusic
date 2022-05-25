<template>
    <Header/>

    <div class="container">
        <!-- 排行榜侧边栏 -->
        <aside class="tab fl">
            <ul>
                <li>
                    <router-link to="/toplist/1" active-class="active">
                        <img src="@/assets/images/toplist_1.jpg" alt="飙升榜">
                        <div class="item_info">
                            <p class="name">飙升榜</p>
                            <p class="time">今日更新</p>
                        </div>
                    </router-link>
                </li>
                <li>
                    <router-link to="/toplist/2" active-class="active">  
                        <img src="@/assets/images/toplist_2.jpg" alt="新歌榜">
                        <div class="item_info">
                            <p class="name">新歌榜</p>
                            <p class="time">今日更新</p>
                        </div>
                    </router-link>
                </li> 
                <li>
                    <router-link to="/toplist/3" active-class="active">
                        <img src="@/assets/images/toplist_3.jpg" alt="原创榜">
                        <div class="item_info">
                            <p class="name">原创榜</p>
                            <p class="time">每周更新</p>
                        </div>
                    </router-link>
                </li>
                <li>
                    <router-link to="/toplist/4" active-class="active">
                        <img src="@/assets/images/toplist_4.jpg" alt="热歌榜">
                        <div class="item_info">
                            <p class="name">热歌榜</p>
                            <p class="time">今日更新</p>
                        </div>
                    </router-link>
                </li>
            </ul>
        </aside>

        <router-view></router-view>
    </div>
</template>

<script setup>
    import Header from '@/components/Header'
</script>

<style lang="less" scoped>
    /* 排行榜侧边栏 */
    .tab {
        width: 237px;                 
        background-color: #fafafa;      
        border: 1px solid #d3d3d3;    
        border-right: hidden;         
        box-sizing: border-box;
        li {
            a {
                display: flex;             
                align-items: center;        
                height: 80px;              
                padding-left: 20px;
                &.active {
                    background-color: #e6e6e6; 
                }
                &.hover:hover {
                     background-color: #f5f3f3; 
                }
                img {
                    width: 60px;           
                    height: 60px;
                    margin-right: 12px; 
                }
                .item_info {
                    .name {
                        font-size: 15px;        
                        font-weight: 600;
                    }
                    .time {
                        font-size: 14px;       
                        color: #999;
                    }
                }
            }
        }      
    }
</style>