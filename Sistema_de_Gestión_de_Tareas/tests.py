from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
import datetime

from .models import Lista, Tarea, Etiqueta


class ModelTestCase(TestCase):
    """Pruebas para los modelos del Sistema de Gestión de Tareas"""
    
    def setUp(self):
        """Configuración inicial para las pruebas"""
        # Crear etiquetas
        self.etiqueta1 = Etiqueta.objects.create(nombre="importante", color="#FF0000")
        self.etiqueta2 = Etiqueta.objects.create(nombre="urgente", color="#0000FF")
        
        # Crear lista
        self.lista = Lista.objects.create(
            nombre="Trabajo",
            descripcion="Tareas de trabajo"
        )
        
        # Crear tarea
        self.tarea = Tarea.objects.create(
            titulo="Preparar informe",
            descripcion="Informe mensual de ventas",
            lista=self.lista,
            prioridad=3,
            fecha_vencimiento=timezone.now().date() + datetime.timedelta(days=3)
        )
        
        # Asignar etiquetas
        self.tarea.etiquetas.add(self.etiqueta1)
    
    def test_lista_creation(self):
        """Probar la creación correcta de una lista"""
        self.assertEqual(self.lista.nombre, "Trabajo")
        self.assertEqual(str(self.lista), "Trabajo")
    
    def test_etiqueta_creation(self):
        """Probar la creación correcta de una etiqueta"""
        self.assertEqual(self.etiqueta1.nombre, "importante")
        self.assertEqual(str(self.etiqueta1), "importante")
        self.assertEqual(self.etiqueta1.color, "#FF0000")
    
    def test_tarea_creation(self):
        """Probar la creación correcta de una tarea"""
        self.assertEqual(self.tarea.titulo, "Preparar informe")
        self.assertEqual(self.tarea.prioridad, 3)
        self.assertEqual(str(self.tarea), "Preparar informe")
        self.assertEqual(self.tarea.lista, self.lista)
        self.assertFalse(self.tarea.completada)
    
    def test_tarea_etiquetas(self):
        """Probar la asignación de etiquetas a tareas"""
        self.assertEqual(self.tarea.etiquetas.count(), 1)
        self.assertIn(self.etiqueta1, self.tarea.etiquetas.all())
        
        # Añadir otra etiqueta y verificar
        self.tarea.etiquetas.add(self.etiqueta2)
        self.assertEqual(self.tarea.etiquetas.count(), 2)
    
    def test_marcar_tarea_como_completada(self):
        """Probar que una tarea se pueda marcar como completada"""
        self.assertFalse(self.tarea.completada)
        
        # Marcar como completada
        self.tarea.marcar_como_completada()
        
        # Verificar que se actualizó correctamente
        self.assertTrue(self.tarea.completada)
        self.assertEqual(self.tarea.estado, 'completada')
        self.assertIsNotNone(self.tarea.fecha_completada)


class ListaAPITestCase(APITestCase):
    """Pruebas para los endpoints de API de Listas"""
    
    def setUp(self):
        """Configuración inicial para las pruebas"""
        self.lista1 = Lista.objects.create(nombre="Lista 1", descripcion="Primera lista")
        self.lista2 = Lista.objects.create(nombre="Lista 2", descripcion="Segunda lista")
        self.lista_url = reverse('tareas-lista-list')
    
    def test_listar_listas(self):
        """Probar que se listen todas las listas"""
        response = self.client.get(self.lista_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_crear_lista(self):
        """Probar la creación de una nueva lista a través de la API"""
        data = {'nombre': 'Nueva Lista', 'descripcion': 'Descripción de prueba'}
        response = self.client.post(self.lista_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lista.objects.count(), 3)
    
    def test_detalle_lista(self):
        """Probar obtener detalles de una lista específica"""
        url = reverse('tareas-lista-detail', args=[self.lista1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre'], 'Lista 1')
    
    def test_actualizar_lista(self):
        """Probar actualizar una lista existente"""
        url = reverse('tareas-lista-detail', args=[self.lista1.id])
        data = {'nombre': 'Lista Actualizada', 'descripcion': 'Descripción actualizada'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar que se actualizó
        self.lista1.refresh_from_db()
        self.assertEqual(self.lista1.nombre, 'Lista Actualizada')
    
    def test_eliminar_lista(self):
        """Probar eliminar una lista"""
        url = reverse('tareas-lista-detail', args=[self.lista1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lista.objects.count(), 1)


class TareaAPITestCase(APITestCase):
    """Pruebas para los endpoints de API de Tareas"""
    
    def setUp(self):
        """Configuración inicial para las pruebas"""
        # Crear lista
        self.lista = Lista.objects.create(nombre="Lista de prueba")
        
        # Crear etiquetas
        self.etiqueta1 = Etiqueta.objects.create(nombre="importante", color="#FF0000")
        self.etiqueta2 = Etiqueta.objects.create(nombre="urgente", color="#0000FF")
        
        # Crear tarea
        self.tarea = Tarea.objects.create(
            titulo="Tarea de prueba",
            descripcion="Descripción de prueba",
            lista=self.lista,
            prioridad=2
        )
        
        # URLs
        self.tareas_url = reverse('tareas-tarea-list')
        self.tarea_url = reverse('tareas-tarea-detail', args=[self.tarea.id])
        self.completar_url = reverse('tareas-tarea-completar', args=[self.tarea.id])
        self.asignar_etiquetas_url = reverse('tareas-tarea-asignar-etiquetas', args=[self.tarea.id])
    
    def test_listar_tareas(self):
        """Probar que se listen todas las tareas"""
        response = self.client.get(self.tareas_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_crear_tarea(self):
        """Probar la creación de una nueva tarea"""
        data = {
            'titulo': 'Nueva tarea',
            'descripcion': 'Descripción de la nueva tarea',
            'lista': self.lista.id,
            'prioridad': 3
        }
        response = self.client.post(self.tareas_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tarea.objects.count(), 2)
    
    def test_detalle_tarea(self):
        """Probar obtener detalles de una tarea específica"""
        response = self.client.get(self.tarea_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['titulo'], 'Tarea de prueba')
    
    def test_marcar_como_completada(self):
        """Probar marcar una tarea como completada a través de la API"""
        response = self.client.post(self.completar_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar que se actualizó
        self.tarea.refresh_from_db()
        self.assertTrue(self.tarea.completada)
        self.assertEqual(self.tarea.estado, 'completada')
    
    def test_asignar_etiquetas(self):
        """Probar asignar etiquetas a una tarea"""
        data = {'etiqueta_ids': [self.etiqueta1.id, self.etiqueta2.id]}
        response = self.client.post(self.asignar_etiquetas_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar que se asignaron las etiquetas
        self.tarea.refresh_from_db()
        self.assertEqual(self.tarea.etiquetas.count(), 2)
    
    def test_filtrar_por_criterios(self):
        """Probar filtrar tareas por diferentes criterios"""
        # Crear varias tareas con diferentes estados y prioridades
        tarea2 = Tarea.objects.create(
            titulo="Tarea urgente",
            lista=self.lista,
            prioridad=4,
            estado='en_proceso'
        )
        
        tarea3 = Tarea.objects.create(
            titulo="Tarea completada",
            lista=self.lista,
            prioridad=1,
            estado='completada',
            completada=True,
            fecha_completada=timezone.now()
        )
        
        # Filtrar por estado
        url = f"{self.tareas_url}?estado=en_proceso"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['titulo'], "Tarea urgente")
        
        # Filtrar por prioridad
        url = f"{self.tareas_url}?prioridad=4"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['titulo'], "Tarea urgente")
        
        # Filtrar por completada
        url = f"{self.tareas_url}?completada=true"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['titulo'], "Tarea completada")


class EtiquetaAPITestCase(APITestCase):
    """Pruebas para los endpoints de API de Etiquetas"""
    
    def setUp(self):
        """Configuración inicial para las pruebas"""
        self.etiqueta1 = Etiqueta.objects.create(nombre="importante", color="#FF0000")
        self.etiqueta2 = Etiqueta.objects.create(nombre="urgente", color="#0000FF")
        self.etiquetas_url = reverse('tareas-etiqueta-list')
    
    def test_listar_etiquetas(self):
        """Probar que se listen todas las etiquetas"""
        response = self.client.get(self.etiquetas_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_crear_etiqueta(self):
        """Probar la creación de una nueva etiqueta"""
        data = {'nombre': 'nueva_etiqueta', 'color': '#00FF00'}
        response = self.client.post(self.etiquetas_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Etiqueta.objects.count(), 3)
    
    def test_detalle_etiqueta(self):
        """Probar obtener detalles de una etiqueta específica"""
        url = reverse('tareas-etiqueta-detail', args=[self.etiqueta1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre'], 'importante')
        self.assertEqual(response.data['color'], '#FF0000')
    
    def test_actualizar_etiqueta(self):
        """Probar actualizar una etiqueta existente"""
        url = reverse('tareas-etiqueta-detail', args=[self.etiqueta1.id])
        data = {'nombre': 'muy_importante', 'color': '#990000'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar que se actualizó
        self.etiqueta1.refresh_from_db()
        self.assertEqual(self.etiqueta1.nombre, 'muy_importante')
        self.assertEqual(self.etiqueta1.color, '#990000')
    
    def test_eliminar_etiqueta(self):
        """Probar eliminar una etiqueta"""
        url = reverse('tareas-etiqueta-detail', args=[self.etiqueta1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Etiqueta.objects.count(), 1)
