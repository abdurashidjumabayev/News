from django.urls import path,include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import CategoryViewSet, NewsArticleViewSet, HomePageView, ContactPageView, NewsListView, NewsDetailView

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'articles', NewsArticleViewSet)


urlpatterns = [
    path('', HomePageView, name='home'),
    path('contact/', ContactPageView, name='contact'),
    path('news/', NewsListView.as_view(), name='news_list'),
    path('news/<int:pk>/', NewsDetailView.as_view(), name='news_detail'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]
