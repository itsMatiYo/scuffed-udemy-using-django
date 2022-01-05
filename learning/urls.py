from django.contrib import admin
from django.urls import path
from django.urls.conf import include

urlpatterns = [
    path("admin/", admin.site.urls),
    # * Authentication
    path("auth/", include("authentication.urls")),
    # * Users
    path("users/", include("users.urls")),
    # * Wallet
    path("wallet/", include("wallet.urls")),
    path("creditcard/", include("wallet_creditcard.urls")),
    path("locked/", include("wallet_locked.urls")),
    path("packet/", include("wallet_packet.urls")),
    path("part/", include("wallet_part.urls")),
    path("payment/", include("wallet_payment.urls")),
    path("transaction/", include("wallet_transaction.urls")),
    path("withdrawal/", include("wallet_withdrawal.urls")),
    # * Chat
    path("chat/", include("chat.urls")),
    # temporary auth
    path("course/", include("course.urls")),
    path("posts/", include("posts_api.urls")),
    # Mail
    path("mail/", include("Mail.urls")),
    path("", include("lapi.urls")),
]
