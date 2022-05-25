//歌曲模块
export default {
    namespaced: true,       //开启命名空间
    actions: {
        //解析歌词
        parseLyric(context) {
            const lrc = context.state.song.lrc
            if(lrc === undefined ) return context.commit('setLyricArr', [])

            //按行分隔歌词
            const lyricArr = lrc.split("\n")

            //新建一个数组存放结果
            let result = []

            for(let i = 0; i < lyricArr.length; i++) {
                //正则匹配播放时间
                const playTimeArr = lyricArr[i].match(/\[\d{2}:\d{2}((\.|\\:)\d{2,3})\]/g)

                //获取每行的歌词
                let lineLyric = ""
                if (lyricArr[i].split(playTimeArr).length > 0) {
                    lineLyric = lyricArr[i].split(playTimeArr)
                }

                if(playTimeArr != null) {
                    for (let j = 0; j < playTimeArr.length; j++) {
                        //分隔时间字符串
                        const time = playTimeArr[j].substring(1, playTimeArr[j].indexOf("]")).split(":")

                        //数组填充
                        result.push({
                            time: (parseInt(time[0]) * 60 + parseFloat(time[1]) - 0.2).toFixed(4),   //播放时间
                            content: String(lineLyric).substr(1)    //歌词
                        })
                    }
                }
            }
            context.commit('setLyricArr', result)
        },

        //当快进或者倒退的时候，找到最近的歌词所在行
        getLineNo(context) {
            const lineNo = context.state.lineNo
            const lyricArr = context.state.lyricArr
            const currentTime = context.state.song.currentTime
            if(lineNo >= 0 && lineNo < lyricArr.length ) {
                if (currentTime >= parseFloat(lyricArr[lineNo].time)) {
                    // 快进
                    for (let i = lyricArr.length - 1; i >= lineNo; i--) {
                        if (currentTime >= parseFloat(lyricArr[i].time)) {
                            context.commit('setLineNo', i)
                            return
                        }
                    }
                } else {
                    // 后退
                    for (let i = 0; i <= lineNo; i++) {
                        if (currentTime <= parseFloat(lyricArr[i].time)) {
                            context.commit('setLineNo', i - 1)
                            return
                        }
                    }
                }
            }
        }
    },

    mutations: {
        //设置当前播放歌曲
        setSong(state, song) {
            state.song = song
        },

        //设置歌曲id
        setSongid(state, songid) {
            state.song.id = songid
        },

        //设置歌曲总时长
        setDuration(state, duration) {
            state.song.duration = duration
        },

        //设置歌曲当前播放时长
        setCurrentTime(state, currentTime) {
            state.song.currentTime = currentTime
        },

        //设置歌词数组
        setLyricArr(state, lyricArr) {
            state.lyricArr = lyricArr
        },

        //设置歌曲当前播放行
        setLineNo(state, lineNo) {
            state.lineNo = lineNo
        },

        //设置歌曲列表滚动条位置
        setScrollTop(state, scrollTop) {
            state.scrollTop = scrollTop
        }
    },

    state: {
        song: {},            //当前播放歌曲
        lyricArr: [],        //歌词数组
        lineNo: 0,           //歌曲当前播放行
        scrollTop: 0         //歌曲列表滚动条位置
    }
}