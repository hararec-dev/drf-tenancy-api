from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.business.models import Feature, Subscription
from apps.core.models import TimestampedModel
from apps.tenancies.models import Tenant


class Invoice(TimestampedModel):
    """
    Invoice generated for a tenant.
    Corresponds to the 'invoices' table.
    """

    class Status(models.TextChoices):
        DRAFT = "draft", _("Draft")
        OPEN = "open", _("Open")
        PAID = "paid", _("Paid")
        UNCOLLECTIBLE = "uncollectible", _("Uncollectible")
        VOID = "void", _("Voided")

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, verbose_name=_("tenant"))
    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("subscription"),
    )
    status = models.CharField(_("status"), max_length=20, choices=Status.choices, default=Status.DRAFT)
    issued_at = models.DateTimeField(_("issued at"), null=True, blank=True)
    due_date = models.DateField(_("due date"))
    period_start = models.DateField(_("period start"))
    period_end = models.DateField(_("period end"))
    currency = models.CharField(_("currency"), max_length=3, default="USD")
    subtotal = models.DecimalField(_("subtotal"), max_digits=12, decimal_places=2)
    tax_total = models.DecimalField(_("total taxes"), max_digits=12, decimal_places=2, default=0)
    discount_total = models.DecimalField(_("total discounts"), max_digits=12, decimal_places=2, default=0)
    amount_due = models.DecimalField(_("amount due"), max_digits=12, decimal_places=2)
    amount_paid = models.DecimalField(_("amount paid"), max_digits=12, decimal_places=2, default=0)
    invoice_pdf_url = models.URLField(_("invoice PDF URL"), max_length=255, blank=True, null=True)
    gateway_invoice_id = models.CharField(
        _("gateway invoice ID"),
        max_length=255,
        unique=True,
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "invoices"
        verbose_name = _("invoice")
        verbose_name_plural = _("invoices")
        unique_together = [["subscription", "period_end"]]
        indexes = [
            models.Index(fields=["tenant"], name="idx_invoices_tenant_id"),
            models.Index(fields=["status"], name="idx_invoices_status"),
        ]


class InvoiceLineItem(models.Model):
    """
    Invoice line item.
    Corresponds to the 'invoice_line_items' table.
    """

    class LineItemType(models.TextChoices):
        SUBSCRIPTION = "subscription", _("Subscription")
        USAGE = "usage", _("Usage")
        ONE_TIME = "one_time", _("One-time charge")
        DISCOUNT = "discount", _("Discount")
        TAX = "tax", _("Tax")
        CREDIT = "credit", _("Credit")

    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name="line_items",
        verbose_name=_("invoice"),
    )
    description = models.TextField(_("description"))
    quantity = models.IntegerField(_("quantity"), default=1)
    unit_price = models.DecimalField(_("unit price"), max_digits=12, decimal_places=2)
    amount = models.DecimalField(_("amount"), max_digits=12, decimal_places=2)
    type = models.CharField(_("type"), max_length=50, choices=LineItemType.choices, blank=True, null=True)
    period_starts_at = models.DateField(_("period start"), null=True, blank=True)
    period_ends_at = models.DateField(_("period end"), null=True, blank=True)
    usage_feature = models.ForeignKey(
        Feature,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("usage feature"),
    )
    unit_price_tier = models.JSONField(
        _("unit price tier"),
        null=True,
        blank=True,
        help_text=_("The pricing tier that was applied."),
    )

    class Meta:
        db_table = "invoice_line_items"
        verbose_name = _("invoice line")
        verbose_name_plural = _("invoice lines")
        indexes = [
            models.Index(fields=["invoice"], name="idx_invoice_line_id"),
        ]


class PaymentMethod(TimestampedModel):
    """
    Tenant payment method stored in an external provider.
    Corresponds to the 'payment_methods' table.
    """

    class MethodType(models.TextChoices):
        CREDIT_CARD = "credit_card", _("Credit Card")
        PAYPAL = "paypal", _("PayPal")
        BANK_ACCOUNT = "bank_account", _("Bank Account")

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, verbose_name=_("tenant"))
    method_type = models.CharField(_("method type"), max_length=50, choices=MethodType.choices)
    gateway_payment_method_id = models.CharField(_("gateway method ID"), max_length=255, unique=True)
    is_default = models.BooleanField(_("is default"), default=False)
    details = models.JSONField(
        _("details"),
        help_text=_("Last 4 digits, expiration date, etc. NEVER sensitive data."),
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "payment_methods"
        verbose_name = _("payment method")
        verbose_name_plural = _("payment methods")


class Payment(TimestampedModel):
    """
    Record of a payment attempt.
    Corresponds to the 'payments' table.
    """

    class Status(models.TextChoices):
        PENDING = "pending", _("Pending")
        SUCCEEDED = "succeeded", _("Succeeded")
        FAILED = "failed", _("Failed")
        REFUNDED = "refunded", _("Refunded")

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, verbose_name=_("tenant"))
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("invoice"),
    )
    amount = models.DecimalField(_("amount"), max_digits=10, decimal_places=2)
    currency = models.CharField(_("currency"), max_length=3, default="USD")
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.PROTECT, verbose_name=_("payment method"))
    gateway_transaction_id = models.CharField(
        _("gateway transaction ID"),
        max_length=255,
        unique=True,
        null=True,
        blank=True,
    )
    status = models.CharField(_("status"), max_length=20, choices=Status.choices)
    paid_at = models.DateTimeField(_("paid at"), null=True, blank=True)
    details = models.JSONField(
        _("details"),
        help_text=_("Used to store gateway responses, etc."),
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "payments"
        verbose_name = _("payment")
        verbose_name_plural = _("payments")
        indexes = [
            models.Index(fields=["tenant"], name="idx_payments_tenant_id"),
            models.Index(fields=["invoice"], name="idx_payments_invoice_id"),
        ]


class UsageRecord(models.Model):
    """
    Detailed tracking record for pay-per-use features.
    Corresponds to the 'usage_records' table.
    """

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, verbose_name=_("tenant"))
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("user"),
    )
    feature = models.ForeignKey(Feature, on_delete=models.PROTECT, verbose_name=_("feature"))
    quantity = models.DecimalField(
        _("quantity"),
        max_digits=18,
        decimal_places=6,
        help_text=_("Supports fractional values (e.g., GB, hours)."),
    )
    recorded_at = models.DateTimeField(_("recorded at"), auto_now_add=True)
    event_time = models.DateTimeField(_("event time"))
    source_ip = models.GenericIPAddressField(_("source IP"), null=True, blank=True)
    reference_id = models.CharField(
        _("reference ID"),
        max_length=255,
        null=True,
        blank=True,
        help_text=_("External resource ID (e.g., transaction ID)."),
    )

    class Meta:
        db_table = "usage_records"
        verbose_name = _("usage record")
        verbose_name_plural = _("usage records")
        indexes = [
            models.Index(fields=["tenant", "feature"], name="idx_usg_rec_tenant_feat"),
            models.Index(fields=["event_time"], name="idx_usage_records_event_time"),
        ]


class CreditTransaction(models.Model):
    """
    Records credit transactions for a tenant.
    Corresponds to the 'credit_transactions' table.
    """

    class TransactionType(models.TextChoices):
        PURCHASE = "purchase", _("Purchase")
        USAGE = "usage", _("Usage")
        ADJUSTMENT = "adjustment", _("Adjustment")

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, verbose_name=_("tenant"))
    amount = models.DecimalField(_("amount"), max_digits=12, decimal_places=2)
    balance_after = models.DecimalField(_("balance after"), max_digits=12, decimal_places=2)
    transaction_type = models.CharField(_("transaction type"), max_length=20, choices=TransactionType.choices)
    reference_id = models.BigIntegerField(
        _("reference ID"),
        null=True,
        blank=True,
        help_text=_("Link to payments/invoices."),
    )
    description = models.TextField(_("description"), blank=True, null=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)

    class Meta:
        db_table = "credit_transactions"
        verbose_name = _("credit transaction")
        verbose_name_plural = _("credit transactions")


class InvoiceLineItemUsageRecord(models.Model):
    invoice_line_item = models.ForeignKey(
        InvoiceLineItem,
        on_delete=models.CASCADE,
        related_name="usage_records",
        db_column="invoice_line_item_id",
    )
    usage_record = models.ForeignKey(
        UsageRecord,
        on_delete=models.CASCADE,
        related_name="invoice_line_items",
        db_column="usage_record_id",
    )

    class Meta:
        db_table = "invoice_line_item_usage_records"
        unique_together = (("invoice_line_item", "usage_record"),)
        verbose_name = "Invoice Line Item Usage Record"
        verbose_name_plural = "Invoice Line Item Usage Records"
