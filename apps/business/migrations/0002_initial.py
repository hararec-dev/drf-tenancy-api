# Generated by Django 5.2.3 on 2025-06-30 08:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("business", "0001_initial"),
        ("tenancies", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="planversionhistory",
            name="changed_by_user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name="changed by",
            ),
        ),
        migrations.AddField(
            model_name="planversionhistory",
            name="plan",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="business.plan",
                verbose_name="plan",
            ),
        ),
        migrations.AddField(
            model_name="planversionhistory",
            name="plan_price",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="business.planprice",
                verbose_name="plan price",
            ),
        ),
        migrations.AddField(
            model_name="subscription",
            name="plan",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to="business.plan",
                verbose_name="plan",
            ),
        ),
        migrations.AddField(
            model_name="subscription",
            name="plan_price",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to="business.planprice",
                verbose_name="plan price",
            ),
        ),
        migrations.AddField(
            model_name="subscription",
            name="tenant",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="tenancies.tenant",
                verbose_name="tenant",
            ),
        ),
        migrations.AddField(
            model_name="subscriptiondiscount",
            name="coupon",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.RESTRICT,
                related_name="subscription_discounts",
                to="business.coupon",
                verbose_name="coupon",
            ),
        ),
        migrations.AddField(
            model_name="subscriptiondiscount",
            name="subscription",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="discounts",
                to="business.subscription",
                verbose_name="subscription",
            ),
        ),
        migrations.AddField(
            model_name="subscriptionevent",
            name="subscription",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="business.subscription",
                verbose_name="subscription",
            ),
        ),
        migrations.AddIndex(
            model_name="creditledger",
            index=models.Index(
                fields=["tenant", "-created_at"], name="idx_cred_led_ten_created_at"
            ),
        ),
        migrations.AlterUniqueTogether(
            name="planfeature",
            unique_together={("plan", "feature")},
        ),
        migrations.AlterUniqueTogether(
            name="planprice",
            unique_together={("plan", "billing_period", "currency")},
        ),
        migrations.AddIndex(
            model_name="featuretier",
            index=models.Index(fields=["feature"], name="idx_feature_tiers_feature_id"),
        ),
        migrations.AddIndex(
            model_name="featuretier",
            index=models.Index(
                fields=["plan_price"], name="idx_feat_tier_plan_price_id"
            ),
        ),
        migrations.AddIndex(
            model_name="subscription",
            index=models.Index(fields=["tenant"], name="idx_subscriptions_tenant_id"),
        ),
        migrations.AddIndex(
            model_name="subscription",
            index=models.Index(fields=["plan"], name="idx_subscriptions_plan_id"),
        ),
        migrations.AddIndex(
            model_name="subscription",
            index=models.Index(fields=["status"], name="idx_subscriptions_status"),
        ),
        migrations.AddIndex(
            model_name="subscriptiondiscount",
            index=models.Index(fields=["subscription"], name="idx_sub_disc_sub_id"),
        ),
    ]
