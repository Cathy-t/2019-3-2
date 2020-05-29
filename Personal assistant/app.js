//app.js
App({
  
//第一部分：小程序的生命周期、回调函数

  onLaunch: function () {
    // 展示本地存储能力
    var logs = wx.getStorageSync('logs') || []
    logs.unshift(Date.now())
    wx.setStorageSync('logs', logs)

    // 登录
    wx.login({
      success: res => {
        // 发送 res.code 到后台换取 openId, sessionKey, unionId
      }
    })
    // 获取用户信息
    wx.getSetting({
      success: res => {
        if (res.authSetting['scope.userInfo']) {
          // 已经授权，可以直接调用 getUserInfo 获取头像昵称，不会弹框
          wx.getUserInfo({
            success: res => {
              // 可以将 res 发送给后台解码出 unionId
              this.globalData.userInfo = res.userInfo

              // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
              // 所以此处加入 callback 以防止这种情况
              if (this.userInfoReadyCallback) {
                this.userInfoReadyCallback(res)
              }
            }
          })
        }
      }
    })
  },

//用于返回当前的用户状态
  getAuthStatus: function () {
    return this.globalData.auth.isAuthorized
  },

//设置用户状态
  setAuthStatus: function (status) {
    console.log('set auth status: ' + status)
    if (status == true || status == false) {
      this.globalData.auth.isAuthorized = status
    } else {
      console.log('invalid status.')
    }

  },

  onShow: function(){},
  onHide: function(){},

//第二部分：小程序的全局变量

  globalData: {
    userInfo: null,
    appId:'wx0541e496228a2d98',
    serverUrl: 'http://127.0.0.1:8000',
    apiVersion: '/api/v1.0',
    auth:{
      isAuthorized:false
    }
  }
})