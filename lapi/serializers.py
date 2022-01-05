
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from course.models import Ticket4Seminar
from lapi.models import Attrib, Category, CompanyInfo, Media


class MediaSerializerUpdate(ModelSerializer):
    class Meta:
        model = Media
        fields = '__all__'


class MediaSerializer(ModelSerializer):
    class Meta:
        model = Media
        fields = '__all__'
        extra_kwargs = {
            'approved': {'read_only': True}
        }

    def validate(self, attrs):
        course = attrs.get('course')
        seminar = attrs.get('seminar')
        category = attrs.get('category')
        post = attrs.get('post')
        if category and not(course) and not(seminar):
            return attrs
        elif course and not(category) and not(seminar):
            return attrs
        elif seminar and not(course) and not(category):
            return attrs
        elif post:
            return attrs
        else:
            raise serializers.ValidationError(
                'You can only submit one foreignkey')


class MediaSerializerUpdate(ModelSerializer):
    class Meta:
        model = Media
        exclude = ['seminar', 'course', 'post']


class MediaSerializerUpdate4Admin(ModelSerializer):
    class Meta:
        model = Media
        fields = '__all__'


class CategoryListSerializer(ModelSerializer):
    medias = serializers.PrimaryKeyRelatedField(read_only=True, many=True)

    class Meta:
        model = Category
        exclude = ('commission', 'commission_adviser',)


class CategoryAdviserSerializer(ModelSerializer):
    medias = serializers.PrimaryKeyRelatedField(read_only=True, many=True)

    class Meta:
        model = Category
        exclude = ('commission', )


class CategoryTeacherSerializer(ModelSerializer):
    medias = serializers.PrimaryKeyRelatedField(read_only=True, many=True)

    class Meta:
        model = Category
        exclude = ('commission_adviser', )


class CategorySerializer(ModelSerializer):
    medias = serializers.PrimaryKeyRelatedField(read_only=True, many=True)

    attribs = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True)

    class Meta:
        model = Category
        fields = '__all__'
        extra_kwargs = {
            'level': {'read_only': True}
        }

    def validate_commission(self, data):
        if int(data) > 0 and int(data) < 101:

            return data
        else:
            raise serializers.ValidationError(
                {'commission': 'The value is not between 0 and 100'})

    def validate_parent(self, data):
        try:
            parent_level = data.level
            if parent_level >= 4:
                raise serializers.ValidationError(
                    'level can\'t be more than 4')
            return data
        except:
            pass


class CategorySerializerPatch(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        extra_kwargs = {
            'parent': {'read_only': True},
            'level': {'read_only': True}
        }

    def validate_commission(self, data):
        if data > 0 and data < 101:
            return data
        else:
            raise serializers.ValidationError(
                {'commission': 'The value is not between 0 and 100'})


class AttribSerializer(ModelSerializer):
    class Meta:
        model = Attrib
        fields = '__all__'

    def validate(self, attrs):
        # check if category has children or not
        category = attrs.get('category')
        if category.subs.exists():
            raise serializers.ValidationError(
                {'category': 'this category has children'})
        else:
            return attrs


class AttribSerializerPatch(ModelSerializer):
    class Meta:
        model = Attrib
        fields = '__all__'
        extra_kwargs = {
            'category': {'read_only': True}
        }


class Ticket4SeminarSerializer(ModelSerializer):
    class Meta:
        model = Ticket4Seminar
        fields = '__all__'


class CompanyInfoSerializer(ModelSerializer):
    class Meta:
        model = CompanyInfo
        fields = '__all__'
