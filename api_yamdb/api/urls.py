from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import CommentViewSet, ReviewViewSet, GenreViewSet, CategoryViewSet, TitleViewSet

router_api = DefaultRouter()

router_api.register('titles/(?P<title_id>[0-9]+)/reviews)',
                    ReviewViewSet, basename='reviews')
router_api.register('titles/(?P<title_id>[0-9]+)/reviews/(?P<review_id>[0-9]+)/comments',
                    CommentViewSet, basename='comments')
router_api.register(
    'titles',
    TitleViewSet,
    basename='titles'
)
router_api.register(
    'genre',
    GenreViewSet,
    basename='follow'
)
router_api.register(
    'category',
    CategoryViewSet,
    basename='group'
)

urlpatterns = [

    path('', include(router_api.urls)),
    path('v1/', include(router_api.urls)),

urlpatterns += [
    path('token/', TokenObtainPairView.as_view(),

         name='token_obtain_pair'),
    path('v1/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
]
