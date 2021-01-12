from django.shortcuts import render
from .forms import UserForm, UserUpdateForm
#from .models import User
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login


# ユーザー登録func
# 出力: (post) 入力エラー: signup.html
# 出力: (post) 入力正常 : index_be.html
# 出力: (get) セッションにユーザ: index_af.html
# 出力: (get) セッションにユーザなし: index_be.html

def signupfunc(request):
    #requestがpostの場合
    if request.method == 'POST':
        # エラー内容を格納していくリスト
        errorList = []
        # formオブジェクト生成 -> reqestの内容を持つobjectを引数に
        form = UserForm(request.POST)

        if form.is_valid():
            # userformオブジェクトから入力内容を取得する
            input_username = form.cleaned_data['username']
            input_password = form.cleaned_data['password']
            #input_image = form.cleaned_data['image']
            #input_otherinfo = form.cleaned_data['otherinfo']

            # usernameが5文字以上、20文字以内
            username_count = len(input_username)
            if username_count < 5 or username_count > 20:
                errorList.append('ユーザー名は5文字以上20文字以内で入力してください')
            # usernameは英数字で構成
            if not input_username.isalnum():
                errorList.append('ユーザー名は英数字で入力してください')
            # passwordが5文字以上、20文字以内
            password_count = len(input_password)
            if password_count < 5 or password_count > 20:
                errorList.append('パスワードは5文字以上、20文字以内で入力してください')
            # passwordは英数字で構成
            if not input_password.isalnum():
                errorList.append('パスワードは英数字で入力してください')

            # errorListが空でない場合 -> ポリシー違反が発生 -> signup.htmlに戻る
            if len(errorList) >= 1:
                return render(request, 'signup.html', {'errorList':errorList})
            # errorListが空でない場合 -> userオブジェクト作成
            else:
                #user = User()
                #user.username = input_username
                #user.password = input_password
                #user.image = input_image
                #user.otherinfo = input_otherinfo
                #user.save()
                user = User.objects.create_user(input_username, '',input_password)
                return render(request, 'index_be.html', {'message':'ユーザーの登録が完了しました'})

        else:
            return render(request, 'signup', {'message':'入力に不正項目があります'})

    #requestがgetの場合
    else:
        form = UserForm()
        return render(request, 'signup.html', {'form':form})


# ログインfunc
# 出力: (post) 入力内容と合うユーザが存在: index_af.html
# 出力: (post) 入力内容と合うユーザが不在: login.html
# 出力: (get)  入力内容と合うユーザが存在: index_af.html
# 出力: (get)  入力内容と合うユーザが不在: index_be.html
def loginfunc(request):
    #requestがpostの場合
    if request.method == 'POST':
        input_username = request.POST['username']
        input_password = request.POST['password']

        # ユーザーの認証 (認証されたユーザーをuserに格納する)
        user = authenticate(request, username=input_username, password=input_password)
        if user is not None: # userがいる場合
            #login(request, user)
            request.session['user'] = user
            return render(request, 'index_af.html', {'message':'ログインしました'})
        else: 
            return render(request, 'login.html', {'error':'ログインに失敗しました'})
    # request = GET
    else:
        return render(request, 'login.html')



# ログアウトfunc
# 出力: セッションにユーザ存在: login_be.html
# 出力: セッションいユーザ不在: sessiontimeout.html
def logoutfunc(request):
    # セッションにユーザーが存在している場合
    if 'user' in request.session:
        del request.session['user']
        return render(request, 'index_be.html', {'message':'ログアウトが完了しました'})
    else:
        return render(request, 'sessiontimeout.html')


# ユーザー更新func
# 出力: セッションタムアウト sessiontimeout.html
# 出力: (post) ポリシー違反、内容変更されていない: userupdate.html
# 出力: (post) 正常:  
def updatefunc(request):
    # requestがPOSTの場合
    if request.method == 'POST':
        # セッションからユーザー情報取得
        if 'user' in request.session:
            session_user = request.session['user']
        else:
            return render(request, 'sessiontimeout.html')

        # === 更新処理 === #
        form = UserUpdateForm(request.POST)
        if form.is_valid():

            # userformオブジェクトから入力内容を取得する
            input_username = form.cleaned_data['username']
            input_password = form.cleaned_data['password']
            input_password2 = form.cleaned_data['password2']

            ## ポリシー違反チェック
            errorList = []

            username_count = len(input_username)
            if username_count != 0:
                # パスワードとパスワード（確認用）の比較
                if input_password != input_password2:
                    errorList.append('パスワードの入力に誤りがあります')
                # usernameが5文字以上、20文字以内
                if username_count < 5 or username_count > 20:
                    errorList.append('ユーザ名は5文字以上20文字以内で入力してください')
                # usernameは英数字で構成
                if not input_username.isalnum():
                    errorList.append('ユーザー名は英数字で入力してください')

            password_count = len(input_password)
            if password_count != 0:
                # passwordが5文字以上、20文字以内
                if password_count < 5 or password_count > 20:
                    errorList.append('パスワードは5文字以上、20文字以内で入力してください')
                # passwordは英数字で構成
                if not input_password.isalnum():
                    errorList.append('パスワードは英数字で入力してください')

            # errorListが空でない場合 -> ポリシー違反が発生 -> userupdate.htmlに戻る
            if len(errorList) >= 1:
                form = UserUpdateForm(initial = {'username':input_username})
                return render(request, 'userupdate.html', {'errorList':errorList, 'form':form,})

            ## 全く内容が変更されていないかチェック + 変更されている項目特定
            changedParamList = []
            # username
            if len(input_username) != 0:
                if input_username != session_user.username:
                      changedParamList.append(['username', session_user.username, input_username]) 

            # password
            if len(input_password) != 0:
                if not session_user.check_password(input_password):
                       changedParamList.append(['password', session_user.password, input_password])      

            # 入力内容が変更されていない場青
            print(len(changedParamList))
            if len(changedParamList) == 0:
                form = UserUpdateForm(initial = {'username':input_username})
                return render(request, 'userupdate.html', {'error':'内容の変更がありません', 'form': form,})
            else:
                for field in changedParamList:
                    if field[0] == "username":
                        session_user.username = input_username
                    elif field[0] == "password":
                        session_user.set_password(input_password)
                # DB変更適応
                session_user.save()
                # index_af.htmlに戻る 
                return render(request, 'index_af.html', {'message':'ユーザー情報の更新が完了しました'})
    # request = GET                
    else:
       # セッションからユーザー情報取得
       if 'user' in request.session:
           user = request.session['user']
           initial_dict = {
                   'username': user.username,
            }
           form = UserUpdateForm(initial = initial_dict)
           return render(request, 'userupdate.html', {'form':form}) 
       else:
           return render(request, 'sessiontimeout.html')

