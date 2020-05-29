//index.js
//获取应用实例
const app = getApp()
const cookieUtil = require('../../utils/cookie.js')
const imageUtil = require('../../utils/util.js')

Page({
  data: {
    isAuthorized: false,
    constellationData: null,
    stockData: null,
    weatherData: null,
    imageUrl: "../../resources/images/yyqx.jpg",
    imageUrl1: "../../resources/images/recommandations.jpg",
    imageUrl2: "../../resources/images/recommandations1.jpg",
    viewHeigh: "",
    viewWidth: ""
  },
  //事件处理函数
  bindViewTap: function () {
    wx.navigateTo({
      url: '../logs/logs'
    })
  },

//请求后台，刷新小程序的后台（发送4个请求：请求天气、股票、星座数据,电影推荐）
  updateData: function () {
    wx.showLoading({
      title: '加载中',
    })
    var that = this
    var cookie = cookieUtil.getCookieFromStorage()
    var header = {}
    header.Cookie = cookie
    wx.request({
      url: app.globalData.serverUrl + app.globalData.apiVersion + '/service/weather',
      header: header,
      success: function (res) {
        that.setData({
          weatherData: res.data.data
        })
        wx.hideLoading()
      }
    })
    wx.request({
      url: app.globalData.serverUrl + app.globalData.apiVersion + '/service/constellation',
      header: header,
      success: function (res) {
        that.setData({
          constellationData: res.data.data
        })
        wx.hideLoading()
      }
    })
    wx.request({
      url: app.globalData.serverUrl + app.globalData.apiVersion + '/service/stock',
      header: header,
      success: function (res) {
        that.setData({
          stockData: res.data.data
        })
        wx.hideLoading()
      }
    })
    wx.request({
      url: app.globalData.serverUrl + app.globalData.apiVersion + '/service/movies',
      header: header,
      success: function (res) {
        that.setData({
          moviesData: res.data.data
        })
        wx.hideLoading()
      }
    })
  },

//下拉刷新时使用
  onPullDownRefresh: function () {
    var that = this
    var cookie = cookieUtil.getCookieFromStorage()
    var header = {}
    header.Cookie = cookie
    wx.request({
      url: app.globalData.serverUrl + app.globalData.apiVersion + '/auth/status',
      header: header,
      success: function (res) {
        var data = res.data.data
        if (data.is_authorized == 1) {
          that.setData({
            isAuthorized: true
          })
          that.updateData()
        } else {
          that.setData({
            isAuthorized: false
          })
          wx.showToast({
            title: '请先授权登录',
          })
        }
      }
    })
  },

  onLoad: function () {
    if (app.globalData.userInfo) {
      this.setData({
        userInfo: app.globalData.userInfo,
        hasUserInfo: true
      })
    } else if (this.data.canIUse) {
      // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
      // 所以此处加入 callback 以防止这种情况
      app.userInfoReadyCallback = res => {
        this.setData({
          userInfo: res.userInfo,
          hasUserInfo: true
        })
      }
    } else {
      // 在没有 open-type=getUserInfo 版本的兼容处理
      wx.getUserInfo({
        success: res => {
          app.globalData.userInfo = res.userInfo
          this.setData({
            userInfo: res.userInfo,
            hasUserInfo: true
          })
        }
      })
    }
  },
  getUserInfo: function (e) {
    console.log(e)
    app.globalData.userInfo = e.detail.userInfo
    this.setData({
      userInfo: e.detail.userInfo,
      hasUserInfo: true
    })
  },

  imageLoad: function (e) {
    var viewSize = imageUtil.getViewWHInfo(e);
    //console.log(viewSize.heigh);
    this.setData({
      viewHeigh: viewSize.height,
      viewWidth: viewSize.width
      })
  }

})