# ────────────────────────────────────────────────────────────────────
# IMPORTS
# ────────────────────────────────────────────────────────────────────
from django.urls import path
from .views import DashboardView, UserListView, UserCreateView, UserUpdateView, UserDeleteView, ProfileView, UserPasswordChangeView


# ────────────────────────────────────────────────────────────────────
# URLS
# ────────────────────────────────────────────────────────────────────
urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    
    # Usuários
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/add/', UserCreateView.as_view(), name='user_add'),
    path('users/<int:pk>/', UserUpdateView.as_view(), name='user_change'),
    path('users/<int:pk>/password/', UserPasswordChangeView.as_view(), name='user_password_change'),
    path('users/<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),
    
    # Perfil
    path('profile/', ProfileView.as_view(), name='profile'),
]
