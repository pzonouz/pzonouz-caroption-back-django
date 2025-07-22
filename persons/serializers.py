from rest_framework.serializers import ModelSerializer

from persons.models import Person


class PersonSeriliazer(ModelSerializer):
    class Meta:
        model = Person
        fields = "__all__"
