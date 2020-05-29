// pages/menu/menu.js

const app = getApp()

Page({

  /**
   * 页面的初始数据
   */
  data: {
    grids: [{
      "name": "应用1"
    }, {
      "name": "应用2"
    }], // 九宫格内容
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    this.updateMenuData()
  },

  /**
   * 请求后台，更新menu数据
   */
  updateMenuData: function () {
    var that = this
    wx.request({
      url: app.globalData.serverUrl + app.globalData.apiVersion + '/service/menu',
      success: function (res) {
        var menuData = res.data.data
        that.setData({
          grids: menuData
        })
      }
    })
  },

  onNavigatorTap: function (e) {
    var index = e.currentTarget.dataset.index
    var item = this.data.grids[index]
    console.log(item)
    if (item.app.application == 'weather') {
      console.log('-------------')
      wx.navigateTo({
        url: '../weather/weather',
      })
    } else if (item.app.application == 'backup-image') {
      wx.navigateTo({
        url: '../backup/backup',
      })
    } else if (item.app.application == 'stock') {
      wx.navigateTo({
        url: '../stock/stock'
      })
    } else if (item.app.application == 'joke') {
      wx.navigateTo({
        url: '../service/service?type=joke'
      })
    } else if (item.app.application == 'constellation') {
      wx.navigateTo({
        url: '../service/service?type=constellation',
      })
    } else if (item.app.application == 'movies'){
      wx.navigateTo({
        url: '../service/service?type=movies',
      })
    }
  }
})