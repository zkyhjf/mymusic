import { request } from './axios'

export const httpManager = {
    //登录
    login: loginForm => request.post('/user/login', loginForm),

    //注册
    register: registerForm => request.post('/user/register', registerForm),

    //获取用户收藏的歌曲
    getFavorites: () => request.get(`/user/favorites`),

    //添加用户收藏
    addFavorites: songid => request.post('/user/favorites/add', { songid }),

    //取消用户收藏
    deleteFavorites: songid => request.post('/user/favorites/delete', { songid }),

    //判断歌曲是否为用户收藏
    checkFavorites: songid => request.get('/user/favorites/check', { params: { songid } }),

    //获取排行榜数据
    getTopList: queryInfo => request.get('/song/toplist', { params: queryInfo }),

    //根据关键词搜索音乐
    searchMusic: keyword => request.get('/song/search', { params: { keyword } }),

    //根据歌曲id获取歌曲详情
    getSongDetail: songid => request.get('/song/detail', { params: { songid } })
}