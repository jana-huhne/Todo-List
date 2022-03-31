from django.urls import path,include
from . import views
from django.conf import settings

app_name = "tasks" 

urlpatterns = [
    path("",views.index, name="index"),
    path("edit/",views.edit, name="edit"),
]
 
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
