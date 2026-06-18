from django.db import models


class DateChart(models.Model):
    """Reference table: MFD/EXP codes that are considered valid."""
    code         = models.CharField(max_length=30, unique=True)
    valid_date   = models.CharField(max_length=30)
    product_type = models.CharField(max_length=100, blank=True)
    created_at   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} → {self.valid_date}"

    class Meta:
        ordering = ['code']
        verbose_name = "Date Code"


class ScanRecord(models.Model):
    """Every photo scan is recorded here."""
    RESULT_CHOICES = [('PASS', 'PASS'), ('FAIL', 'FAIL')]

    image      = models.ImageField(upload_to='scans/')
    mfd        = models.CharField(max_length=50, blank=True)
    exp        = models.CharField(max_length=50, blank=True)
    batch      = models.CharField(max_length=50, blank=True)
    raw_text   = models.TextField(blank=True)
    result     = models.CharField(max_length=4, choices=RESULT_CHOICES)
    scanned_at = models.DateTimeField(auto_now_add=True)
    notes      = models.TextField(blank=True)

    def __str__(self):
        return f"#{self.pk} | {self.result} | {self.scanned_at:%d %b %Y %H:%M}"

    class Meta:
        ordering = ['-scanned_at']
