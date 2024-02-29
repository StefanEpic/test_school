from django.contrib.auth.models import User
from django.db import models


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.user.username)


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.user.username)


class Product(models.Model):
    title = models.CharField(max_length=100)
    datetime_start = models.DateTimeField()
    price = models.FloatField()
    max_group_clients = models.IntegerField(default=1)
    min_group_clients = models.IntegerField(default=0)
    author = models.ForeignKey(Author, on_delete=models.PROTECT)
    clients = models.ManyToManyField(Client, related_name="products", through="ProductClient")

    def __str__(self) -> str:
        return str(self.title)


class ProductClient(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product} / {self.client}"


class Lesson(models.Model):
    title = models.CharField(max_length=100)
    video_url = models.URLField()
    product = models.ForeignKey(Product, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.title)


class Group(models.Model):
    title = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    clients = models.ManyToManyField(Client, related_name="groups", blank=True)

    def __str__(self):
        return str(self.title)
