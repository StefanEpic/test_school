from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from school import models, serializers
from school.filters import ProductTitleSearchFilter


class ProductViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = models.Product.objects.all().order_by("id")
    serializer_class = serializers.ProductSerializer
    http_method_names = ["get", "head", "options"]


class MyLessonsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.ProductLessonSerializer
    http_method_names = ["get", "head", "options"]
    permission_classes = [IsAuthenticated]
    filter_backends = [ProductTitleSearchFilter]
    search_fields = ["title"]

    def get_queryset(self):
        if self.request.user:
            user_id = self.request.user.id
            return models.Product.objects.filter(clients__user__id=user_id).order_by("id")


class GroupStatisticViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = models.Product.objects.all().order_by("id")
    serializer_class = serializers.ProductStatisticSerializer
    http_method_names = ["get", "head", "options"]
    permission_classes = [IsAuthenticated]
