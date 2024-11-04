import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Payment
from .serializers import PaymentSerializer


class PayKeeperAPIView(APIView):
    def post(self, request):
        data = request.POST.dict()

        payload = {
            "amount": data.get("amount"),
            "order_id": data.get("order_id"),
            "currency": "RUB",
            "success_url": "http://127.0.0.1:8000/succes",
            "fail_url": "http://127.0.0.1:8000/fail",
        }

        url = "https://api.paykeeper.ru/payment"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.PAYKEEPER_API_TOKEN}"
        }
        try:
            response = requests.post(url, headers=headers, json=payload)
            response_data = response.json()
            if response.status_code == 200:
                payment_link = response_data.get("payment_url")
                return Response({"payment_url": payment_link}, status=status.HTTP_200_OK)
            else:
                return Response({'error:' "Некорректный запрос"}, status=response.status_code)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class PayKeeperNotificationAPIView(APIView):
    def post(self, request):
        order_id = request.data.get('order_id')
        payment_status = request.data.get('status')

        try:
            payment = Payment.objects.get(order_id=order_id)
            payment.status = payment_status
            payment.save()
            return Response(status=status.HTTP_200_OK)
        except Payment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)