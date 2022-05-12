from django.urls import path, include
#APIView
from profile_api import views

#viewset
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('hello-viewset',views.HelloViewSet, basename='hello-viewset')
#cuando estamos utilizando un query no se necesita un basename
router.register('profile',views.UserProfileViewSet)
#Url de usuarios
router.register('feed',views.UserProfileFeedViewSet)


urlpatterns = [
    path('hello-view/',views.HellowApiView.as_view()),
    path('login/',views.UserLoginApiView.as_view()),
    #viewset
    path('',include(router.urls))
]
