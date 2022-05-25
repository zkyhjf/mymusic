<template>
    <!-- 登录弹窗 -->
    <teleport to='body'>
        <div class="mask" v-if="$store.state.user.loginDialogVisible">
            <div class="login_window">
                <div class="head">
                    <span class="fl">登录</span>
                    <span class="close fr" title="关闭窗体" @click="closeDialog">×</span>
                </div>
                <div class="main">
                    <el-form
                        ref="loginFormRef"
                        :model="loginForm"
                        :rules="loginFormRules"
                        label-width="0"
                        size="large"
                    >
                        <el-form-item prop="username">
                            <el-input v-model="loginForm.username" placeholder="输入用户名"></el-input>
                        </el-form-item>
                        <el-form-item prop="password">
                            <el-input v-model="loginForm.password" placeholder="输入密码" show-password></el-input>
                        </el-form-item>
                        <input type="button" value="登录" class="submit" @click="login">
                        <div class="register_wrap">
                            <a class="register" @click="register">注册新账号</a>
                        </div>
                    </el-form>
                </div>
            </div>
        </div>
    </teleport>
</template>

<script setup>
    import { reactive, ref } from 'vue'
    import { httpManager } from '@/api'
    import { ElMessage } from 'element-plus'
    import { useStore } from 'vuex'
    import { useRouter } from 'vue-router'

    const store = useStore()
    const router = useRouter()

    const loginFormRef = ref(null)
    
    //登录表单数据
    const loginForm = reactive({
        username: '',
        password: ''
    })

    //表单校验规则
    const loginFormRules =  reactive({
        //验证用户名是否合法
        username: [
            { required: true, message: '请输入用户名', trigger: 'blur' },
            { min: 3, max: 10, message: '长度为 3 到 10 个字符', trigger: 'blur' }
        ],
        //验证密码是否合法
        password: [
            { required: true, message: '请输入密码', trigger: 'blur' },
            { min: 6, max: 15, message: '长度为 6 到 15 个字符', trigger: 'blur' }
        ]
    })

    //关闭对话框
    function closeDialog() {
        loginFormRef.value.resetFields()                //重置登录表单
        store.commit('user/setLoginDialogVisible', false)
    }

    //用户登录
    function login() {
        //对整个表单进行校验
        loginFormRef.value.validate(async valid => {
            if(!valid) return
            const { data: res } = 
                await httpManager.login(loginForm)
                    .catch(() => {
                        ElMessage.error('用户名或密码错误')
                    })

            //登录成功保存用户信息至vuex
            store.commit('user/setLoginUser', res.data)
            
            //设置用户已登录
            store.commit('user/setLoginState', true)

            //将token保存至localStorage中
            localStorage.setItem('token', res.data.token)

            //跳转至我的音乐界面
            router.push('/mymusic')

            ElMessage.success('登录成功')
            closeDialog()
        })
    }

    //用户点击注册
    function register() {
        closeDialog()
        router.push('/register')
    }
</script>

<style lang="less" scoped>
    /* 登录弹窗 */
    .mask {
        position: absolute;
        top: 0;
        bottom: 0;
        left: 0;
        right: 0;
    }

    .login_window {
        position: fixed;                 
        top: 50%;                           
        left: 50%;
        transform: translate(-50%, -50%);   
        z-index: 999;                      
        width: 530px;                      
        height: 372px;
        background-color: #fff;          
        border-radius: 4px;                
        box-shadow: 0 5px 16px rgba(0,0,0,0.8);  
        border: none;                       
        overflow: hidden;                  
        user-select: none; 
        .head {
            height: 45px;                  
            background-color: #2e353d;  
            line-height: 45px;            
            text-align: center;
            span:first-child {
                padding-left: 20px;           
                font-weight: bold;           
                font-size: 14px;             
                color: #fff;               
            }
            span:last-child {
                padding-right: 10px;          
                cursor: pointer;             
                font-size: 20px;             
                color: #999;
                &:hover {
                    color: #fff;
                }               
            }
        }
        .main {
            display: flex;                 
            justify-content: center;      
            padding-top: 55px; 
            input {
                width: 270px;                 
                height: 38px;
                margin: 10px 0;               
                border-radius: 5px;           
                box-sizing: border-box; 
            }
            .submit {
                background-color: #0091da;  
                color: #fff;                
                font-size: 18px;             
                cursor: pointer; 
            }
            .register_wrap {
                margin-top: 5px;              
                text-align: center;
                .register {
                    color: #333; 
                    &:hover {
                        color: #0091da;             
                        text-decoration: underline;
                    }
                }
            }
        }                 
    }
</style>