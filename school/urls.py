from django.urls import path, include
from rest_framework.routers import DefaultRouter

from school import views

router = DefaultRouter()
router.register(r"products", views.ProductViewSet, basename="products")
router.register(r"my-lessons", views.MyLessonsViewSet, basename="my_lessons")
router.register(r"group-statistic", views.GroupStatisticViewSet, basename="group_statistic")

urlpatterns = [
    path("", include(router.urls)),
]
