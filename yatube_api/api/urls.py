from django.urls import path, include

from rest_framework import routers
from rest_framework.authtoken import views

from api.views import PostViewSet, GroupRetrieveViewSet, CommentViewSet


router = routers.DefaultRouter()
router.register('posts', PostViewSet, basename='post')
router.register('groups', GroupRetrieveViewSet, basename='group')
router.register(r'^posts/(?P<post_id>\d+)/comments',
                CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token),
]
