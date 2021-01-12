from django.shortcuts import render
from .forms import GoalRegisterForm, ImpressionForm, GoalUpdateApplicationForm
from .models import Goal, User, Prefecture, Impression, Changedhistory, Changeapplication
from django.shortcuts import redirect
from django.utils.timezone import localtime
from django.utils import timezone
import requests
from bs4 import BeautifulSoup
import time
from tqdm import tqdm
from .views_sub import subFunc

## === 関数: 新規ストリートコート登録処理 === ##
def registergoalfunc(request):
    # request = POST
    if request.method == 'POST':
        # エラー内容を格納していくリスト
        errorList = []

        # formオブジェクトにRequestの内容を与える
        form = GoalRegisterForm(request.POST, request.FILES)

        # formオブジェクトが有効であれば
        if form.is_valid():
            # goalformオブジェクトから入力内容を取得
            input_prefecture_id = form.cleaned_data['prefecture_id']
            input_address = form.cleaned_data['address']
            input_name = form.cleaned_data['name']
            input_image = form.cleaned_data['image']
            input_starttime = form.cleaned_data['starttime']
            input_endtime = form.cleaned_data['endtime']
            input_url = form.cleaned_data['url']
            input_explanation = form.cleaned_data['explanation']
            input_otherinfo = form.cleaned_data['otherinfo']
            
            # addressが実在しているかのチェック
            prefecture = Prefecture.objects.get(pk=input_prefecture_id)
            try:
                latlon = subFunc.get_lat_lon_from_address(prefecture.name + input_address)
            except:
                errorList.append('この住所は存在していません')        

            # errorListが空でない場合
            if len(errorList) >= 1:
                # エラー時の初期値設定
                initial_dict = {
                        'prefecture_id': input_prefecture_id ,
                        'address' : input_address ,
                        'name' : input_name ,
                        'image' : input_image ,
                        'starttime' : input_starttime ,
                        'endtime' : input_endtime ,
                        'url' : input_url ,
                        'explanation' : input_explanation ,
                        'otherinfo' : input_otherinfo ,
                } 
                form = GoalRegisterForm(initial=initial_dict)
                return render(request, 'goalregister.html', {'errorList':errorList, 'form':form,})
            else:
                # ゴール情報オブジェクトに情報を設定
                goal = Goal()
                prefecture = Prefecture.objects.get(pk=input_prefecture_id)
                goal.prefecture_id = prefecture
                goal.address = input_address
                goal.name = input_name
                goal.image = input_image
                goal.starttime = input_starttime
                goal.endtime = input_endtime
                goal.url = input_url
                goal.explanation = input_explanation
                goal.otherinfo = input_otherinfo
                goal.lat = latlon['lat']
                goal.lon = latlon['lon']

                # 登録したユーザー情報をゴールオブジェクトに追加
                if 'user' in request.session:
                    user = request.session['user']
                    goal.user_id = user
                    goal.save()
                    return render(request, 'index_af.html', {'message':'ゴール情報の登録が完了しました'})
                # セッションにuserがいない場合
                else:
                    return render(request, 'sessiontimeout.html')

        # 入力内容に不正がある場合
        else:
             form = GoalRegisterForm()
             return render(request, 'goalregister.html', {'form':form, 'error':'入力に不正項目がありました',}) 
         
    # requestがGETの場合: 新規ストリートコート登録画面に遷移
    else:
        if 'user' in request.session:
            # 空のフォームオブジェクトを生成
            form = GoalRegisterForm()
            return render(request, 'goalregister.html', {'form':form}) 
        else:
            return render(request, 'sessiontimeout.html') 

#===================================================== 感想投稿系処理 ===================================================#

##=== 関数：感想投稿処理 ===##
def impressionfunc(request):

    #requestがPOST
    if request.method == 'POST':
        # formオブジェクト取得 
        form = ImpressionForm(request.POST, request.FILES)

        if form.is_valid():
            input_impression = form.cleaned_data['impression']
      
            # ゴール情報オブジェクト、ユーザー情報オブジェクトがセッションに存在するかチェック
            if 'goal' in request.session and 'user' in request.session:

                # 感想オブジェクトに情報を設定しDBに保存
                impression = Impression()
                user = request.session['user']
                goal = request.session['goal']
                impression.user_id = user
                impression.goal_id = goal 
                impression.impression = input_impression
                impression.date = localtime(timezone.now())
                impression.save()
                
                #ゴールに対応する感想一覧取得 
                impression_list = Impression.objects.filter(goal_id=goal).all()
                request.session['impression_list'] = impression_list.reverse()

                page_data = subFunc.getpage(request)
                if page_data is None:
                    return render(request, 'sessiontimeout.html')

                params = {
                    'param':0 ,
                    'param2':0 ,
                    'his_page': page_data['his_page'],
                    'his_page_max': page_data['his_page_max'],
                    'imp_page': page_data['imp_page'],
                    'imp_page_max': page_data['imp_page_max'],
                 }
                return render(request, 'detailgoalscreen.html', params)

            # セッションにgoal,userがいない場合
            else: 
                return render(request, 'sessiontimeout.html')

        # form オブジェクトに有効でない
        else:
            form = ImpressionForm()

            page_data = subFunc.getpage(requst)
            if page_data is None:
                return render(request, 'sessiontimeout.html')

            params = {
                'param':1 ,
                'param2':0 ,
                'his_page': page_data['his_page'],
                'his_page_max': page_data['his_page_max'],
                'form': form ,
             }
            return render(request, 'detailgoalscreen.html', params, {'message':'入力内容に不正項目があります'})

    # request = GET :ゴール詳細画面に感想フォームを出す
    else:
        form = ImpressionForm()

        page_data = subFunc.getpage(request)
        if page_data is None:
            return render(request, 'sessiontimeout.html')

        params = {
            'param':1 ,
            'param2':0 ,
            'his_page': page_data['his_page'],
            'his_page_max': page_data['his_page_max'],
            'form': form ,
         }
        return render(request, 'detailgoalscreen.html', params)


##=== 関数：感想へのいいね処理 ===##
def impressiongoodfunc(request, pk):
    impression = Impression.objects.get(pk=pk)

    # セッションのユーザー情報、ゴール情報を取得
    if 'user' in request.session and 'goal' in request.session:
        session_user = request.session['user']
        session_goal = request.session['goal']
    else:
        return render(request, 'sessiontimeout.html')

    #  過去に感想にいいねを押したユーザー一覧を取得
    good_users = impression.good_users.all()

    # 過去にいいねを押したユーザー一覧に含まれていない場合
    if session_user not in good_users:
        impression.good = impression.good + 1
        # 過去にいいねを押したユーザー一覧に追加
        impression.good_users.add(session_user)
        impression.save()

    page_data = subFunc.getpage(request)
    if page_data is None:
        return render(request, 'sessiontimeout.html')

    params = {
        'param':0 ,
        'param2':0 ,
        'his_page': page_data['his_page'],
        'his_page_max': page_data['his_page_max'],
        'imp_page': page_data['imp_page'],
        'imp_page_max': page_data['imp_page_max'],
    }
    return render(request, 'detailgoalscreen.html', params)


#===================================================== お気に入り処理 ===================================================#

##=== 関数：ゴールのお気に入り処理 ===##
def goalfavoritefunc(request):

    # セッションのユーザー情報、ゴール情報を取得
    if 'user' in request.session and 'goal' in request.session:
        session_user = request.session['user']
        session_goal = request.session['goal']
    else:
        return render(request, 'sessiontimeout.html')

    #  過去にお気に入りを押したユーザー一覧を取得
    favo_users = session_goal.favo_users.all()

    # 過去にお気に入りを押したユーザー一覧に含まれていない場合
    if session_user not in favo_users:
        session_goal.favorite = session_goal.favorite + 1
        # 過去にお気に入りを押したユーザー一覧に追加
        session_goal.favo_users.add(session_user)
        session_goal.save()
        # セッションのゴール情報を更新
        goal = Goal.objects.get(pk=session_goal.pk)
        request.session['goal'] = goal

    page_data = subFunc.getpage(request)
    if page_data is None:
        return render(request, 'sessiontimeout.html')

    params = {
        'param':0 ,
        'param2':0 ,
        'his_page': page_data['his_page'],
        'his_page_max': page_data['his_page_max'],
        'imp_page': page_data['imp_page'],
        'imp_page_max': page_data['imp_page_max'],
    }
    return render(request, 'detailgoalscreen.html', params)


#===================================================== 変更申請系処理 ===================================================#

##=== 関数： 変更申請投稿処理 ===##
def changeapplicationfunc(request):

    #requestがPOST
    if request.method == 'POST':

        # セッションからゴール情報取得
        if 'goal' in request.session and 'user' in request.session:
            session_goal = request.session['goal']
            session_user = request.session['user']
        else:
            return render(request, 'sessiontimeout.html')
        
        # 変更申請内容を取得
        form = GoalUpdateApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            
            input_prefecture_id = form.cleaned_data['prefecture_id']
            input_address = form.cleaned_data['address']
            input_name = form.cleaned_data['name']
            input_image = form.cleaned_data['image']
            input_starttime = form.cleaned_data['starttime']
            input_endtime = form.cleaned_data['endtime']
            input_url = form.cleaned_data['url']
            input_explanation = form.cleaned_data['explanation']
            input_otherinfo = form.cleaned_data['otherinfo']

            errorList = []

            # addressが実在しているか 
            prefecture = Prefecture.objects.get(pk=input_prefecture_id)
            try:
                # 緯度経度取得試み
                latlon = subFunc.get_lat_lon_from_address(prefecture.name + input_address)
            except:
                errorList.append('この住所は存在していません')        

            # errorListが空でない場合(ポリシー違反発生)
            if len(errorList) >= 1:
                initial_dict = {
                        'prefecture_id': input_prefecture_id ,
                        'address' : input_address ,
                        'name' : input_name ,
                        'image' : input_image ,
                        'starttime' : input_starttime ,
                        'endtime' : input_endtime ,
                        'url' : input_url ,
                        'explanation' : input_explanation ,
                        'otherinfo' : input_otherinfo ,
                }
                form = GoalUpdateApplicationForm(initial=initial_dict)    
                
                page_data = subFunc.getpage(request)
                if page_data is None:
                    return render(request, 'sessiontimeout.html')

                params = {
                       'param':0 ,
                       'param2':1 ,
                       'imp_page': page_data['imp_page'],
                       'imp_page_max': page_data['imp_page_max'],
                       'errorList':errorList,
                       'form':form,
                }
                return render(request, 'detailgoalscreen.html', params)

            # 内容に変更があるかチェック
            changeParamList = [] 
            image_param = {
                    'count' : -1,
                    'before':False,
                    'after' :False,
            }

            # prefecture_id
            if int(input_prefecture_id) != session_goal.prefecture_id.pk:
                prefecture = Prefecture.objects.get(pk=input_prefecture_id)
                changeParamList.append(['都道府県', session_goal.prefecture_id.name, prefecture.name]) 
               
            # address
            if len(input_address) != 0:
                if input_address != session_goal.address:
                    changeParamList.append(['住所', session_goal.address, input_address]) 

            # name 
            if len(input_name) != 0:
                if input_name != session_goal.name:
                    changeParamList.append(['ゴール名', session_goal.name, input_name])

            # image
            if input_image is not None:
                if not session_goal.image:
                    changeParamList.append(['画像', None, input_image])
                    image_param['count'] = len(changeParamList) - 1
                    image_param['before'] = False 
                    image_param['after'] = True
                else:
                    changeParamList.append(['画像', session_goal.image.url, input_image])
                    image_param['count'] = len(changeParamList) - 1
                    image_param['before'] = True
                    image_param['after'] = True

            # starttime 
            if input_starttime is not None:
                if input_starttime != session_goal.starttime:
                    changeParamList.append(['利用可能開始時間', session_goal.starttime, input_starttime])

            # endtime 
            if input_endtime is not None:
                if input_endtime != session_goal.endtime:
                    changeParamList.append(['利用可能終了時間', session_goal.endtime, input_endtime])

            # url 
            if len(input_url) != 0:
                if input_url != session_goal.url:
                    changeParamList.append(['URL', session_goal.url, input_url])

            # explanation 
            if len(input_explanation) != 0:
                if input_explanation != session_goal.explanation:
                    changeParamList.append(['説明', session_goal.explanation, input_explanation])

            # otherinfo 
            if len(input_otherinfo) != 0:
                if input_otherinfo != session_goal.otherinfo:
                    changeParamList.append(['補足事項', session_goal.otherinfo, input_otherinfo])

            # 変更が存在しない
            if len(changeParamList) == 0:
                initial_dict = {
                        'prefecture_id': input_prefecture_id ,
                        'address' : input_address ,
                        'name' : input_name ,
                        'image' : input_image ,
                        'starttime' : input_starttime ,
                        'endtime' : input_endtime ,
                        'url' : input_url ,
                        'explanation' : input_explanation ,
                        'otherinfo' : input_otherinfo ,
                }
                form = GoalUpdateApplicationForm(initial=initial_dict)    

                page_data = subFunc.getpage(request)
                if page_data is None:
                    return render(request, 'sessiontimeout.html')

                params = {
                       'param':0 ,
                       'param2':1 ,
                       'imp_page': page_data['imp_page'],
                       'imp_page_max': page_data['imp_page_max'],
                       'error': '変更が存在しません',
                       'form' : form ,
                }
                return render(request, 'detailgoalscreen.html', params)

            # 変更が存在する
            else:
                # 変更申請に変更申請内容を保存
                count = 0
                while count < len(changeParamList): 
                    changeapp = Changeapplication()
                    changeapp.goal_id = session_goal 
                    changeapp.user_id = session_user
                    changeapp.changevariable = changeParamList[count][0]
                    changeapp.date = localtime(timezone.now())
                    
                    if count != image_param['count']:
                        changeapp.before = changeParamList[count][1]
                        changeapp.after = changeParamList[count][2]
                    elif image_param['before'] == False and image_param['after'] == True:
                        changeapp.before_image = '/static/no_image.png' 
                        changeapp.after_image = input_image 
                    else:
                        changeapp.before_image = session_goal.image
                        changeapp.after_image = input_image 

                    changeapp.save()

                    # 変更申請反映関数呼び出し
                    reflectchangefunc(changeapp)
                    count = count + 1 


                # DBから変更申請内容の一覧を取得
                changeapp_list = Changeapplication.objects.filter(goal_id = session_goal).all()
                request.session['changeapp_list'] = changeapp_list

                page_data = subFunc.getpage(request)
                if page_data is None:
                    return render(request, 'sessiontimeout.html')

                params = {
                      'param':0,
                      'param2':2,
                      'imp_page': page_data['imp_page'],
                      'imp_page_max': page_data['imp_page_max'],
                      'app_page': page_data['app_page'],
                      'app_page_max': page_data['app_page_max'],
                      'message': '変更申請が受け付けられました',
                }
                return render(request, 'detailgoalscreen.html', params)
        # フォームの入力に不正が存在
        else:
            initial_dict = {
                    'prefecture_id': input_prefecture_id ,
                    'address' : input_address ,
                    'name' : input_name ,
                    'image' : input_image ,
                    'starttime' : input_starttime ,
                    'endtime' : input_endtime ,
                    'url' : input_url ,
                    'explanation' : input_explanation ,
                    'otherinfo' : input_otherinfo ,
            }
            form = GoalUpdateApplicationForm(initial=itnitial_dict)

            page_data = subFunc.getpage(request)
            if page_data is None:
                return render(request, 'sessiontimeout.html')

            params = {
              'param':0 ,
              'param2':1 ,
              'imp_page': page_data['imp_page'],
              'imp_page_max': page_data['imp_page_max'],
              'error': '入力に不正箇所があります',
              'form':form,
            }
            return render(request, 'detailgoalscreen.html', params)
    # request = GETの場合
    else:
        if 'goal' in request.session:
            goal = request.session['goal']
            initial_dict = {
                    'prefecture_id': goal.prefecture_id.pk ,
                    'address' : goal.address ,
                    'name' : goal.name ,
                    'image' : goal.image ,
                    'starttime' : goal.starttime ,
                    'endtime' : goal.endtime ,
                    'url' : goal.url ,
                    'explanation' : goal.explanation ,
                    'otherinfo' : goal.otherinfo ,
            }
            form = GoalUpdateApplicationForm(initial=initial_dict)

            page_data = subFunc.getpage(request)
            if page_data is None:
                return render(request, 'sessiontimeout.html')

            params = {
                  'param':0 ,
                  'param2':1 ,
                  'imp_page': page_data['imp_page'],
                  'imp_page_max': page_data['imp_page_max'],
                  'form':form ,
               }
            return render(request, 'detailgoalscreen.html', params)
        else:
            return render(request, 'sessiontimeout.html')

##=== ゴール情報削除申請処理 ===##
def deleteapplicationfunc(request):
    # セッションからゴール情報取得
    if 'goal' in request.session and 'user' in request.session:
        session_goal = request.session['goal']
        session_user = request.session['user']
    else:
        # セッションタイムアウト
        return render(request, 'sessiontimeout.html')

    # 変更申請に追加する
    changeapp = Changeapplication()
    changeapp.goal_id = session_goal 
    changeapp.user_id = session_user
    changeapp.changevariable = 'Are you agree with deleting this goal information?' 
    changeapp.before = session_goal.name
    changeapp.after = 'delete'
    changeapp.date = localtime(timezone.now())
    changeapp.save()
    # 変更申請反映関数呼び出し
    reflectchangefunc(changeapp)
    
    page_data = subFunc.getpage(request)
    if page_data is None:
        return render(request, 'sessiontimeout.html')

    params = {
          'param':0,
          'param2':2,
          'imp_page': page_data['imp_page'],
          'imp_page_max': page_data['imp_page_max'],
          'app_page': page_data['app_page'],
          'app_page_max': page_data['app_page_max'],
          'message': '削除申請が受け付けられました',
    }
    return render(request, 'detailgoalscreen.html', params)
    

##=== 関数:変更申請のいいね処理 ===##
def changegoodfunc(request, pk):

    # result = True : 変更が反映されたため、ゴール選択画面に戻る
    result = False

    changeapplication = Changeapplication.objects.get(pk=pk)
    # セッションにあるユーザー情報を取得
    if 'user' in request.session and 'goal' in request.session:
        session_user = request.session['user']
        session_goal = request.session['goal']
    else:
        return render(request, 'sessiontimeout.html')

    # 過去変更申請にいいねを押したユーザー一覧を取得
    good_users = changeapplication.good_users.all()

    # ユーザーがいいねを押したユーザー一覧に含まれていない場合
    if session_user not in good_users:
        changeapplication.good = changeapplication.good + 1
        # ユーザーを過去変更申請にいいねしたユーザー一覧に追加する
        changeapplication.good_users.add(session_user)
        changeapplication.save()
        # 変更申請反映関数呼び出し 
        result = reflectchangefunc(changeapplication)

    if result == True: 
        return redirect('selectgoalscreen', pk=session_goal.prefecture_id.pk)
  
    else:
        page_data = subFunc.getpage(request)
        if page_data is None:
            return render(request, 'sessiontimeout.html')

        params = {
                'param':0,
                'param2':2,
                'imp_page': page_data['imp_page'],
                'imp_page_max': page_data['imp_page_max'],
                'app_page': page_data['app_page'],
                'app_page_max': page_data['app_page_max'],
        }
        return render(request, 'detailgoalscreen.html', params)

   
##=== 関数: 変更申請反映関数 ===##
def reflectchangefunc(changeapplication):
    # ゴールのお気に入り数を取得
    favorite = changeapplication.goal_id.favorite

    #閾値はお気に入り数の3割
    threshold = int(favorite) * 0.3  
    if threshold <= 0:
        threshold = 1

    # 変更申請が閾値以上の場合
    if changeapplication.good >= threshold:
        # 削除処理の時
        if changeapplication.after == 'delete':
            # 削除処理
            Goal.objects.filter(pk=changeapplication.goal_id.pk).delete()
        
        else:
            # 変更処理
            goal = Goal.objects.get(pk=changeapplication.goal_id.pk)

            # changevariableに応じて変更処理
            variable = changeapplication.changevariable

            if variable == '都道府県':
                prefecture_after = Prefecture.objects.get(name=changeapplication.after)
                goal.prefecture_id = prefecture_after
                goal.save()
            elif variable in ['住所', 'ゴール名', '利用可能開始時間', '利用可能終了時間', 'URL', '説明', '補足事項']:
                if variable == '住所':
                    latlon = subFunc.get_lat_lon_from_address(goal.prefecture_id.name + changeapplication.after)
                    goal.address = changeapplication.after
                    goal.lat = latlon['lat']
                    goal.lon = latlon['lon']
                elif variable == 'ゴール名':
                    goal.name = changeapplication.after
                elif variable == '利用可能開始時間':
                    goal.starttime = changeapplication.after
                elif variable == '利用可能終了時間':
                    goal.endtime = changeapplication.after
                elif variable == 'URL':
                    goal.url = changeapplication.after
                elif variable == '説明':
                    goal.explanation = changeapplication.after
                elif variable == '補足事項':
                    goal.otherinfo = changeapplication.after
                goal.save()
            elif variable == '画像':
                goal.image = changeapplication.after_image
                goal.save()

            # 変更申請を削除
            Changeapplication.objects.filter(pk=changeapplication.pk).delete()

        return True

    else:
        # 変更反映まで必要ないいね数を更新
        changeapplication.remaining = threshold - changeapplication.good
        changeapplication.save()
        return False



#===================================================== 画面表示関数 ===================================================#

##=== 関数: ゴール詳細画面表示処理（ゴール選択画面の[詳細表示」が選択された時の処理) ===##
def detailgoalscreenfunc(request, pk):
    # 指定されたpkのゴールのオブジェクトをDBから取得
    goal = Goal.objects.get(pk=pk)
    # セッションに保存する(ゴール情報)
    request.session['goal'] = goal
    
    page_data = subFunc.getpage(request)
    if page_data is None:
        return render(request, 'sessiontimeout.html')

    # ゴール詳細画面に遷移
    params = {
      'param':0 ,
      'param2':0 ,
      'imp_page': page_data['imp_page'],
      'imp_page_max': page_data['imp_page_max'],
      'his_page': page_data['his_page'],
      'his_page_max': page_data['his_page_max'],
    }
    return render(request, 'detailgoalscreen.html', params)


##=== 関数: ゴール選択画面の[位置確認」が押された時に地図にゴールの位置を表示する処理 ===##
def showpositionfunc(request, pk):
    # 指定されたpkのゴールのオブジェクトをDBから取得
    goal = Goal.objects.get(pk=pk)

    # ページ取得
    page_dict = request.session['page_dict']
    goal_page = page_dict['goal_list']

    goal_all = Goal.objects.filter(prefecture_id=goal.prefecture_id).all()

    # 現在のページにおけるゴールリスト切り出し
    goal_list = goal_all[(5*(goal_page-1)) : 5*goal_page]

    # ゴール一覧の最大ページを計算 
    if (len(goal_all) % 5) == 0:
        if len(goal_all) != 0:
            goal_page_max = len(goal_all) // 5
        else:
            goal_page_max = 1
    else:
        goal_page_max = (len(goal_all) // 5) + 1

    params = {
        'lat': goal.lat,
        'lon': goal.lon,
        'goal_page': goal_page,
        'goal_page_max': goal_page_max,
    }
    return render(request, 'selectgoalscreen.html', params)


##=== 関数: ゴール選択画面表示(都道府県検索 -> ゴール一覧表示) ===##
def selectgoalscreenfunc(request, pk):

    # ページ取得
    page_dict = request.session['page_dict']
    goal_page = page_dict['goal_list']

    prefecture = Prefecture.objects.get(pk=pk)
    goal_all = Goal.objects.filter(prefecture_id=prefecture).all()

    # 現在のページにおけるゴールリスト切り出し
    goal_list = goal_all[(5*(goal_page-1)) : 5*goal_page]

    # ゴール一覧の最大ページを計算 
    if (len(goal_all) % 5) == 0:
        if len(goal_all) != 0:
            goal_page_max = len(goal_all) // 5
        else:
            goal_page_max = 1
    else:
        goal_page_max = (len(goal_all) // 5) + 1

    # ゴールのアドレス一覧を緯度経度リストに変換
    goal_latlon_list = []
    for goal in goal_list:
        latlon = {"lat":goal.lat, "lon":goal.lon}
        goal_latlon_list.append(tuple(latlon.values()))

    # セッションに保存する
    request.session['prefecture'] = prefecture
    request.session['goal_list'] = goal_list

    params = {
        'goal_latlon_list':goal_latlon_list,
        'goal_page': goal_page,
        'goal_page_max': goal_page_max,
    }

    # ゴール一覧画面に遷移
    return render(request, 'selectgoalscreen.html', params)


##=== 関数: ゴール詳細画面に変更申請一覧表示 ===##
def showchangeapplicationhistoryfunc(request):
    
    page_data = subFunc.getpage(request)
    if page_data is None:
        return render(request, 'sessiontimeout.html')

    params = {
              'param':0 ,
              'param2':2 ,
              'app_page': page_data['app_page'],
              'app_page_max': page_data['app_page_max'],
              'imp_page': page_data['imp_page'],
              'imp_page_max': page_data['imp_page_max'],
    }
    return render(request, 'detailgoalscreen.html', params)

#===================================================== ページング関数 ===================================================#

##===  関数: ページングの「次へ」に対する処理 ===##
def nextfunc(request, which):
    page_dict = request.session['page_dict']

    if which == 'goal_list':
        prefecture = request.session['prefecture']
        page_value = page_dict['goal_list']
        page_dict['goal_list'] = page_value + 1
        request.session['page_dict'] = page_dict
        return redirect('selectgoalscreen', pk=prefecture.pk) 
    elif which == 'impression':
        goal = request.session['goal']
        page_value = page_dict['impression']
        page_dict['impression'] = page_value + 1
        request.session['page_dict'] = page_dict
        return redirect('detailgoalscreen', pk=goal.pk)
    elif which == 'changeApplication':
        page_value = page_dict['changeApplication']
        page_dict['changeApplication'] = page_value + 1
        request.session['page_dict'] = page_dict
        return redirect('showchangeapplicationhistory')
    elif which == 'changeHistory':
        goal = request.session['goal']
        page_value = page_dict['changeHistory']
        page_dict['changeHistory'] = page_value + 1
        request.session['page_dict'] = page_dict
        return redirect('detailgoalscreen', pk=goal.pk)
    else:
        return redirect('index')


##=== 関数: ページングの「戻る」に対する処理 ===##
def reversefunc(request, which):
    page_dict = request.session['page_dict']

    if which == 'goal_list':
        prefecture = request.session['prefecture']
        page_value = page_dict['goal_list']
        if page_value > 0:
            page_dict['goal_list'] = page_value - 1
            request.session['page_dict'] = page_dict
        return redirect('selectgoalscreen', pk=prefecture.pk)
    elif which == 'impression':
        goal = request.session['goal']
        page_value = page_dict['impression']
        if page_value > 0:
            page_dict['impression'] = page_value - 1
            request.session['page_dict'] = page_dict
        return redirect('detailgoalscreen', pk=goal.pk)
    elif which == 'changeApplication':
        page_value = page_dict['changeApplication']
        if page_value > 0:
            page_dict['changeApplication'] = page_value - 1
            request.session['page_dict'] = page_dict
        return redirect('showchangeapplicationhistory')
    elif which == 'changeHistory':
        goal = request.session['goal']
        page_value = page_dict['changeHistory']
        if page_value > 0:
            page_dict['changeHistory'] = page_value - 1
            request.session['page_dict'] = page_dict
        return redirect('detailgoalscreen', pk=goal.pk)
    else:
        return redirect('index')
