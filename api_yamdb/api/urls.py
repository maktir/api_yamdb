from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, ReviewViewSet

router_api = DefaultRouter()

router_api.register('titles/(?P<title_id>[0-9]+)/reviews)',
                    ReviewViewSet, basename='reviews')
router_api.register('titles/(?P<title_id>[0-9]+)/reviews/(?P<review_id>[0-9]+)/comments',
                    CommentViewSet, basename='comments')


urlpatterns = [
    path('', include(router_api.urls)),
    path('v1/', include(router_api.urls)),
]
