from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import exceptions, generics, mixins, serializers, viewsets
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.permission import (
    AdminPermission,
    AdviserPermission,
    AdviserPermissionUnApproved,
    ReadOnly,
    StudentPermission,
    TeacherPermission,
    TeacherPermissionUnApproved,
)
from authentication.utils import (
    get_my_object,
    get_token,
    get_wallet,
    is_it_admin,
    is_it_adviser,
    is_it_teacher,
)
from course.models import Course, Seminar, Ticket4Seminar
from lapi.models import Ticket4Adviser
from users.models import Adviser, Document, Student, Teacher
from users.serializers import (
    Admin_Document_Serializer,
    AdviserCategoryPatch,
    Document_Serializer,
    StudentSerializer,
    StudentSerializerAdmin,
    TeacherCategoryPatch,
    TicketSerializer,
)
from wallet_creditcard.utils import spend_from_card, spend_from_card_data
from wallet_part.utils import (
    create_part,
    create_part_data,
    spend_from_part,
    spend_part_data,
)


class Accept_Seminar(APIView):
    permission_classes = [TeacherPermission]

    def get(self, request, *args, **kwargs):
        ticket = get_object_or_404(Ticket4Seminar, id=kwargs["student_uuid"])

        # ? spend from part and return response data
        amount = ticket.course.price
        section_wallet_id = ticket.course.teacher.wallet.id
        section_percent = ticket.course.attrib.category.commission
        data_spend_from_part = spend_part_data(
            amount, section_wallet_id, section_percent
        )
        data = spend_from_part(ticket.part_id, data=data_spend_from_part)

        # ? Add student to course
        # ticket.course.students.add(ticket.student)
        # this part is done in buy seminar

        return Response({"data": data}, status=201)


class Buy_Seminar(APIView):
    permission_classes = [StudentPermission]

    def post(self, request, *args, **kwargs):

        # * Take a class's obj
        target_class = get_object_or_404(Seminar, id=kwargs["class_id"])

        if (
            target_class.capacity == target_class.students.count()
            or target_class.capacity > target_class.students.count()
        ):
            raise exceptions.ValidationError(detail="class is full", code=400)
        if (
            timezone.now() < target_class.starting_time
            and timezone.now() > target_class.starting_seminar
        ):
            raise exceptions.ValidationError(detail="time expired", code=400)

        # * Take a student's obj with Token
        student = get_my_object(request, Student)

        # ! Student cant register twice
        if student not in target_class.students.all():

            # * Get Token & Wallet_id from request :
            token = get_token(request)
            wallet = get_wallet(token)

            # ? create part and return part id
            data_create_part = create_part_data(wallet.id, amount=target_class.price)
            part_id = create_part(data=data_create_part)

            # ? Create Ticket
            ticket = Ticket4Seminar.objects.create(
                course=target_class, student=student, part_id=part_id
            )

            target_class.waiting_students.add(student)

            return Response({"part_id": part_id, "uuid": ticket.id}, status=201)

        else:
            raise exceptions.ValidationError(
                detail="you have already registered", code=400
            )


class Buy_Class(APIView):
    permission_classes = [StudentPermission]

    def post(self, request, *args, **kwargs):

        # * Take a class's obj
        target_class = get_object_or_404(Course, id=kwargs["class_id"])

        # * Take a student's obj with Token
        student = get_my_object(request, Student)

        # ! Student cant register twice
        if student not in target_class.students.all():

            # * Get Token & Wallet_id from request :
            token = get_token(request)
            wallet = get_wallet(token)

            # ? create part and return part id
            data_create_part = create_part_data(wallet.id, amount=target_class.price)
            part_id = create_part(data=data_create_part)

            # ? spend from part and return response data
            amount = target_class.price
            section_wallet_id = target_class.teacher.wallet.id
            section_percent = target_class.attrib.category.commission
            data_spend_from_part = spend_part_data(
                amount, section_wallet_id, section_percent
            )
            data = spend_from_part(part_id, data=data_spend_from_part)

            # ? Add student to course
            target_class.waiting_students.add(student)

            return Response({"data": data}, status=201)

        else:
            raise exceptions.ValidationError(
                detail="you have already registered", code=400
            )


class Buy_Adviser(APIView):
    permission_classes = [StudentPermission]

    def post(self, request, *args, **kwargs):

        # * Take a adviser's obj
        target_adviser = get_object_or_404(Adviser, id=kwargs["adviser_id"])
        # * Take a student's obj with Token
        student = get_my_object(request, Student)

        # * Get Token & Wallet_id from request :
        token = get_token(request)
        wallet = get_wallet(token)

        # ? create part and return part id
        data_create_part = create_part_data(
            wallet.id, amount=target_adviser.category.price_adviser
        )
        part_id = create_part(data=data_create_part)

        # ? spend from part and return response data
        amount = target_adviser.category.price_adviser
        section_wallet_id = target_adviser.wallet.id
        section_percent = target_adviser.category.commission_adviser
        data_spend_from_part = spend_part_data(
            amount, section_wallet_id, section_percent
        )
        data = spend_from_part(part_id, data=data_spend_from_part)

        # ? Create Ticket
        Ticket4Adviser.objects.create(buyer=student, adviser=target_adviser)

        return Response({"data": data}, status=201)


class Buy_Class_With_Card(APIView):
    permission_classes = [StudentPermission]

    def post(self, request, *args, **kwargs):

        # * Take a class's obj
        target_class = get_object_or_404(Course, id=kwargs["class_id"])

        card_type = kwargs["type"]
        cart_id = kwargs["cart_id"]

        # * Take a student's obj with Token
        student = get_my_object(request, Student)
        # ! Student cant register twice
        if student not in target_class.students.all():

            # * Get Token & Wallet_id from request :
            token = get_token(request)
            wallet = get_wallet(token)

            # ? create a data for (Spend From Card) section :
            sections_wallet_id = target_class.teacher.wallet.id
            sections_percent = target_class.attrib.category.commission
            data_spend_from_card = spend_from_card_data(
                target_class.price,
                wallet.id,
                cart_id,
                sections_wallet_id=sections_wallet_id,
                sections_percent=sections_percent,
            )

            # ! type must be ---> giftcard or creditcard
            if card_type == "giftcard":
                try:
                    password = request.data["password"]
                    data_spend_from_card["password"] = request.data["password"]
                except:
                    raise exceptions.ValidationError(
                        detail="not found password", code=404
                    )

            elif card_type != "creditcard":
                raise exceptions.ValidationError(detail="Invalid type", code=404)

            data = spend_from_card(card_type, data=data_spend_from_card)

            # ? add student to course
            target_class.waiting_students.add(student)

            return Response({"data": data}, status=201)

        else:
            raise exceptions.ValidationError(
                detail="you have already registered", code=400
            )


class Buy_Adviser_With_Card(APIView):
    permission_classes = [StudentPermission]

    def post(self, request, *args, **kwargs):

        # * Take a adviser's obj
        target_adviser = get_object_or_404(Adviser, id=kwargs["adviser_id"])

        card_type = kwargs["type"]
        cart_id = kwargs["cart_id"]

        # * Take a student's obj with Token
        student = get_my_object(request, Student)

        # * Get Token & Wallet_id from request :
        token = get_token(request)
        wallet = get_wallet(token)

        # ? create a data for (Spend From Card) section :
        sections_wallet_id = target_adviser.wallet.id
        sections_percent = target_adviser.category.commission_adviser
        data_spend_from_card = spend_from_card_data(
            target_adviser.category.price_adviser,
            wallet.id,
            cart_id,
            sections_wallet_id=sections_wallet_id,
            sections_percent=sections_percent,
        )

        # ! type must be ---> giftcard or creditcard
        if card_type == "giftcard":
            try:
                password = request.data["password"]
                data_spend_from_card["password"] = request.data["password"]
            except:
                raise exceptions.ValidationError(detail="not found password", code=404)

        elif card_type != "creditcard":
            raise exceptions.ValidationError(detail="Invalid type", code=404)

        data = spend_from_card(card_type, data=data_spend_from_card)

        # ? Create Ticket
        Ticket4Adviser.objects.create(buyer=student, adviser=target_adviser)

        return Response({"data": data}, status=201)


class User_Create_Document(generics.ListCreateAPIView):
    queryset = Document.objects.all()
    serializer_class = Document_Serializer
    permission_classes = [TeacherPermissionUnApproved | AdviserPermissionUnApproved]

    def perform_create(self, serializer):

        if self.kwargs["type"] == "adviser":
            user = get_my_object(self.request, Adviser)
        elif self.kwargs["type"] == "teacher":
            user = get_my_object(self.request, Teacher)

        if user.document == None:
            # ? create document obj :
            new_document = serializer.save()

            # ? connect user to document obj :
            user.document = new_document
            user.save()
        else:
            raise exceptions.ValidationError(detail="documents is available", code=400)

    def get_queryset(self):
        req = self.request
        if is_it_teacher(req):
            return Document.objects.filter(teacher=get_my_object(req, Teacher))
        elif is_it_adviser(req):
            return Document.objects.filter(adviser=get_my_object(req, Adviser))


class User_Update_Document(generics.UpdateAPIView):
    queryset = Document.objects.all()
    serializer_class = Document_Serializer
    permission_classes = [TeacherPermissionUnApproved | AdviserPermissionUnApproved]

    def get_object(self):
        if self.kwargs["type"] == "adviser":
            user = get_my_object(self.request, Adviser)
            obj = get_object_or_404(Document, adviser=user)

        elif self.kwargs["type"] == "teacher":
            user = get_my_object(self.request, Teacher)
            obj = get_object_or_404(Document, teacher=user)

        return obj

    def perform_update(self, serializer):
        obj = serializer.save(status="ns", reason="")


class AdminDocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    permission_classes = []
    serializer_class = Admin_Document_Serializer
    filterset_fields = ("status",)

    def list(self, request, *args, **kwargs):
        print("s")
        return super().list(request, *args, **kwargs)

    def perform_update(self, serializer):
        status = serializer.validated_data.get("status")
        doc = self.get_object()
        if status == "ap":
            if doc.teacher:
                doc.teacher.apprvoed = True
                doc.teacher.save()
            elif doc.adviser:
                doc.adviser.apprvoed = True
                doc.adviser.save()
        return super().perform_update(serializer)


class AdviserTicketList(generics.ListAPIView):
    # Adviser get own tickets
    queryset = Ticket4Adviser.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [
        AdviserPermission,
    ]

    def get(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(adviser=get_my_object(request, Adviser))
        return self.list(request, *args, **kwargs)


# user get his tickets
class StudentTicketList(generics.ListAPIView):
    queryset = Ticket4Adviser.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [
        StudentPermission,
    ]

    def get(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(buyer=get_my_object(request, Student))
        return self.list(request, *args, **kwargs)


class AdminTicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket4Adviser.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [
        AdminPermission,
    ]


class AdminAdviserViewset(viewsets.ModelViewSet):
    queryset = Adviser.objects.all()
    serializer_class = AdviserCategoryPatch
    permission_classes = [AdminPermission | ReadOnly]
    filterset_fields = ["wallet"]

    def get_queryset(self):
        if is_it_admin(self.request):
            return super().get_queryset()
        else:
            return Adviser.objects.filter(approved=True)


class AdminTeacherViewset(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherCategoryPatch
    permission_classes = [AdminPermission | ReadOnly]
    filterset_fields = ["wallet"]

    def get_queryset(self):
        if is_it_admin(self.request):
            return super().get_queryset()
        else:
            return Teacher.objects.filter(approved=True)


class AdminStudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    permission_classes = []
    filterset_fields = ["wallet"]

    def get_serializer_class(self):
        if is_it_admin(self.request):
            return StudentSerializerAdmin
        else:
            return StudentSerializer

    def retrieve(self, request, *args, **kwargs):
        self.permission_classes = []
        return super().retrieve(request, *args, **kwargs)
