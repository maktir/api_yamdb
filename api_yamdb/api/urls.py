from django.urls import include, path
from rest_framework import routers


from .views import (CommentViewSet, ReviewViewSet,
                    GenreViewSet, CategoryViewSet,
                    TitleViewSet, EmailCodeSendView,
                    UserViewSet, email_token_obtain_view,)

router_api = routers.DefaultRouter()
router_api.register(r'users', UserViewSet, basename='users')
router_api.register(r'titles/(?P<title_id>\d+)/reviews',
                    ReviewViewSet, basename='reviews')
router_api.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)
router_api.register(
    r'titles',
    TitleViewSet,
    basename='titles'
)
router_api.register(
    r'genres',
    GenreViewSet,
    basename='genre'
)
router_api.register(
    r'categories',
    CategoryViewSet,
    basename='categories'
)

urlpatterns = [
    path('v1/', include(router_api.urls)),
    path('v1/auth/email/', EmailCodeSendView.as_view(), name='email_code'),
    path('v1/auth/token/', email_token_obtain_view, name='get_token'),
]
