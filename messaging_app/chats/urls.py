from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from chats import views

router = DefaultRouter()
router.register(r'conversations', views.ConversationViewSet, basename='conversation')
router.register(r'messages', views.MessageViewSet, basename='message')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/',include('rest_framework.urls'))
]