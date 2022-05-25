module.exports = {
    devServer: {
        port: 8888, // 启动端口
        open: true, // 启动后自动打开网页
    },
    assetsDir: 'static',         //配置静态文件存放目录
    productionSourceMap: false,  //去除源码映射
    lintOnSave: false,           //关闭语法检查
}