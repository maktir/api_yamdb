from rest_framework.routers import DefaultRouter
from .views import GenreViewSet, CategoryViewSet, TitleViewSet
from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router_api = DefaultRouter()

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
    path('token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('v1/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
]
