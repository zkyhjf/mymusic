import { createStore } from 'vuex'
import song from './modules/song'
import user from './modules/user'

//创建并导出store
export default createStore({
    modules: {
        song,
        user
    }
})