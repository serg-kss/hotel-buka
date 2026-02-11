from django.contrib import admin
from django.urls import reverse
from django.http import HttpResponseRedirect


class SingletonAdmin(admin.ModelAdmin):
    """
    Базовый админ-класс для моделей,
    у которых может быть только одна запись.
    """

    def has_add_permission(self, request):
        return not self.model.objects.exists()

    def response_add(self, request, obj, post_url_continue=None):
        return HttpResponseRedirect(
            reverse(f"admin:{self.model._meta.app_label}_{self.model._meta.model_name}_changelist")
        )

    def response_change(self, request, obj):
        return HttpResponseRedirect(
            reverse(f"admin:{self.model._meta.app_label}_{self.model._meta.model_name}_changelist")
        )

    save_as = False
    save_on_top = False

    def render_change_form(self, request, context, *args, **kwargs):
        context.update({
            "show_save_and_add_another": False,
            "show_save_and_continue": False,
        })
        return super().render_change_form(request, context, *args, **kwargs)
