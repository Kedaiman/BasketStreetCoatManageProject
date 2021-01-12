from django.db import models
#from manageuser.models import User
from django.contrib.auth.models import User

# 県モデル
class Prefecture(models.Model):
    # 県名
    name = models.CharField(max_length=20)
    # 緯度
    lat = models.FloatField(null=True)
    # 経度
    lon = models.FloatField(null=True)


# ゴール情報
class Goal(models.Model):
    # 県名id (外部キー)
    prefecture_id = models.ForeignKey(Prefecture, on_delete=models.CASCADE)
    # 住所(県名以下)
    address = models.CharField(max_length=100)
    # ゴールの名前
    name = models.CharField(max_length=10)
    # ゴールの画像
    image = models.ImageField(upload_to='static/', null=True, blank=True)
    # 利用可能時間
    starttime = models.TimeField(null=True, blank=True)
    # 利用終了時間
    endtime = models.TimeField(null=True, blank=True)
    # URL -> ホームページへのURLなど
    url = models.URLField(null=True, blank=True)
    # 説明
    explanation = models.TextField(max_length=1000, null=True, blank=True)
    # 備考
    otherinfo = models.TextField(max_length=1000, null=True, blank=True)
    # ユーザーid (外部キー)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goal_user_id')
    # 緯度
    lat = models.FloatField(null=True)
    # 経度
    lon = models.FloatField(null=True)
    # お気に入り数
    favorite = models.IntegerField(default=0)
    # お気に入りをしたユーザー群
    favo_users = models.ManyToManyField(User, related_name='favo_users')


# 感想情報
class Impression(models.Model):
    # ゴールid (外部キー)
    goal_id = models.ForeignKey(Goal, on_delete=models.CASCADE)
    # ユーザーid (外部キー) 
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_id')
    # 感想
    impression = models.TextField(max_length=1000)
    # いいね
    good = models.IntegerField(default=0)
    # いいねを押したユーザー群
    good_users = models.ManyToManyField(User, related_name='good_users')
    # 変更申請日付
    date = models.DateTimeField(blank=True, null=True)


# 変更申請
class Changeapplication(models.Model):
    # ゴールの主キー
    goal_id = models.ForeignKey(Goal, on_delete=models.CASCADE)
    # 変更申請をしたユーザー
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_id_changeapp', null=True )
    # 変更した変数
    changevariable = models.CharField(max_length=30)
    # changevariableで指定した変数の前の状態
    before = models.TextField(max_length=1000)
    # changevariableで指定した変数の後の状態
    after = models.TextField(max_length=1000)
    # 前の画像
    before_image = models.ImageField(upload_to='static/', null=True, blank=True)
    # 後の画像
    after_image = models.ImageField(upload_to='static/', null=True, blank=True)
    # 変更に対してのいいね
    good = models.IntegerField(default=0)
    # 申請反映までの残りのいいね
    remaining = models.IntegerField(default=0)
    # いいねを押したユーザー群
    good_users = models.ManyToManyField(User, related_name='good_users_changeapp')
    # 変更申請日付
    date = models.DateTimeField()


class Changedhistory(models.Model):
    # ゴールid (外部キー)
    goal_id = models.ForeignKey(Goal, on_delete=models.CASCADE)
    # 変更したユーザーid (外部キー)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    # 変更した変数
    changevariable = models.TextField(max_length=1000)
    # changevariableで指定した変数の前の状態
    before = models.TextField(max_length=1000)
    # changevariableで指定した変数の後の状態
    after = models.TextField(max_length=1000)
    # 変更した日時
    date = models.DateTimeField(blank=True, null=True)

