from django.utils.translation import gettext_lazy

from . import __version__

try:
    from pretix.base.plugins import PluginConfig
except ImportError:
    raise RuntimeError("Please use pretix 2026.9.0 or above to run this plugin!")


class PluginApp(PluginConfig):
    default = True
    name = "pretix_simple_crm"
    verbose_name = "Simple CRM"

    class PretixPluginMeta:
        name = gettext_lazy("Simple CRM")
        author = "ski7777"
        description = gettext_lazy("Simple CRM system to track order baehavior of customers across events")
        visible = True
        version = __version__
        category = "FEATURE"
        compatibility = "pretix>=2026.9.0"
        settings_links = []
        navigation_links = []

    def ready(self):
        from . import signals  # NOQA
