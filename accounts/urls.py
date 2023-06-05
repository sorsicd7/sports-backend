from django.urls import path
from .views import AccountListCreateView, AccountDetailView
app_name = "account"
urlpatterns = [
    path('accounts/', AccountListCreateView.as_view(), name='account-list-create'),
    path('accounts/<int:id>/', AccountDetailView.as_view(), name='account-detail'),
]