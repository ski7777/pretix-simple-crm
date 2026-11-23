from django.dispatch import receiver
from django.http import HttpRequest
from pretix.base.models import Event, Order, OrderPosition, Item, Organizer
from django.template.loader import get_template
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


from pretix.control.signals import order_info, order_position_buttons, item_formsets, nav_organizer

@receiver(order_info, dispatch_uid="simple_crm_order_info")
def register_order_info(sender: Event, request: HttpRequest, order: Order, **kwargs):
    template = get_template('pretix_simple_crm/control_order_info.html')

    ctx = {}
    return template.render(ctx, request=request)

@receiver(order_position_buttons, dispatch_uid="simple_crm_order_position_buttons")
def register_order_position_buttons(sender: Event, position: OrderPosition, request: HttpRequest, order: Order, **kwargs):
    template = get_template('pretix_simple_crm/order_position_buttons.html')

    ctx = {}
    return template.render(ctx, request=request)

@receiver(item_formsets, dispatch_uid="simple_crm_item_formsets")
def register_item_formsets(sender: Event, request: HttpRequest, item: Item, **kwargs):
    return None

@receiver(nav_organizer, dispatch_uid="simple_crm_nav_organizer")
def register_nav_organizer(sender: Organizer, request: HttpRequest, organizer: Organizer, **kwargs):
    return [
        {
            'label': _('CRM'),
            'url': reverse('control:organizer:crm', kwargs={'organizer': organizer.slug}),
        }
    ]