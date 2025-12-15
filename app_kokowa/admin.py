from django.contrib import admin
from .models import Donateur, Lutteur, Soutient, Contribution, PaymentInfo, DeviceInfo, WebhookEvent, Log, Utilisateur, Affrontement


admin.site.register(Donateur)
admin.site.register(Lutteur)
admin.site.register(Soutient)
admin.site.register(Contribution)
admin.site.register(PaymentInfo)
admin.site.register(DeviceInfo)
admin.site.register(WebhookEvent)
admin.site.register(Log)
admin.site.register(Utilisateur)
admin.site.register(Affrontement)
