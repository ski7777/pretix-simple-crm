from django.dispatch import receiver
from django.http import HttpRequest
from django.utils.safestring import SafeString
from pretix.base.models import Event, Order, OrderPosition
from django.template.loader import get_template


from pretix.control.signals import order_info, order_position_buttons

@receiver(order_info, dispatch_uid="simple_crm_order_info")
def register_order_info(sender: Event, request: HttpRequest, order: Order, **kwargs):
    template = get_template('pretix_simple_crm/control_order_info.html')

    ctx = {}
    return template.render(ctx, request=request)

@receiver(order_position_buttons, dispatch_uid="simple_crm_order_position_buttons")
def register_order_position_buttons(sender: Event, position: OrderPosition, request: HttpRequest, order: Order, **kwargs):
    return None
    return SafeString("CRM-ORDER-POS-BUTS")