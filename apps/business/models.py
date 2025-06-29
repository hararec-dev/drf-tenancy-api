from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseAuditModel, TimestampedModel
from apps.tenancies.models import Tenant


class Feature(models.Model):
    """
    Describes a system feature that can be included in a plan.
    Corresponds to the 'features' table.
    """

    class FeatureType(models.TextChoices):
        LIMIT = "limit", _("Limit")  # e.g., '1000' users
        BOOLEAN = "boolean", _("Boolean")  # e.g., 'true'
        METERED = "metered", _("Metered")  # e.g., 'pay-as-you-go'

    class ValueType(models.TextChoices):
        BOOLEAN = "boolean", _("Boolean")
        INTEGER = "integer", _("Integer")
        TEXT = "text", _("Text")

    codename = models.CharField(
        _("codename"),
        max_length=100,
        unique=True,
        help_text=_("e.g., 'max_users', 'api_access'"),
    )
    description = models.TextField(_("description"), blank=True, null=True)
    type = models.CharField(_("type"), max_length=50, choices=FeatureType.choices)
    value_type = models.CharField(
        _("value type"),
        max_length=20,
        choices=ValueType.choices,
        default=ValueType.BOOLEAN,
        help_text=_(
            "Defines how to interpret the value in plan_features: boolean (on/off), "
            "integer (limit), text (specific value)."
        ),
    )

    def __str__(self):
        return self.codename

    class Meta:
        db_table = "features"
        verbose_name = _("feature")
        verbose_name_plural = _("features")


class Plan(BaseAuditModel):
    """
    Defines a subscription plan that tenants can subscribe to.
    Corresponds to the 'plans' table.
    """

    name = models.CharField(_("name"), max_length=100, unique=True)
    description = models.TextField(_("description"), blank=True, null=True)
    features = models.ManyToManyField(
        Feature, through="PlanFeature", verbose_name=_("features")
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = "plans"
        verbose_name = _("plan")
        verbose_name_plural = _("plans")


class PlanFeature(models.Model):
    """
    Intermediate table associating a feature with a plan and a specific value.
    Corresponds to the 'plan_features' table.
    """

    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)
    value = models.CharField(
        _("value"),
        max_length=255,
        help_text=_("Feature value for this plan (e.g., '100', 'true')"),
    )

    class Meta:
        db_table = "plan_features"
        unique_together = [["plan", "feature"]]


class PlanPrice(BaseAuditModel):
    """
    Defines the price of a plan for a specific billing period and currency.
    Corresponds to the 'plan_prices' table.
    """

    class BillingPeriod(models.TextChoices):
        MONTHLY = "monthly", _("Monthly")
        ANNUAL = "annual", _("Annual")

    plan = models.ForeignKey(
        Plan, on_delete=models.CASCADE, related_name="prices", verbose_name=_("plan")
    )
    billing_period = models.CharField(
        _("billing period"), max_length=20, choices=BillingPeriod.choices
    )
    price_amount = models.DecimalField(_("amount"), max_digits=10, decimal_places=2)
    currency = models.CharField(_("currency"), max_length=3, default="USD")

    class Meta:
        db_table = "plan_prices"
        verbose_name = _("plan price")
        verbose_name_plural = _("plan prices")
        unique_together = [["plan", "billing_period", "currency"]]


class Subscription(TimestampedModel):
    """
    Tenant subscription to a plan.
    Corresponds to the 'subscriptions' table.
    """

    class Status(models.TextChoices):
        ACTIVE = "active", _("Active")
        PENDING = "pending", _("Pending")
        CANCELED = "canceled", _("Canceled")
        EXPIRED = "expired", _("Expired")
        TRIALING = "trialing", _("Trialing")

    tenant = models.ForeignKey(
        Tenant, on_delete=models.CASCADE, verbose_name=_("tenant")
    )
    plan = models.ForeignKey(
        Plan, on_delete=models.PROTECT, verbose_name=_("plan")
    )  # Do not delete plan if there are subscribers
    plan_price = models.ForeignKey(
        PlanPrice, on_delete=models.PROTECT, verbose_name=_("plan price")
    )
    status = models.CharField(_("status"), max_length=20, choices=Status.choices)
    trial_ends_at = models.DateTimeField(_("trial ends at"), null=True, blank=True)
    current_period_starts_at = models.DateTimeField(_("current period starts at"))
    current_period_ends_at = models.DateTimeField(_("current period ends at"))
    cancel_at_period_end = models.BooleanField(_("cancel at period end"), default=False)

    class Meta:
        db_table = "subscriptions"
        verbose_name = _("subscription")
        verbose_name_plural = _("subscriptions")
        indexes = [
            models.Index(fields=["tenant"], name="idx_subscriptions_tenant_id"),
            models.Index(fields=["plan"], name="idx_subscriptions_plan_id"),
            models.Index(fields=["status"], name="idx_subscriptions_status"),
        ]


class FeatureTier(TimestampedModel):
    """
    Defines tiered pricing for metered-usage features.
    Corresponds to the 'feature_tiers' table.
    """

    feature = models.ForeignKey(
        Feature, on_delete=models.CASCADE, verbose_name=_("feature")
    )
    up_to = models.IntegerField(
        _("up to"),
        help_text=_(
            "The accumulated usage up to this point. The last tier can have an infinite or very large value."
        ),
    )
    unit_price = models.DecimalField(_("unit price"), max_digits=12, decimal_places=6)
    flat_fee = models.DecimalField(
        _("flat fee"), max_digits=12, decimal_places=2, default=0
    )
    currency = models.CharField(_("currency"), max_length=3)
    plan_price = models.ForeignKey(
        PlanPrice, on_delete=models.CASCADE, verbose_name=_("plan price")
    )

    class Meta:
        db_table = "feature_tiers"
        verbose_name = _("feature tier")
        verbose_name_plural = _("feature tiers")
        indexes = [
            models.Index(fields=["feature"], name="idx_feature_tiers_feature_id"),
            models.Index(fields=["plan_price"], name="idx_feat_tier_plan_price_id"),
        ]


class Coupon(models.Model):
    """
    Stores discount coupons applicable to subscriptions.
    Corresponds to the 'coupons' table.
    """

    class DiscountType(models.TextChoices):
        PERCENTAGE = "percentage", _("Percentage")
        FIXED_AMOUNT = "fixed_amount", _("Fixed Amount")

    class Duration(models.TextChoices):
        ONCE = "once", _("Once")
        REPEATING = "repeating", _("Repeating")
        FOREVER = "forever", _("Forever")

    code = models.CharField(_("code"), max_length=100, unique=True)
    description = models.TextField(_("description"), blank=True, null=True)
    discount_type = models.CharField(
        _("discount type"), max_length=20, choices=DiscountType.choices
    )
    discount_value = models.DecimalField(
        _("discount value"), max_digits=10, decimal_places=2
    )
    duration = models.CharField(_("duration"), max_length=20, choices=Duration.choices)
    duration_in_months = models.IntegerField(
        _("duration in months"),
        null=True,
        blank=True,
        help_text=_('Only applicable if duration is "repeating"'),
    )
    is_active = models.BooleanField(_("is active"), default=True)
    max_redemptions = models.IntegerField(
        _("max redemptions"),
        null=True,
        blank=True,
        help_text=_("Maximum number of times this coupon can be used in total"),
    )
    redeem_by = models.DateTimeField(
        _("redeem by"),
        null=True,
        blank=True,
        help_text=_("Expiration date of the coupon"),
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)

    def __str__(self):
        return self.code

    class Meta:
        db_table = "coupons"
        verbose_name = _("coupon")
        verbose_name_plural = _("coupons")


class SubscriptionDiscount(models.Model):
    """
    Junction table to apply a coupon to a subscription.
    Corresponds to the 'subscription_discounts' table.
    """

    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.CASCADE,
        related_name="discounts",
        verbose_name=_("subscription"),
    )
    coupon = models.ForeignKey(
        Coupon,
        on_delete=models.RESTRICT,
        related_name="subscription_discounts",
        verbose_name=_("coupon"),
    )
    redeemed_at = models.DateTimeField(_("redeemed at"), auto_now_add=True)

    def __str__(self):
        return f"{self.subscription} - {self.coupon}"

    class Meta:
        db_table = "subscription_discounts"
        verbose_name = _("subscription discount")
        verbose_name_plural = _("subscription discounts")
        indexes = [
            models.Index(
                fields=["subscription"],
                name="idx_sub_disc_sub_id",
            ),
        ]


class CreditLedger(models.Model):
    """
    Append-only table that records all credit transactions for a tenant.
    Corresponds to the 'credit_ledger' table.
    """

    class TransactionType(models.TextChoices):
        PURCHASE = "purchase", _("Purchase")
        USAGE_DEDUCTION = "usage_deduction", _("Usage Deduction")
        REFUND = "refund", _("Refund")
        ADJUSTMENT = "adjustment", _("Adjustment")

    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name="credit_transactions",
        verbose_name=_("tenant"),
    )
    transaction_type = models.CharField(
        _("transaction type"), max_length=50, choices=TransactionType.choices
    )
    amount = models.BigIntegerField(
        _("amount"),
        help_text=_(
            "Positive for purchases/credits, negative for consumption/deductions."
        ),
    )
    balance_after = models.BigIntegerField(
        _("balance after"), help_text=_("The resulting balance after this transaction")
    )
    description = models.TextField(_("description"), blank=True, null=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    invoice_line_item_id = models.BigIntegerField(
        _("invoice line item ID"),
        null=True,
        blank=True,
        help_text=_(
            "Optional: link to the invoice line where credits were purchased/used"
        ),
    )
    actor_id = models.BigIntegerField(
        _("actor ID"),
        null=True,
        blank=True,
        help_text=_("Optional: The user or system that generated the transaction"),
    )

    def __str__(self):
        return f"{self.tenant} - {self.transaction_type} - {self.amount}"

    class Meta:
        db_table = "credit_ledger"
        verbose_name = _("credit transaction")
        verbose_name_plural = _("credit transactions")
        indexes = [
            models.Index(
                fields=["tenant", "-created_at"],
                name="idx_cred_led_ten_created_at",
            ),
        ]


class PlanVersionHistory(models.Model):
    """
    History of changes to plans and prices.
    Corresponds to the 'plan_version_history' table.
    """

    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, verbose_name=_("plan"))
    plan_price = models.ForeignKey(
        PlanPrice, on_delete=models.CASCADE, verbose_name=_("plan price")
    )
    changeset = models.JSONField(
        _("changeset"), help_text=_("Details of changes (name, description, etc.)")
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    changed_by_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("changed by"),
    )

    class Meta:
        db_table = "plan_version_history"
        verbose_name = _("plan version history")
        verbose_name_plural = _("plan version histories")


class SubscriptionEvent(models.Model):
    """
    Lifecycle events for subscriptions.
    Corresponds to the 'subscription_events' table.
    """

    class EventType(models.TextChoices):
        UPGRADE = "upgrade", _("Upgrade")
        DOWNGRADE = "downgrade", _("Downgrade")
        CANCEL = "cancel", _("Cancel")
        RENEWAL = "renewal", _("Renewal")

    subscription = models.ForeignKey(
        Subscription, on_delete=models.CASCADE, verbose_name=_("subscription")
    )
    event_type = models.CharField(
        _("event type"), max_length=50, choices=EventType.choices
    )
    event_data = models.JSONField(_("event data"))
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)

    class Meta:
        db_table = "subscription_events"
        verbose_name = _("subscription event")
        verbose_name_plural = _("subscription events")
