from django.conf import settings
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView


class ImageUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        file = request.FILES.get("image")
        if not file:
            return Response(
                {"error": "No image uploaded"}, status=status.HTTP_400_BAD_REQUEST
            )

        from django.core.files.storage import default_storage

        path = default_storage.save(f"uploads/{file.name}", file)
        return Response({"url": f"{settings.MEDIA_URL}{path}"})
