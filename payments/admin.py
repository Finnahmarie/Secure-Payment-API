from django.contrib import admin
from payments.models import PaymentRecord

class PaymentRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'card_number', 'amount')

admin.site.register(PaymentRecord, PaymentRecordAdmin)