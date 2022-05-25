//用户模块
export default {
    namespaced: true,       //开启命名空间
    actions: {
        //退出登录
        logout(context) {
            localStorage.removeItem('token')
            context.commit('setLoginUser', {})
            context.commit('setLoginState', false)
        }
    },

    mutations: {
        //设置登录用户信息
        setLoginUser(state, loginUser) {
            state.loginUser = loginUser
        },
        
        //设置用户登录状态
        setLoginState(state, isLogin) {
            state.isLogin = isLogin
        },

        //设置弹窗显示状态
        setLoginDialogVisible(state, visible) {
            state.loginDialogVisible = visible
        }
    },

    state: {
        loginDialogVisible: false,   //登录弹窗显示状态
        loginUser: {},        //登录用户信息
        isLogin: false        //用户是否已登录
    }
}