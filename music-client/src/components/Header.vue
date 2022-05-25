<template>
    <header>
        <div class="container">
            <!-- logo -->
            <h1 class="logo fl">
                <a href="/">
                    <img src="../assets/images/logo.png" alt="music">
                    <span>music</span>
                </a>
            </h1>

            <!-- 导航 -->
            <nav class="fl">
                <ul>
                    <li><router-link to="/home" active-class="active">首页</router-link></li>
                    <li><a href="#">歌单</a></li>
                    <li><a href="#">歌手</a></li>
                    <li><router-link to="/toplist" active-class="active">排行榜</router-link></li>
                    <li v-if="$store.state.user.isLogin">
                        <router-link to="/mymusic" active-class="active">我的音乐</router-link>
                    </li>
                </ul>
            </nav>

            <!-- 搜索框 -->
            <div class="search fl">
                <input type="search" placeholder="搜索音乐" v-model="keyword" @keyup.enter="searchMusic">
            </div>

            <!-- 用户相关 -->
            <div class="user_about fl">
                <template v-if="$store.state.user.isLogin">
                    <img src="../assets/images/user-icon.jpg" alt="" class="user_icon">
                    <!-- 用户操作列表 -->
                    <div class="user_list">
                        <ul>
                            <li>
                                <a class="logout" @click="logout">
                                    <i class="icn icn_ex"></i>
                                    退出 
                                </a>
                            </li>
                        </ul>
                    </div>
                </template>
                
                <a id="btn_login" @click="login" v-else>登录</a>
            </div>
        </div>
    </header>

    <LoginDialog/>
</template>

<script setup>
    import LoginDialog from '@/components/LoginDialog'
    import { httpManager} from '@/api'
    import { ref } from 'vue'
    import { useRouter } from 'vue-router'
    import { useStore } from 'vuex'
    import { ElMessage } from 'element-plus'

    const router = useRouter()
    const store = useStore()
    const keyword = ref('')                  //搜索关键词
    
    //搜索音乐
    function searchMusic() {
        router.push({
            path: '/search',
            query: {
                keyword: keyword.value
            }
        })
    }

    //用户点击登录，显示登录弹窗
    function login() {
        store.commit('user/setLoginDialogVisible', true)
    }

    //用户退出登录
    async function logout() {
        //跳转至首页
        router.replace('/home')
        store.dispatch('user/logout')
    }
</script>

<style lang="less" scoped>
    /* 头部模块 */
    header {
        height: 70px;               
        line-height: 70px;          
        background-color: #2e353d;  
        user-select: none; 
        /* logo */
        .logo {
            margin-left: 35px;
            span {
                margin-left: 10px;  
                color: #fff;
            }   
        }
        /* 导航栏*/
        nav {
            margin-left: 40px;
            li {
                float: left;
                a {
                    display: inline-block;  
                    height: 100%;           
                    padding: 0 20px;        
                    color: #fff;
                    &.active, &:hover {
                        background-color: #008fd9;
                    } 
                }
            }  
        }
        /* 搜索框 */
        .search {
            position: relative;     
            height: 100%;          
            margin-left: 100px; 
            input {
                width: 158px;           
                height: 32px;
                border-radius: 16px;    
                padding-left: 30px;     
                padding-right: 10px;   
                vertical-align: middle;
            }
            /* 添加搜索图标 */
            &::after {
                position: absolute;     
                top: 28px;                       
                left: 10px;
                content: '';           
                width: 13px;           
                height: 14px;
                background: url(../assets/images/sprite.png) -167px 0;
            }
        }
        /* 用户相关 */ 
        .user_about {
            position: relative;     
            width: 40px;            
            height: 32px;
            margin-left: 30px; 
            #btn_login {
                position: absolute;    
                top: 0;                            
                left: 0;
                color: #fff;
                &:hover {
                    color: #008fd9;            
                    text-decoration: underline;
                }           
            }  
            .user_icon {
                width: 40px;               
                border-radius: 50%;         
            }
            .user_list {
                display: none;         
                position: absolute;    
                top: 64px;                     
                right: -60px;
                width: 158px;          
                height: 34px;                
                border: 1px solid #202020;                  
                box-shadow: 0 8px 24px 0 rgba(0,0,0,0.5);   
                border-radius: 4px;    
                z-index: 5; 
                /* 添加上箭头 */ 
                &::before {
                    position: absolute;    
                    content: '';             
                    top: -8px;              
                    left: 72px;
                    width: 14px;            
                    height: 8px;
                    background: url(../assets/images/sprite.png) -181px -44px;   
                } 
                li {
                    width: 100%;  
                }  
                a {
                    display: block;               
                    height: 34px;                 
                    width: 100%;
                    line-height: 34px;             
                    background-color: #2b2b2b;     
                    color: #ccc;                  
                    font-size: 14px; 
                    &:hover {
                        background-color: #383838;   
                        color: #fff;
                    }
                    .icn {
                        display: inline-block;          
                        width: 14px;                   
                        height: 14px;
                        margin: -3px 10px 0px 25px;     
                        background-image: url(../assets/images/sprite.png);  
                        vertical-align: middle;
                    }
                    .icn_ex {
                        background-position: -162px -246px; 
                    }
                }        
            }
            /* 鼠标悬浮在头像上时显示用户操作列表 */ 
            &:hover .user_list {
                display: block;        
            }
        } 
    }
</style>