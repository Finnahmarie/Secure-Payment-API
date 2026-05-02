from rest_framework.routers import DefaultRouter
from payments.views import PaymentRecordViewSet, login_view, RegisterView
from django.urls import path

router = DefaultRouter()
router.register(r'payments', PaymentRecordViewSet, basename='payments')

urlpatterns = [
    path('login/', login_view),
    path('register/', RegisterView.as_view()),
]

urlpatterns += router.urls