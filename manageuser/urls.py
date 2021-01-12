from django.urls import path
from .views import signupfunc,loginfunc,logoutfunc,updatefunc

urlpatterns = [
    # ユーザー登録
    path('signup/',signupfunc,name='signup'),
    # ログイン画面
    path('login/',loginfunc,name='login'),
    # ログアウト
    path('logout/',logoutfunc,name='logout'),
    # ユーザー更新 
    path('update/',updatefunc,name='userupdate'),
]
