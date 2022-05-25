<template>
    <Header/>
    
    <div class="register_wrap">
        <div class="title">
            <p>注册</p>
        </div>

        <el-form
            ref="registerFormRef"
            :model="registerForm"
            :rules="registerFormRules"
            label-width="120px"
            size="large"
        >
            <el-form-item prop="username" label="用户名：">
                <el-input v-model="registerForm.username" placeholder="请输入用户名"></el-input>
            </el-form-item>
            <el-form-item prop="password" label="密码：">
                <el-input v-model="registerForm.password" placeholder="请输入密码" show-password></el-input>
            </el-form-item>
             <el-form-item prop="repassword" label="确认密码：">
                <el-input v-model="registerForm.repassword" placeholder="请输入确认密码" show-password></el-input>
            </el-form-item>
             <el-form-item prop="gender" label="性别：">
                <el-radio v-model="registerForm.gender" :label="1" size="large">男</el-radio>
                <el-radio v-model="registerForm.gender" :label="0" size="large">女</el-radio>
            </el-form-item>
            <el-form-item prop="email" label="邮箱：">
                <el-input v-model="registerForm.email" placeholder="请输入邮箱"></el-input>
            </el-form-item>
            <el-form-item prop="tel" label="联系电话：">
                <el-input v-model="registerForm.tel" placeholder="请输入联系电话"></el-input>
            </el-form-item>
            <el-form-item prop="introduce" label="个人介绍：">
                <el-input v-model="registerForm.introduce" placeholder="请输入个人介绍" type="textarea" :rows="5"></el-input>
            </el-form-item>
            <el-form-item>
                <input type="button" value="立即注册" class="btn_register" @click="register">
            </el-form-item>
        </el-form>
    </div>
</template>

<script setup>
    import Header from '@/components/Header'
    import { reactive, ref } from 'vue'
    import { httpManager } from '@/api'
    import { ElMessage } from 'element-plus'
    import { useStore } from 'vuex'

    const store = useStore()
    const registerFormRef = ref(null)

    //注册表单数据
    const registerForm = reactive({
        username: '',           //用户名
        password: '',           //密码
        repassword: '',         //确认密码
        gender: 1,              //性别
        email: '',              //邮箱
        tel: '',                //联系电话
        introduce: ''           //个人介绍
    })

    //验证确认密码是否合法
    const checkRepassword = (rules, value, callback) => {
        if(registerForm.password !== value) {
            return callback(new Error('两次密码输入不一致'))
        }
        callback()
    }

    //验证邮箱规则
    const checkEmail = (rules, value, callback) => {
        const regEmail = /^[\w-]+@([\w-]+\.)+[a-zA-Z]{2,4}$/
        if(regEmail.test(value)) {
            return callback()       //验证通过
        }
        callback(new Error('请输入合法的邮箱'))
    }

    //验证联系电话规则
    const checkTel = (rules, value, callback) => {
        const regTel = /^\d{11}$/
        if(regTel.test(value)) {
            return callback()       //验证通过
        }
        callback(new Error('请输入合法的手机号'))
    }

    //表单校验规则
    const registerFormRules = reactive({
        //验证用户名是否合法
        username: [
            { required: true, message: '请输入用户名', trigger: 'blur' },
            { min: 3, max: 10, message: '长度为 3 到 10 个字符', trigger: 'blur' }
        ],
        //验证密码是否合法
        password: [
            { required: true, message: '请输入密码', trigger: 'blur' },
            { min: 6, max: 15, message: '长度为 6 到 15 个字符', trigger: 'blur' }
        ],
        //验证确认是否合法
        repassword: [
            { required: true, message: '请输入确认密码', trigger: 'blur' },
            { validator: checkRepassword, trigger: 'blur' }
        ],
        //验证邮箱是否合法
        email: [
            { required: true, message: '请输入邮箱', trigger: 'blur' },
            { validator: checkEmail, trigger: 'blur' }
        ],
        //验证联系电话是否合法
        tel: [
            { required: true, message: '请输入联系电话', trigger: 'blur' },
            { validator: checkTel, trigger: 'blur' }
        ]  
    })

    //用户注册
    function register() {
        registerFormRef.value.validate(async valid => {
            if(!valid) return

            const {data: res} = await httpManager.register(registerForm)

            //注册错误提示
            if(res.status != 200) {
                return ElMessage.error(res.msg)
            }

            ElMessage.success('注册成功，请登录')

            //重置表单
            registerFormRef.value.resetFields()

            store.commit('user/setLoginDialogVisible', true)
        })
    }
</script>

<style lang="less" scoped>
    .register_wrap {
        width: 650px;
        margin: 40px auto;
        padding: 32px 40px 40px;
        background-color: #fff;
        box-sizing: border-box;
        box-shadow: 0 0 20px 0 rgb(0 0 0 / 10%);
        .title {
            height: 50px;
            line-height: 50px;
            border-bottom: 1px solid #E9E9E9;
            margin-bottom: 25px;
            p {
                font-size: 17px;  
                color: #008fd9;
                height: 49px;
                width: 104px;
                text-align: center;
                margin-left: 30px;
                border-bottom: 2px solid #008fd9;
            }
        }
        .el-form {
            padding-right: 30px;
            .btn_register {
                right: 0;
                background: #008fd9;
                border-radius: 5px;
                height: 38px;
                width: 120px;
                color: #fff;
                font-size: 17px;
                cursor: pointer;
            }
        }
    }
</style>