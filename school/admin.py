from django.contrib import admin

from school.models import Author, Client, Product, Lesson, Group


class ProductClientInline(admin.TabularInline):
    model = Product.clients.through
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    inlines = (ProductClientInline,)


admin.site.register(Author)
admin.site.register(Client)
admin.site.register(Product, ProductAdmin)
admin.site.register(Lesson)
admin.site.register(Group)
