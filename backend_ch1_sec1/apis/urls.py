
from django.urls import path

from apis.views import service
from .views import weather, menu, image

urlpatterns = [
     # 把请求路由到了helloworld函数
     # path('', weather.helloworld)
     # path('', weather.weather)

     # path('weather', weather.weather),
     path('weather', weather.WeatherView.as_view()),

     path('menu', menu.get_menu),
     # path('menu/user', menu.UserMenu.as_view()),
     # path('menu/list', menu.get_menu),

     # path('image', image.image),
     # path('imagetext',image.image_text)

     # 引入类视图路由
     path('image', image.ImageView.as_view()),
     path('image/list', image.ImageListView.as_view()),

     path('stock', service.stock),
     path('constellation', service.constellation),
     path('joke', service.joke),

     path('movies', service.movies)

]