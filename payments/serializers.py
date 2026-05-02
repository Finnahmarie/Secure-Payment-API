from rest_framework import serializers
from django.contrib.auth.models import User
from payments.models import PaymentRecord
from payments.encryption import encrypt_card
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

class PaymentRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentRecord
        fields = '__all__'
        read_only_fields = ['user']

    def create(self, validated_data):
        validated_data['card_number'] = encrypt_card(validated_data['card_number'])
        return super().create(validated_data)