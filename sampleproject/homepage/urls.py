from django.urls import path
from . import views
from .views import display_view, detailed_view
from .views import delete_view

urlpatterns = [
    path('login_page/', views.login_view, name='login_page'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add_employee/', views.create_view, name='add_employee'),
    path('view_employee/', views.display_view, name='view_employee'),
    path('detailed_view/<int:id>', views.detailed_view, name='view_detail'),
    path('delete_view/<int:id>', views.delete_view),
    path('update_view/<int:id>', views.update_view)
]