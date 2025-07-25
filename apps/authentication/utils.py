from apps.audit.models import AuditLog, SensitiveAccessLog
from apps.billing.models import (
    CreditTransaction,
    Invoice,
    Payment,
    PaymentMethod,
    UsageRecord,
)
from apps.business.models import (
    Coupon,
    CreditLedger,
    Feature,
    FeatureTier,
    Plan,
    PlanPrice,
    Subscription,
    SubscriptionDiscount,
)
from apps.tenancies.models import (
    Department,
    Tenant,
    TenantAuditPolicy,
    TenantConfiguration,
)
from apps.users.models import User

from .models import Invitation, Role


def get_permission_to_model_map():
    permission_to_model_map = {
        "add_tenant": Tenant,
        "change_tenant": Tenant,
        "delete_tenant": Tenant,
        "view_tenant": Tenant,
        "suspend_tenant": Tenant,
        "reactivate_tenant": Tenant,
        "access_all_tenants_data": Tenant,
        "change_tenantconfiguration": TenantConfiguration,
        "view_tenantconfiguration": TenantConfiguration,
        "change_tenantauditpolicy": TenantAuditPolicy,
        "view_tenantauditpolicy": TenantAuditPolicy,
        "impersonate_tenant_user": User,
        "add_department": Department,
        "change_department": Department,
        "delete_department": Department,
        "view_department": Department,
        "add_plan": Plan,
        "change_plan": Plan,
        "delete_plan": Plan,
        "view_plan": Plan,
        "add_feature": Feature,
        "change_feature": Feature,
        "delete_feature": Feature,
        "view_feature": Feature,
        "add_planprice": PlanPrice,
        "change_planprice": PlanPrice,
        "delete_planprice": PlanPrice,
        "view_planprice": PlanPrice,
        "add_featuretier": FeatureTier,
        "change_featuretier": FeatureTier,
        "delete_featuretier": FeatureTier,
        "view_featuretier": FeatureTier,
        "add_subscription": Subscription,
        "change_subscription": Subscription,
        "delete_subscription": Subscription,
        "view_subscription": Subscription,
        "override_tenant_subscription": Subscription,
        "add_coupon": Coupon,
        "change_coupon": Coupon,
        "delete_coupon": Coupon,
        "view_coupon": Coupon,
        "add_subscriptiondiscount": SubscriptionDiscount,
        "delete_subscriptiondiscount": SubscriptionDiscount,
        "view_subscriptiondiscount": SubscriptionDiscount,
        "add_user": User,
        "change_user": User,
        "delete_user": User,
        "view_user": User,
        "add_role": Role,
        "change_role": Role,
        "delete_role": Role,
        "view_role": Role,
        "assign_role": Role,
        "add_invitation": Invitation,
        "change_invitation": Invitation,
        "delete_invitation": Invitation,
        "view_invitation": Invitation,
        "add_invoice": Invoice,
        "change_invoice": Invoice,
        "delete_invoice": Invoice,
        "view_invoice": Invoice,
        "download_invoice": Invoice,
        "add_payment": Payment,
        "change_payment": Payment,
        "delete_payment": Payment,
        "view_payment": Payment,
        "add_paymentmethod": PaymentMethod,
        "change_paymentmethod": PaymentMethod,
        "delete_paymentmethod": PaymentMethod,
        "view_paymentmethod": PaymentMethod,
        "add_credittransaction": CreditTransaction,
        "view_credittransaction": CreditTransaction,
        "add_creditledger": CreditLedger,
        "view_creditledger": CreditLedger,
        "add_usagerecord": UsageRecord,
        "view_usagerecord": UsageRecord,
        "view_auditlog": AuditLog,
        "export_auditlog": AuditLog,
        "view_sensitiveaccesslog": SensitiveAccessLog,
        "view_platform_dashboard": Tenant,
        "manage_deployments": Tenant,
        "run_data_migrations": Tenant,
        "toggle_feature_flags": Tenant,
        "view_global_financial_reports": Invoice,
        "add_supportticket": User,
        "view_supportticket": User,
        "manage_knowledgebase": User,
    }
    return permission_to_model_map


def get_group_permissions():
    group_permissions = {
        "PlatformAdmin": [
            "add_tenant",
            "change_tenant",
            "delete_tenant",
            "view_tenant",
            "suspend_tenant",
            "reactivate_tenant",
            "access_all_tenants_data",
            "override_tenant_subscription",
            "add_plan",
            "change_plan",
            "delete_plan",
            "view_plan",
            "add_feature",
            "change_feature",
            "delete_feature",
            "view_feature",
            "add_planprice",
            "change_planprice",
            "delete_planprice",
            "view_planprice",
            "add_featuretier",
            "change_featuretier",
            "delete_featuretier",
            "view_featuretier",
            "add_coupon",
            "change_coupon",
            "delete_coupon",
            "view_coupon",
            "impersonate_tenant_user",
            "manage_deployments",
            "run_data_migrations",
            "toggle_feature_flags",
            "view_platform_dashboard",
            "view_global_financial_reports",
            "view_auditlog",
            "export_auditlog",
            "view_sensitiveaccesslog",
            "add_creditledger",
        ],
        "PlatformSupport": [
            "view_tenant",
            "view_subscription",
            "view_invoice",
            "view_payment",
            "view_auditlog",
            "add_supportticket",
            "view_supportticket",
            "manage_knowledgebase",
        ],
        "TenantOwner": [
            "change_tenantconfiguration",
            "view_tenantconfiguration",
            "change_tenantauditpolicy",
            "view_tenantauditpolicy",
            "add_department",
            "change_department",
            "delete_department",
            "view_department",
            "view_plan",
            "view_coupon",
            "add_subscriptiondiscount",
            "delete_subscriptiondiscount",
            "view_subscriptiondiscount",
            "change_subscription",
            "view_subscription",
            "add_user",
            "change_user",
            "delete_user",
            "view_user",
            "add_role",
            "change_role",
            "delete_role",
            "view_role",
            "assign_role",
            "add_invitation",
            "delete_invitation",
            "view_invitation",
            "view_invoice",
            "download_invoice",
            "view_payment",
            "add_paymentmethod",
            "change_paymentmethod",
            "delete_paymentmethod",
            "view_paymentmethod",
            "view_creditledger",
            "view_usagerecord",
            "view_auditlog",
            "add_supportticket",
            "view_supportticket",
        ],
        "TenantAdmin": [
            "change_tenantconfiguration",
            "view_tenantconfiguration",
            "add_department",
            "change_department",
            "delete_department",
            "view_department",
            "add_user",
            "change_user",
            "delete_user",
            "view_user",
            "add_role",
            "change_role",
            "view_role",
            "assign_role",
            "add_invitation",
            "delete_invitation",
            "view_invitation",
            "view_auditlog",
            "add_supportticket",
            "view_supportticket",
        ],
        "BillingManager": [
            "view_plan",
            "view_coupon",
            "add_subscriptiondiscount",
            "delete_subscriptiondiscount",
            "view_subscriptiondiscount",
            "view_subscription",
            "view_invoice",
            "download_invoice",
            "view_payment",
            "add_paymentmethod",
            "change_paymentmethod",
            "delete_paymentmethod",
            "view_paymentmethod",
            "view_creditledger",
        ],
        "StandardUser": [
            "view_user",
            "add_usagerecord",
            "add_supportticket",
            "view_supportticket",
        ],
    }
    return group_permissions
