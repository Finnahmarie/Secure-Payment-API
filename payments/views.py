import logging
import json
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from django.http import JsonResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, AllowAny
from payments.models import PaymentRecord
from payments.serializers import PaymentRecordSerializer, UserSerializer

logger = logging.getLogger('payments')

class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(ratelimit(key='ip', rate='5/m', block=False), name='dispatch')
class PaymentRecordViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentRecordSerializer
    
    def get_queryset(self):
        return PaymentRecord.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        logger.warning(f"Payment record created for user: {self.request.user.username}")

    def dispatch(self, request, *args, **kwargs):
        if getattr(request, 'limited', False):
            return JsonResponse({"error": "Too many requests. Try again in a minute."}, status=429)
        return super().dispatch(request, *args, **kwargs)

@csrf_exempt
@ratelimit(key='ip', rate='5/m', block=False)
def login_view(request):
    if getattr(request, 'limited', False):
        return JsonResponse({"error": "Too many requests. Try again in a minute."}, status=429)

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")

            logger.warning(f"Login attempt for username: {username}")
            user = authenticate(username=username, password=password)

            if user is not None:
                return JsonResponse({"message": "Login successful", "username": username})
            else:
                logger.warning(f"Failed login attempt for username: {username}")
                return JsonResponse({"error": "Invalid credentials"}, status=401)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)