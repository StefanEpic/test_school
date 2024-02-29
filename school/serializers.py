from django.db.models import Avg
from rest_framework import serializers
from school import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ("id", "username", "first_name", "last_name", "email")


class AuthorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = models.Author
        fields = ("id", "user")


class ClientSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = models.Client
        fields = ("id", "user")


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Lesson
        fields = ("id", "title", "video_url")


class ProductSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(read_only=True, many=True, source="lesson_set")
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = models.Product
        fields = (
            "id",
            "title",
            "datetime_start",
            "price",
            "author",
            "lessons",
        )


class ProductLessonSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(read_only=True, many=True, source="lesson_set")

    class Meta:
        model = models.Product
        fields = (
            "title",
            "lessons",
        )


class ProductStatisticSerializer(serializers.ModelSerializer):
    clients_count = serializers.SerializerMethodField()
    filling_groups_percent = serializers.SerializerMethodField()
    product_purchase_percent = serializers.SerializerMethodField()

    class Meta:
        model = models.Product
        fields = (
            "title",
            "clients_count",
            "filling_groups_percent",
            "product_purchase_percent",
        )

    def get_clients_count(self, obj) -> int:
        return obj.clients.count()

    def get_filling_groups_percent(self, obj) -> float:
        obj_avg_clients = (
            obj.group_set.all().annotate(avg_clients=Avg("clients")).aggregate(Avg("avg_clients"))["avg_clients__avg"]
        )
        if obj_avg_clients:
            return round(obj_avg_clients * 100 / obj.max_group_clients, 2)
        return 0

    def get_product_purchase_percent(self, obj) -> float:
        return round(obj.clients.count() / models.Client.objects.all().count(), 2)
