// pages/backup/backup.js
const app = getApp()
const imageUrl = app.globalData.serverUrl + app.globalData.apiVersion + '/service/image'

Page({
  data: {
    // 需要上传的图片
    needUploadFiles: [],
    // backupedFiles每个元素四个字段 name, md5, path, isDownloaded
    // 已下载的备份图片
    downloadedBackupedFiles: [],
  },

  // 选择图片上传
  chooseImage: function (e) {
    var that = this;
    wx.chooseImage({
      sizeType: ['original', 'compressed'], // 可以指定是原图还是压缩图，默认二者都有
      sourceType: ['album', 'camera'], // 可以指定来源是相册还是相机，默认二者都有
      success: function (res) {
        // 返回选定照片的本地文件路径列表，tempFilePath可以作为img标签的src属性显示图片
        that.setData({
          needUploadFiles: that.data.needUploadFiles.concat(res.tempFilePaths)
        });
      }
    })
  },

  onLoad: function(){
    this.downloadAllFromRemote()
  },

  //下载所有的已备份图片
  downloadAllFromRemote: function(){
    var that = this
    wx.request({
      url: app.globalData.serverUrl + app.globalData.apiVersion + '/service/image/list',
      method:'GET',
      success: function(res){
        var imageList = res.data.data
        for(var i = 0; i < imageList.length; i++){
          var imageItem = imageList[i]
          that.downloadFile(imageItem)
        }
      }
    })
  },

  //长按取消上传


  //长按确认函数
  longTapConfirm: function(e){
    var that = this
    var confirmList = ["删除备份"]
    wx.showActionSheet({
      itemList: confirmList,
      success: function(res){
        if(res.cancel){
          return
        }
        var imageIndex = e.currentTarget.dataset.index
        var imageItem = that.data.downloadedBackupedFiles[imageIndex]
        //将其进行移除
        var newList = that.data.downloadedBackupedFiles
        newList.splice(imageIndex, 1)
        // 完成本地图片的删除
        that.setData({
          downloadedBackupedFiles: newList 
        })
        //完成远端图片的删除
        that.deleteBackup(imageItem)
      }
    })
  },

  // 上传图片文件
  uploadFiles: function () {
    var that = this
    for (var i = 0; i < this.data.needUploadFiles.length; i++) {
      var filePath = this.data.needUploadFiles[i]
      wx.uploadFile({
        url: app.globalData.serverUrl + app.globalData.apiVersion + '/service/image',
        filePath: filePath,
        name: 'test',
        success: function (res) {
          var res = JSON.parse(res.data)
          var md5 = res.data[0].md5
          var name = res.data[0].name
          var newImageItem = {
            "md5": md5,
            "name": name
          }
          that.downloadFile(newImageItem)
        }
      })
    }
    wx.showToast({
      title: '上传成功',
    })
    //将待上传的图片数组清空
    this.setData({
      needUploadFiles: []
    })
  },

  // 下载图片
  downloadFile: function (imgItem) {
    var that = this
    // 变动1： 下载URL改为从参数获取
    var downLoadUrl = imageUrl + '?md5=' + imgItem.md5
    wx.downloadFile({
      url: downLoadUrl,
      success: function (res) {
        var filePath = res.tempFilePath
        console.log(filePath)
        var newDownloadedBackupedFiles = that.data.downloadedBackupedFiles
        imgItem.path = filePath
        // 变动2： 操作图片数组
        newDownloadedBackupedFiles.unshift(imgItem)
        that.setData({
          downloadedBackupedFiles: newDownloadedBackupedFiles
        })
      }
    })
  },

  // 删除图片
  deleteBackup: function (imgItem) {
    wx.request({
      url: app.globalData.serverUrl + app.globalData.apiVersion + '/service/image' + '?md5=' + '1ad78e3e075fd648882ba5299728369b',
      method: 'DELETE',
      success: function (res) {
        console.log(res.data)
        wx.showToast({
          title: '删除成功',
        })
      }
    })
  }
});