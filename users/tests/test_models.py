from django.test import TestCase
from users import models as md
from lapi.models import Category


class WalletTest(TestCase):
    def test_wallet_create(self):
        self.wallet1 = md.Wallet.objects.create(id="First id of wallet")
        self.wallet2 = md.Wallet.objects.create(id="2nd id of wallet")

        self.assertEqual(str(self.wallet1), "First id of wallet")
        self.assertEqual(str(self.wallet2), "2nd id of wallet")


class TeacherTest(TestCase):
    def setUp(self) -> None:
        self.wallet1 = md.Wallet.objects.create(id="First id of wallet")
        self.wallet2 = md.Wallet.objects.create(id="2nd id of wallet")
        self.document = md.Document.objects.create(
            reason="Test reason",
            status="ap",
        )
        self.teacher = md.Teacher.objects.create(
            wallet=self.wallet1,
            approved=True,
            document=self.document,
        )

    def test_get(self):

        self.assertEqual(str(self.teacher), "First id of wallet")
        self.assertEqual(self.teacher.approved, True)
        self.assertEqual(self.document.status, "ap")


class AdviserTest(TestCase):
    def setUp(self) -> None:
        self.category = Category.objects.create(name="Name of Cat", level=0)
        wallet = md.Wallet.objects.create(id="Adviser wallet id")
        self.adviser = md.Adviser.objects.create(
            wallet=wallet, category=self.category, approved=True
        )

    def test_get(self):
        self.assertEqual(str(self.adviser), "Adviser wallet id")
        self.assertEqual(self.adviser.category, self.category)
