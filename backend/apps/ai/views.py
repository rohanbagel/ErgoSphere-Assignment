from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .rag import ask_question
from .serializers import AskRequestSerializer


class AskQuestionView(APIView):
    def post(self, request):
        serializer = AskRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        payload = serializer.validated_data
        result = ask_question(
            question=payload["question"],
            book_id=payload.get("book_id"),
            top_k=payload.get("top_k", 5),
        )
        return Response(result, status=status.HTTP_200_OK)
