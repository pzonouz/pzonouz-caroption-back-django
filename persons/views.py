from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from persons.models import Person
from persons.serializers import PersonSeriliazer


class PersonsViewset(ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Person.objects.all()
    serializer_class = PersonSeriliazer
    ordering = ("lastname",)
