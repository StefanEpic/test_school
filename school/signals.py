from django.db.models import Count
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from django.utils import timezone

from school.models import Group, Client, Product
from school.utils.signals import split_list_by_sublist


@receiver(m2m_changed, sender=Product.clients.through)
def assign_user_to_group(instance, action, pk_set, **kwargs) -> None:
    """
    Assign a user to a group when gaining access to the product.
    If the product has not started, reassemble the groups
    so that there are approximately the same number of participants everywhere.
    """
    if action == "post_add":
        product = instance
        groups = (
            Group.objects.annotate(clients_count=Count("clients")).filter(product=product).order_by("-clients_count")
        )

        if product.datetime_start <= timezone.now():
            max_group_clients = product.max_group_clients
            for group in groups:
                if group.clients_count < max_group_clients:
                    client = Client.objects.get(id=list(pk_set)[0])
                    group.clients.add(client)
                    break
        else:
            product_clients = Client.objects.filter(products=product)
            for client in product_clients:
                client.groups.clear()
            split_clients_by_group = split_list_by_sublist(
                product_clients, len(groups), product.min_group_clients, product.max_group_clients
            )
            len_split_clients_by_group = len(split_clients_by_group)
            split_clients_index = 0
            for group in groups:
                group.clients.add(*split_clients_by_group[split_clients_index])
                split_clients_index += 1
                if len_split_clients_by_group == split_clients_index:
                    break
