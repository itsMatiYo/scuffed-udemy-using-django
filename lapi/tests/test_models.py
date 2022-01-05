from django.test import TestCase

from lapi import models as md
from users.models import Adviser, Wallet


class TestMedia(TestCase):
    def setUp(self) -> None:
        self.media1 = md.Media.objects.create(
            alt="media 1 alt",
            approved=True,
            file=None,
            seo={"test": "ok"},
        )

    def test_get(self):
        self.assertEqual(self.media1.alt, "media 1 alt")
        self.assertEqual(self.media1.approved, True)


class TestCategoryAndAttrib(TestCase):
    def setUp(self) -> None:
        self.parent_category1 = md.Category.objects.create(
            name="Parent 1",
            level=0,
            description="Description of Test Category",
            seo={"test": "ok"},
        )

        self.category2 = md.Category.objects.create(
            name="Parent 2",
            commission=10,
            level=1,
            commission_adviser=20,
            price_adviser=300,
            parent=self.parent_category1,
            seo={"test": "ok"},
            description="Description of Test Category",
        )

        self.attrib1 = md.Attrib.objects.create(
            name="name of attrib 1", category=self.category2
        )

    def test_get_category(self):
        self.assertEqual(self.category2.parent, self.parent_category1)
        self.assertEqual(self.category2.name, "Parent 2")
        self.assertEqual(self.parent_category1.name, "Parent 1")

    def test_str_attrib(self):
        self.assertEqual(str(self.attrib1), "name of attrib 1 of Parent 2")


class TestTicket4Adviser(TestCase):
    def setUp(self) -> None:
        self.wallet_adviser = Wallet.objects.create(id="wallet adviser id")
        self.adviser = Adviser.objects.create(wallet=self.wallet_adviser, approved=True)

    def test_get(self):
        self.assertEqual(str(self.adviser), "wallet adviser id")
        self.assertEqual(self.adviser.approved, True)


class TestCompanyInfo(TestCase):
    def test_create(self):
        cm = md.CompanyInfo.objects.create(
            name="Test name",
            address="Address of company",
            phonenums={"home": "093321123"},
        )
        self.assertEqual(cm.name, "Test name")
        self.assertEqual(cm.address, "Address of company")
