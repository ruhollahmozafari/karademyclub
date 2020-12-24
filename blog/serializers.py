from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):
    title = serializers.CharField
