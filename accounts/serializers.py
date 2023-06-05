from rest_framework import serializers
from .models import Account

class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = Account
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'password', 'is_trainer', 'is_student',\
            'phone_number', 'description')
        read_only_fields = ('id',)

    def create(self, validated_data):
        return Account.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        account = super().update(instance, validated_data)

        if password:
            account.set_password(password)
            account.save()

        return account