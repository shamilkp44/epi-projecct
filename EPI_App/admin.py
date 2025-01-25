from django.contrib import admin
from .models import Profile, Services, Referral, ProductScheme, pay_his, Payment

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'referral_code', 'referred_by', 'kyc_document_type', 'pan_card', 'bank_passbook')
    search_fields = ('user__username', 'referral_code')
    list_filter = ('kyc_document_type',)

class ServicesAdmin(admin.ModelAdmin):
    list_display = ('title', 'product_id', 'total')
    search_fields = ('title', 'product_id')
    list_filter = ('total',)

class ProductSchemeAdmin(admin.ModelAdmin):
    list_display = ('product_id','investment', 'total', 'days', 'start_date', 'end_date')
    search_fields = ['product_id']
    list_filter = ['investment']

class Pay_hisAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'title', 'img', 'investments', 'total', 'balance', 'backcount')
    search_fields = ('title',)
    list_filter = ('title',)

class ReferralAdmin(admin.ModelAdmin):
    list_display = ('referred_by', 'referred_user', 'timestamp')

admin.site.register(Profile,ProfileAdmin)
admin.site.register(Services,ServicesAdmin)
admin.site.register(Referral,ReferralAdmin)
admin.site.register(pay_his)
admin.site.register(Payment)
admin.site.register(ProductScheme,ProductSchemeAdmin)