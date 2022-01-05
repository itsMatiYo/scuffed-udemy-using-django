import jwt
import json
import datetime

from decouple import config
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from lapi import models as md
from lapi.serializers import (
    AttribSerializer,
    CategoryListSerializer,
    CategorySerializer,
    CompanyInfoSerializer,
)

tokenAdmin = jwt.encode(
    {
        "id": "6e4818fb-4000-47be-8d05-1510e1efdff2",
        "role": "admin",
        "service": config("SERVICE_ID"),
        "packet_id": "dded429f-852b-47ca-aafd-c0285350a5a7",
        "username": "learning_admin",
        "wallet_id": "6e4818fb-4000-47be-8d05-1510e1efdff2",
        "iat": datetime.datetime.now(),
        "exp": datetime.datetime.now() + datetime.timedelta(days=1),
    },
    config("AUTH_SECRET_KEY"),
    algorithm="HS256",
)


class InfoCompanyTest(APITestCase):
    def test_admin_create(self):
        res = self.client.post(
            "/info/",
            data={
                "name": "company",
                "address": "test address",
            },
            HTTP_AUTHORIZATION=tokenAdmin,
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_get(self):
        test = md.CompanyInfo.objects.create(name="company", address="test address")
        res = self.client.get("/info/1/")
        self.assertEqual(json.loads(res.content), CompanyInfoSerializer(test).data)

    def test_update(self):
        md.CompanyInfo.objects.create(name="company", address="test address")
        res = self.client.patch(
            "/info/1/",
            data={
                "name": "another name",
                "address": "another address",
            },
            HTTP_AUTHORIZATION=tokenAdmin,
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete(self):
        md.CompanyInfo.objects.create(name="company", address="test address")
        res = self.client.delete(
            "/info/1/",
            HTTP_AUTHORIZATION=tokenAdmin,
        )
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)


class CategoryTest(APITestCase):
    def setUp(self) -> None:
        self.par1 = md.Category.objects.create(
            name="top category 1",
            level=0,
            commission=10,
            commission_adviser=7,
            price_adviser=5,
            description="test desc",
        )
        md.Category.objects.create(
            name="top category 2",
            level=0,
            commission=7,
            commission_adviser=7,
            price_adviser=5,
            description="test desc",
        )
        self.car2 = md.Category.objects.create(
            name="category 1",
            level=1,
            parent=self.par1,
            commission=10,
            commission_adviser=7,
            price_adviser=5,
            description="test desc",
        )

    def test_create(self):
        res = self.client.post(
            "/category/",
            data={
                "name": "test 1",
                "parent": f"{self.par1.pk}",
                "description": "desc",
                "price_adviser": "12",
                "commission_adviser": "15",
                "commission": "5",
            },
            HTTP_AUTHORIZATION=tokenAdmin,
        )
        self.assertEqual(status.HTTP_201_CREATED, res.status_code)

    def test_get_all(self):
        res = self.client.get(
            "/category/",
            HTTP_AUTHORIZATION=tokenAdmin,
            content_type="application/json",
        )
        categories = md.Category.objects.all()
        serializer = CategoryListSerializer(categories, many=True)
        self.assertEqual(serializer.data, json.loads(res.content)["results"])

    def test_get(self):
        res = self.client.get(
            f"/category/{self.par1.pk}/",
            HTTP_AUTHORIZATION=tokenAdmin,
        )
        serializer = CategorySerializer(self.par1)
        self.assertEqual(serializer.data, json.loads(res.content))

        res = self.client.get(
            f"/category/{self.par1.pk}/",
        )
        serializer = CategoryListSerializer(self.par1)
        self.assertEqual(serializer.data, json.loads(res.content))

    def test_admin_delete(self):
        res = self.client.delete(
            f"/category/{self.car2.pk}/",
            HTTP_AUTHORIZATION=tokenAdmin,
        )
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete(self):
        res = self.client.delete(
            f"/category/{self.car2.pk}/",
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AttribTest(APITestCase):
    def setUp(self) -> None:
        self.cat1 = md.Category.objects.create(
            name="top category 1",
            level=0,
            commission=7,
            commission_adviser=7,
            price_adviser=5,
            description="test desc",
        )
        md.Category.objects.create(
            name="top category 2",
            level=0,
            commission=7,
            commission_adviser=7,
            price_adviser=5,
            description="test desc",
        )
        self.att1 = md.Attrib.objects.create(
            name="python",
            category=self.cat1,
        )

    def test_create(self):
        res = self.client.post(
            "/attrib/",
            data={"name": "js", "category": f"{self.cat1.pk}"},
            HTTP_AUTHORIZATION=tokenAdmin,
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_get_all(self):
        res = self.client.get("/attrib/")
        attribs = md.Attrib.objects.all()
        serializer = AttribSerializer(attribs, many=True)
        self.assertEqual(serializer.data, json.loads(res.content)["results"])

    def test_get(self):
        res = self.client.get(f"/attrib/{self.att1.pk}/")
        serializer = AttribSerializer(self.att1)
        self.assertEqual(serializer.data, json.loads(res.content))

    def test_delete(self):
        res = self.client.delete(
            f"/attrib/{self.att1.pk}/",
            HTTP_AUTHORIZATION=tokenAdmin,
        )
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
