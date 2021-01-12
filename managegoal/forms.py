from django import forms
from .models import Goal

# ゴール登録Form
# 課題: ChoiseField -> choisesの書き方
class GoalRegisterForm(forms.Form):
    prefecture_id = forms.ChoiceField(
        choices = (
                (1, '北海道'),
                (2, '青森県'),
                (3, '岩手県'),
                (4, '宮城県'),
                (5, '秋田県'),
                (6, '山形県'),
                (7, '福島県'),
                (8, '茨城県'),
                (9, '栃木県'),
                (10, '群馬県'),
                (11, '埼玉県'),
                (12, '千葉県'),
                (13, '東京都'),
                (14, '神奈川県'),
                (15, '新潟県'),
                (16, '富山県'),
                (17, '石川県'),
                (18, '福井県'),
                (19, '山梨県'),
                (20, '長野県'),
                (21, '岐阜県'),
                (22, '静岡県'),
                (23, '愛知県'),
                (24, '三重県'),
                (25, '滋賀県'),
                (26, '京都府'),
                (27, '大阪府'),
                (28, '兵庫県'),
                (29, '奈良県'),
                (30, '和歌山県'),
                (31, '鳥取県'),
                (32, '島根県'),
                (33, '岡山県'),
                (34, '広島県'),
                (35, '山口県'),
                (36, '徳島県'),
                (37, '香川県'),
                (38, '愛媛県'),
                (39, '高知県'),
                (40, '福岡県'),
                (41, '佐賀県'),
                (42, '長崎県'),
                (43, '熊本県'),
                (44, '大分県'),
                (45, '宮崎県'),
                (46, '鹿児島県'),
                (47, '沖縄県')
        ),
        label='都道府県',
        required = True,
        widget = forms.widgets.Select
    )
    address = forms.CharField(label='住所(都道府県以降)', min_length=5, max_length=100)
    name = forms.CharField(label='ゴール名', min_length=3, max_length=10)
    image = forms.ImageField(label='画像', required=False)
    starttime = forms.TimeField(label='利用可能開始時間', required=False)
    endtime = forms.TimeField(label='利用可能終了時間', required=False)
    url = forms.URLField(label='URL', required=False)
    #explanation = forms.TextField(required=False, max_length=1000)
    #otherinfo = forms.TextField(required=False, max_length=1000)
    explanation = forms.CharField(label='ゴール説明', required=False, widget=forms.Textarea, max_length=1000)
    otherinfo = forms.CharField(label='補足事項', required=False, widget=forms.Textarea, max_length=1000)

# ゴール情報更新画面でのフォームオブジェクト
class GoalUpdateApplicationForm(forms.Form):
    prefecture_id = forms.ChoiceField(
        choices = (
                (1, '北海道'),
                (2, '青森県'),
                (3, '岩手県'),
                (4, '宮城県'),
                (5, '秋田県'),
                (6, '山形県'),
                (7, '福島県'),
                (8, '茨城県'),
                (9, '栃木県'),
                (10, '群馬県'),
                (11, '埼玉県'),
                (12, '千葉県'),
                (13, '東京都'),
                (14, '神奈川県'),
                (15, '新潟県'),
                (16, '富山県'),
                (17, '石川県'),
                (18, '福井県'),
                (19, '山梨県'),
                (20, '長野県'),
                (21, '岐阜県'),
                (22, '静岡県'),
                (23, '愛知県'),
                (24, '三重県'),
                (25, '滋賀県'),
                (26, '京都府'),
                (27, '大阪府'),
                (28, '兵庫県'),
                (29, '奈良県'),
                (30, '和歌山県'),
                (31, '鳥取県'),
                (32, '島根県'),
                (33, '岡山県'),
                (34, '広島県'),
                (35, '山口県'),
                (36, '徳島県'),
                (37, '香川県'),
                (38, '愛媛県'),
                (39, '高知県'),
                (40, '福岡県'),
                (41, '佐賀県'),
                (42, '長崎県'),
                (43, '熊本県'),
                (44, '大分県'),
                (45, '宮崎県'),
                (46, '鹿児島県'),
                (47, '沖縄県')
        ),
        required = False,
        widget = forms.widgets.Select,
        label='都道府県'
    )
    address = forms.CharField(label='住所(都道府県以降)', min_length=5, max_length=100, required=False)
    name = forms.CharField(label='ゴール名', min_length=3, max_length=10, required=False)
    image = forms.ImageField(label='画像', required=False)
    starttime = forms.TimeField(label='利用可能開始時間', required=False)
    endtime = forms.TimeField(label='利用可能終了時間', required=False)
    url = forms.URLField(label='URL', required=False)
    explanation = forms.CharField(label='説明', max_length=1000, required=False, widget=forms.Textarea)
    otherinfo = forms.CharField(label='補足', max_length=1000, required=False, widget=forms.Textarea)


class ImpressionForm(forms.Form):
    impression = forms.CharField(label='感想', max_length=50, widget=forms.Textarea)



