from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from .serializers import CustomTokenObtainPairSerializer
from rest_framework import viewsets
from .models import Category, NewsArticle
from .serializers import CategorySerializer, NewsArticleSerializer


def HomePageView(request):
    return render(request, 'news/home.html')


def ContactPageView(request):
    return render(request, 'news/contact.html')


class NewsListView(ListView):
    model = NewsArticle
    template_name = 'news/news_list.html'
    context_object_name = 'articles'
    ordering = ['-published_at']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class NewsDetailView(DetailView):
    model = NewsArticle
    template_name = 'news/news_detail.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


def redirect_to_swagger(request):
    """
    Redirects to the Swagger UI interface.
    """
    return redirect('schema-swagger-ui')


def redirect_to_redoc(request):
    """
    Redirects to the ReDoc interface.
    """
    return redirect('schema-redoc')


class ObtainTokenPairWithUsername(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = serializer.validated_data['refresh']
        return Response({
            'refresh': str(token),
            'access': str(token.access_token),
            'user_id': user.id,
            'username': user.username,
        })


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class NewsArticleViewSet(viewsets.ModelViewSet):
    queryset = NewsArticle.objects.all()
    serializer_class = NewsArticleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
