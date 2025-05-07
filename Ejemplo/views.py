from django.shortcuts import render
from rest_framework import generics, viewsets
from .models import Producto
from .serializers import ProductoSerializer

# Vista para obtener todos los productos (GET)
class ProductoListView(generics.ListCreateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

    # Aquí se define el método GET para obtener los productos.
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    # Aquí se define el método POST para crear un nuevo producto.
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

# ViewSet para productos (más adecuado para DRF router)
class ProductoViewSet(viewsets.ModelViewSet):
    """
    API endpoint para ver y editar productos
    """
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
