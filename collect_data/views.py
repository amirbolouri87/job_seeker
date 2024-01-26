from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from collect_data.serializer import TranslateEnglishTextSerializer


class TranslateEnglishText(APIView):
    def get_advertisements(self, request):
        self.advertisements = {
          "title": "Sales Manager (m/w/d) Business Development / Vertrieb",
          "company": "Ideabay GmbH",
          "city": "Munich",
          "advertise_url": "https://www.arbeitnow.com/jobs/companies/ideabay-gmbh/sales-manager-business-development-vertrieb-munich-191885",
          "datetime": "2024-01-09 17:04:04",
          "link_text": "View details for Sales Manager (m/w/d) Business Development / Vertrieb",
          "content": "Wir sind VUI (:Unser Team macht uns besonders! Wir revolutionieren den Voice-Markt, in dem wir das Erlebnis für Nutzende von Sprachassistenten zu einem Besonderen, nämlich zu einem charmismatischen Erlebnis machen. Sei dabei!AufgabenLead-Magier: Du zauberst neue Leads und füllst unsere Umsatzpipeline durch Outbound Prospecting.!",
          "pk": "sales-manager-business-development-vertrieb-munich-191885",
            "is_translate": False
        }

        pass

    def post(self, request):
        keys = ['is_translate', 'content']
        data = [self.advertisements.get(key) for key in keys]
        serializer = TranslateEnglishTextSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
