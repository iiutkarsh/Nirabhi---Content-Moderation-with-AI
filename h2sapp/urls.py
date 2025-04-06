from django.urls import path
from . import views
from h2sapp.views import moderate_url, moderate_document


urlpatterns = [
    path('',views.base,name="base"),
    path("url/", moderate_url, name="moderate_url"),
    path("document/", moderate_document, name="moderate_document"),
    path("text/", views.text, name="text"),
    path("analyze/", views.analyze_text, name="analyze"),
    path("result/",views.result,name="result")  

]