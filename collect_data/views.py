import googletrans
from googletrans import Translator, LANGUAGES
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from collect_data.serializer import TranslateEnglishTextSerializer, IsEnglishTextSerializer

class IsEnglishTextView(APIView):
    def post(self, request):
        serializer = IsEnglishTextSerializer(data=request.data)

        if serializer.is_valid():
            content = serializer.validated_data['content']
            paragraphs = content.split('\n')
            for paragraph in paragraphs:
                translator = Translator()
                result = translator.detect(paragraph)
                language_code = result.lang
                if language_code != 'en':
                    return Response(False, status=status.HTTP_200_OK)
                return Response(True, status=status.HTTP_200_OK)


class TranslateEnglishText(APIView):

    def _translate(self, content):
        translate_content = ""
        translator = Translator()
        paragraphs = content.split('\n')
        for paragraph in paragraphs:
            if self._check_germany(paragraph):
                # print(paragraph)
                translate_paragraph = translator.translate(paragraph, src='de', dest='en').text
                translate_content += str(translate_paragraph)
        return translate_content

    @staticmethod
    def _check_germany(content):
        paragraphs = content.split('\n')
        for paragraph in paragraphs:
            translator = Translator()
            result = translator.detect(paragraph)
            language_code = result.lang
            if language_code == 'de':
                return True

            return False

    def post(self, request, *args, **kwargs):
        serializer = TranslateEnglishTextSerializer(data=request.data)

        if serializer.is_valid():
            content = serializer.validated_data['content']

            # Perform the translation logic here
            translated_content = self._translate(content)

            response_data = {
                "content":translated_content,
                "is_translated":True
            }

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
