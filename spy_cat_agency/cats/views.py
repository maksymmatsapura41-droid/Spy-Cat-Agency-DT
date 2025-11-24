from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from .models import SpyCat, Mission, Target
from .serializers import SpyCatSerializer, MissionSerializer, TargetSerializer


class SpyCatViewSet(viewsets.ModelViewSet):
    queryset = SpyCat.objects.all()
    serializer_class = SpyCatSerializer


class MissionViewSet(viewsets.ModelViewSet):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer

    def destroy(self, request, *args, **kwargs):
        mission = self.get_object()
        if mission.cat:
            return Response({"error": "Cannot delete mission assigned to a cat"}, status=status.HTTP_400_BAD_REQUEST)
        return super().destroy(request, *args, **kwargs)


class TargetUpdateView(generics.UpdateAPIView):
    queryset = Target.objects.all()
    serializer_class = TargetSerializer

    def update(self, request, *args, **kwargs):
        target = self.get_object()
        if 'notes' in request.data and (target.complete_state or target.mission.complete_state):
            return Response("Cannot update a target or notes if the target or mission is completed.")
        return super().update(request, *args, **kwargs)
