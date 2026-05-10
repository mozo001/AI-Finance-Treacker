from django.contrib import admin

# Register your models here.
from .models import Transaction

class TransactionAdmin(admin.ModelAdmin):
  list_display = ("title", "amount", "date","transaction_type","category","description")

admin.site.register(Transaction, TransactionAdmin)