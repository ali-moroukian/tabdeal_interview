from django.contrib import admin

from sellers.models import Seller, Transaction


class TransactionInline(admin.TabularInline):
    model = Transaction
    readonly_fields = ('seller', 'amount', 'type', 'extra_data')
    can_delete = False
    extra = 0


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('id', 'balance')
    readonly_fields = ('balance',)
    inlines = (TransactionInline,)


@admin.register(Transaction)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('id', 'seller', 'amount', 'type', 'time')
    list_filter = ('type',)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
