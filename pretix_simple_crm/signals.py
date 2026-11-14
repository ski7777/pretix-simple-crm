from django.dispatch import receiver
from django.utils.safestring import SafeString


from pretix.control.signals import order_info, order_position_buttons

@receiver(order_info, dispatch_uid="simple_crm_order_info")
def register_order_info(sender, **kwargs):
    return SafeString("CRM-ORDER-INFO")

@receiver(order_position_buttons, dispatch_uid="simple_crm_order_position_buttons")
def register_order_position_buttons(sender, **kwargs):
    return SafeString("CRM-ORDER-POS-BUTS")