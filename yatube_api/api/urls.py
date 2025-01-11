from django.urls import path, include

from rest_framework import routers
from rest_framework.authtoken import views

from api.views import PostViewSet


router = routers.DefaultRouter()
router.register('posts', PostViewSet)

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/<int:pk>/', include(router.urls)),
    path('api/v1/api-token-auth/', views.obtain_auth_token),
]
