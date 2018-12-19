from winereviews.models import *
from api.serializers import WineSerializer
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response


class WineViewSet(viewsets.ModelViewSet):
    """
    This ViewSet provides both 'list' and 'detail' views.
    """
    queryset = Wine.objects.select_related().order_by('wine_name')
    serializer_class = WineSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def delete(self, request, pk, format=None):
        site = self.get_object(pk)
        self.perform_destroy(self, site)

        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()