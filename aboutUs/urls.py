from django.urls import path,include
from rest_framework.routers import DefaultRouter

from .views import company_info,ArticleViewSet

router = DefaultRouter()
router.register('article', ArticleViewSet)

#  aboutUs/
urlpatterns = [
    path('',company_info),
    path('router/', include(router.urls)), 
]
