from django.urls import path
from .views import registergoalfunc, impressionfunc, impressiongoodfunc, changegoodfunc,changeapplicationfunc,deleteapplicationfunc
from .views import detailgoalscreenfunc, showpositionfunc, selectgoalscreenfunc,showchangeapplicationhistoryfunc
from .views import nextfunc, reversefunc, goalfavoritefunc

urlpatterns = [
    # ゴール新規登録
    path('register/', registergoalfunc, name='register'),
    # 感想投稿
    path('impression/', impressionfunc, name='impression'),
    # 感想にいいね
    path('impressiongood/<int:pk>', impressiongoodfunc, name='impressiongood'),
    # 変更申請にいいね 
    path('changegood/<int:pk>', changegoodfunc, name='changegood'),
    # ゴール詳細画面表示 (リストからゴール選択)  
    path('detailgoalscreen/<int:pk>', detailgoalscreenfunc, name='detailgoalscreen'),
    # 地図にゴールの位置表示
    path('showposition/<int:pk>', showpositionfunc, name='showposition'),
    # ゴール選択画面表示 (都道府県検索)
    path('selectgoalscreen/<int:pk>', selectgoalscreenfunc, name='selectgoalscreen'),
    # 変更申請送信
    path('changeapplication/' ,changeapplicationfunc, name='changeapplication'),
    # 削除申請送信
    path('deleteapplication/' ,deleteapplicationfunc, name='deleteapplication'),
    # ゴール詳細画面に変更申請一覧表示
    path('showchangeapplicationhistory/' ,showchangeapplicationhistoryfunc, name='showchangeapplicationhistory'),
    # リストの次へ
    path('next/<str:which>', nextfunc, name='next'),
    # リストの前へ
    path('reverse/<str:which>', reversefunc, name='reverse'),
    # ゴールお気に入り処理
    path('goalfavorite', goalfavoritefunc, name='goalfavorite'),
]
