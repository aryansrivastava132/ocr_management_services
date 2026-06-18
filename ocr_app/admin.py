from django.contrib import admin
from .models import ScanRecord, DateChart


@admin.register(ScanRecord)
class ScanRecordAdmin(admin.ModelAdmin):
    list_display  = ('id', 'result', 'mfd', 'exp', 'batch', 'scanned_at')
    list_filter   = ('result',)
    search_fields = ('mfd', 'exp', 'batch')
    readonly_fields = ('raw_text', 'scanned_at')


@admin.register(DateChart)
class DateChartAdmin(admin.ModelAdmin):
    list_display  = ('code', 'valid_date', 'product_type')
    search_fields = ('code', 'product_type')
