from django.shortcuts import render

def indexfunc(request):
    # ページを初期化
    page_dict = {
            'goal_list': 1,
            'changeApplication':1,
            'changeHistory':1,
            'impression':1,
    }
    request.session['page_dict'] = page_dict

    # セッションにユーザー->ログイン後画面
    if 'user' in request.session:
        return render(request, 'index_af.html')
    # セッションにユーザーがいない場合
    else:
        return render(request, 'index_be.html')
