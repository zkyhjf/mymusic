import axios from 'axios'
import { ElMessage } from 'element-plus'

//创建axios实例
export const request = axios.create({
    timeout: 5000,                      //设置超时时间
    baseURL: 'http://127.0.0.1:8000'    //配置请求根路径    
})

//请求拦截器
request.interceptors.request.use(config => {
    //在请求头中添加token验证的Authorization字段
    const token = localStorage.getItem('token')
    if(token) {
        config.headers.Authorization = 'jwt ' + token
    }
    return config
})