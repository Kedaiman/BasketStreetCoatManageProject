from django.contrib import admin
from django.urls import path
from django.urls import include
from .views import indexfunc
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('manageuser/', include('manageuser.urls')),
    path('managegoal/', include('managegoal.urls')),
    # index.htmlに移る(indexfuncでログイン前、ログイン後画面に遷移する)
    path('index/',indexfunc, name='index')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 


