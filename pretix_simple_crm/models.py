from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q


class OrganizerSalesItem(models.Model):
    organizer = models.ForeignKey(
        "pretixbase.Organizer",
        on_delete=models.CASCADE,
        related_name="crm_sales_items",
    )
    name = models.TextField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("organizer", "name"),
                name="crm_sales_item_organizer_name",
            ),
        ]

    def __str__(self):
        return self.name


class OrganizerSalesItemItem(models.Model):
    organizer_sales_item = models.ForeignKey(
        OrganizerSalesItem,
        on_delete=models.CASCADE,
        related_name="items",
    )
    item = models.OneToOneField(
        "pretixbase.Item",
        on_delete=models.CASCADE,
        related_name="crm_sales_items",
        unique=True,
    )

    def clean(self):
        super().clean()
        if (
            self.organizer_sales_item_id
            and self.item_id
            and self.organizer_sales_item.organizer_id
            != self.item.event.organizer_id
        ):
            raise ValidationError(
                {"item": "The sales item and product must belong to the same organizer."}
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class Customer(models.Model):
    organizer = models.ForeignKey(
        "pretixbase.Organizer",
        on_delete=models.CASCADE,
        related_name="crm_customers",
    )
    name = models.TextField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("organizer", "name"),
                name="crm_customer_organizer_name",
            ),
        ]

    def __str__(self):
        return self.name


class CustomerContacts(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="contacts",
    )
    primary = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("customer",),
                condition=Q(primary=True),
                name="one_primary_customer_contact",
            ),
        ]


class OrderCustomer(models.Model):
    order = models.OneToOneField(
        "pretixbase.Order",
        on_delete=models.CASCADE,
        related_name="crm_customer",
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="orders",
    )

    def clean(self):
        super().clean()
        if (
            self.order_id
            and self.customer_id
            and self.order.organizer_id != self.customer.organizer_id
        ):
            raise ValidationError(
                {"customer": "The order and customer must belong to the same organizer."}
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
