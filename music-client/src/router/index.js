import { createRouter, createWebHistory }  from 'vue-router'
import Home from '@/pages/Home'
import MyMusic from '@/pages/MyMusic'
import Search from '@/pages/Search'
import TopList from '@/pages/TopList'
import TopSongList from '@/pages/TopSongList'
import Player from '@/pages/Player'
import Register from '@/pages/Register'

export default createRouter({
    history: createWebHistory(),        //使用history模式
    routes: [
        {
            path: '/',
            redirect: '/home'   //重定向到首页
        },
        {
            path: '/home',
            component: Home
        },
        {
            path: '/mymusic',
            component: MyMusic,
            //路由独享守卫
            beforeEnter: (to, from, next) => {
                //token不存在跳转首页
                if(!localStorage.getItem('token')) {
                    location.href = location.origin + '/home'
                    return
                }
                next()
            },
        },
        {
            path: '/search',
            component: Search,
            props({ query }) {
                return { keyword: query.keyword }
            }
        },
        {
            path: '/toplist',
            component: TopList,
            redirect: '/toplist/1',     //重定向到飙升榜
            children: [
                {
                    path: ':category',
                    props: true,
                    component: TopSongList
                }
            ]
        },
        {
            path: '/player',
            component: Player,
            props({ query }) {
                return { songid: query.songid }
            }
        },
        {
            path: '/register',
            component: Register
        }
    ]
})