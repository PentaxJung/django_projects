# pentaxjung/blog/urls.py

from django.urls import path, include
from . import views # 현재 폴더의 views.py를 import

urlpatterns = [
	path('', views.index),
	path('blog/', views.index),
	path('blog/page/<int:page>/', views.index),
	path('blog/entry/<int:entry_id>/', views.read),
	path('blog/write/', views.write_form),
	path('blog/add/post/', views.add_post),
	path('blog/add/comment/', views.add_comment),
	path('blog/del/comment/', views.del_comment),
]
