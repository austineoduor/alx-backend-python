from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from messaging import views

router =routers.DefaultRouter()
router.register(r'conversations', views.ConversationViewSet, basename='conversation')
router.register(r'messages', views.MessageViewSet, basename='message')
router.register(r'user', views.UserViewSet, basename='User')
router.register(r'Thread', views.ThreadedMessageViewSet, basename='Thread')

#["NestedDefaultRouter"]
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/',include('rest_framework.urls'))
]