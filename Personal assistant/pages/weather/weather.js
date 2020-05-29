// pages/weather/weather.js

const app = getApp()

const popularCities = [{
  "province": "广东省",
  "city": "深圳市",
  "area": "南山区"
},
{
  "province": "广东省",
  "city": "广州市",
  "area": "天河区"
},
{
  "province": "北京市",
  "city": "北京市",
  "area": "朝阳区"
},
{
  "province": "上海市",
  "city": "上海市",
  "area": "徐汇区"
}
]

Page({

  /**
   * 页面的初始数据
   */
  data: {
    isAuthorized: false,
    weatherData: null
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    this.updateWeatherData()
  },

  updateWeatherData: function () {
    wx.showLoading({
      title: '加载中',
    })
    var that = this;
    wx.request({
      url: app.globalData.serverUrl + app.globalData.apiVersion + '/service/weather',
      method: 'POST',
      header: {
        'content-type': 'application/json' // 默认值
      },
      data: {
        cities: popularCities
      },
      success: function (res) { 
        console.log(res.data.data)
        that.setData({
          weatherData: res.data.data
        })
        wx.hideLoading()
      }
    })
  },


  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {
    this.updateWeatherData()
  }
})