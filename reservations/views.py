from rest_framework import viewsets, permissions, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Reservation
from .serializers import ReservationSerializer
from foods.models import Food
from drf_spectacular.utils import extend_schema

class StatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=['completed', 'cancelled', 'pending'])

class ReservationViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if not self.request or self.request.user.is_anonymous:
            return Reservation.objects.none()
        if self.request.user.is_staff:
            return Reservation.objects.all()
        return Reservation.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        food_id = request.data.get('food_id')
        if not food_id:
            return Response({"error": "food_id required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            food = Food.objects.get(id=food_id)
        except Food.DoesNotExist:
            return Response({"error": "Food not found"}, status=status.HTTP_404_NOT_FOUND)

        reservation = Reservation.objects.create(
            user=request.user,
            food=food
        )
        serializer = self.get_serializer(reservation)
        return Response({
            "message": "Ovqat muvaffaqiyatli band qilindi",
            "reservation": serializer.data
        }, status=status.HTTP_201_CREATED)

    @extend_schema(request=StatusUpdateSerializer, responses={200: ReservationSerializer})
    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAdminUser])
    def change_status(self, request, pk=None):
        reservation = self.get_object()
        new_status = request.data.get('status')
        
        if new_status not in ['completed', 'cancelled', 'pending']:
            return Response(
                {"error": "Noto'g'ri status. Faqat 'completed' yoki 'cancelled' qabul qilinadi"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        reservation.status = new_status
        reservation.save()
        return Response({
            "message": f"Buyurtma statusi muvaffaqiyatli '{new_status}' holatiga o'zgartirildi",
            "reservation": self.get_serializer(reservation).data
        }, status=status.HTTP_200_OK)