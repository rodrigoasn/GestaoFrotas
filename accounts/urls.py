# ────────────────────────────────────────────────────────────────────
# IMPORTS
# ────────────────────────────────────────────────────────────────────
from django.urls import path
from .views import UserListView, UserCreateView, UserUpdateView, UserDeleteView, ProfileView, UserPasswordChangeView, UserPermissionsView, GroupListView, GroupCreateView, GroupUpdateView, GroupDeleteView


# ────────────────────────────────────────────────────────────────────
# URLS
# ────────────────────────────────────────────────────────────────────
urlpatterns = [
    # Usuários
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/add/', UserCreateView.as_view(), name='user_add'),
    path('users/<int:pk>/', UserUpdateView.as_view(), name='user_change'),
    path('users/<int:pk>/password/', UserPasswordChangeView.as_view(), name='user_password_change'),
    path('users/<int:pk>/permissions/', UserPermissionsView.as_view(), name='user_permissions'),
    path('users/<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),
    
    # Perfil do usuário
    path('profile/', ProfileView.as_view(), name='profile'),

    # Grupos
    path('groups/', GroupListView.as_view(), name='group_list'),
    path('groups/add/', GroupCreateView.as_view(), name='group_add'),
    path('groups/<int:pk>/', GroupUpdateView.as_view(), name='group_change'),
    path('groups/<int:pk>/delete/', GroupDeleteView.as_view(), name='group_delete'),
]
