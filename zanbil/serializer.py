from rest_framework import serializers
from zanbil.models import Business, Service, TimeTable, Sans, Category, Review, User, Reserve, File, Transaction


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = [
            'id',
            'address',
            'business',
            'service',
            'message'
        ]


class ServiceSerializer(serializers.ModelSerializer):
    pictures = FileSerializer(many=True)

    class Meta:
        model = Service
        fields = [
            'id',
            'business',
            'name',
            'fee',
            'rating',
            'timetable',
            'description',
            'pictures',
            'is_protected',
            'cancellation_range'
        ]


class SansSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sans
        fields = [
            'id',
            'start_time',
            'end_time',
            'timetable_id',
            'weekday',
            'capacity',
        ]


class BusinessSerializer(serializers.ModelSerializer):
    services = ServiceSerializer(many=True)
    pictures = FileSerializer(many=True)

    class Meta:
        model = Business
        fields = [
            'id',
            'owner_id',
            'name',
            'phone_number',
            'email',
            'address',
            'services',
            'description',
            'category_id',
            'pictures',
        ]


class BusinessSimpleSerializer(serializers.ModelSerializer):
    id = serializers.models.fields.BooleanField()
    pictures = FileSerializer(many=True)
    class Meta:
        model = Business
        fields = [
            'id',
            'owner_id',
            'name',
            'phone_number',
            'email',
            'address',
            'description',
            'category_id',
            'pictures'
        ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'name',
        ]


class TimetableSimpleSerializer(serializers.ModelSerializer):
    sanses = SansSerializer(many=True)

    class Meta:
        model = TimeTable
        fields = [
            'id',
            'name',
        ]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'username',
            'email',
            'phone_number',
        ]



class UsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
        ]


class ReserveSerializer(serializers.ModelSerializer):
    service = ServiceSerializer()
    sans = SansSerializer()
    class Meta:
        model = Reserve
        fields = [
            'date',
            'description',
            'service',
            'sans',
            'is_cancelled',
        ]


class ReviewSerializer(serializers.ModelSerializer):
    user = UsernameSerializer()

    class Meta:
        model = Review
        fields = [
            'id',
            'user',
            'description',
            'rating',
        ]


class TransactionSerializer(serializers.ModelSerializer):
    reserve = ReserveSerializer()

    class Meta:
        model = Transaction
        fields = [
            'id',
            'reserve',
            'paidAt',
            'amount'

        ]
class FileSerializer(serializers.ModelSerializer):
    reserve = ReserveSerializer()
    business = BusinessSimpleSerializer()
    service = ServiceSerializer()
    class Meta:
        model = Transaction
        fields = [
            'id',
            'address',
            'business',
            'service',
            'message'
        ]


class ServiceSearchSerializer(serializers.ModelSerializer):
    business = BusinessSimpleSerializer()
    pictures = FileSerializer()
    class Meta:
        model = Service
        fields = [
            'id',
            'business',
            'name',
            'fee',
            'rating',
            'timetable',
            'description',
            'cancellation_range',
            'pictures',
        ]
