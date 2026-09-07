# Emergency Housing — MVP 0.4

Prototipo de registro rápido de daños y pre-triage de viviendas después de un terremoto.

## Corrección de mapas en 0.4.1

Esta entrega corrige el problema del mapa de Carto que puede mostrar `API KEY REQUIRED`.

- El mapa de ubicación del usuario utiliza **OpenStreetMap** sin API key.
- El usuario puede hacer clic directamente sobre el mapa para seleccionar la vivienda.
- Las coordenadas seleccionadas se actualizan en el formulario.
- La **dirección** sigue siendo un campo independiente y no se elimina.
- El mapa operativo también utiliza OpenStreetMap.
- Las capas `Expedientes DEMO` y `Expedientes registrados` siguen siendo independientes y se pueden activar/desactivar.

## Incluye

- Coordenadas + dirección
- Mapa interactivo para seleccionar ubicación
- 10 preguntas críticas
- Priority Score heurístico
- Prioridad ALTA / MEDIA / BAJA
- 1–10 fotografías
- Ventana tentativa de visita profesional
- Expediente PNG
- Persistencia local en `data/cases.json`
- Fotografías en `photos/`
- Reportes en `reports/`
- Mapa operativo
- Capas DEMO y expedientes registrados separadas y cerrables

## Google Colab

```python
%cd /content/Emergency_Housing_MVP_0_4
!pip install -r requirements.txt
!streamlit run app.py --server.port 8501 &
```

El score es experimental y no determina habitabilidad. OpenStreetMap debe utilizarse respetando su política de uso de teselas; para un despliegue público de mayor escala convendrá configurar un proveedor de mapas/tiles apropiado.

## Próximo paso

MVP 0.5 — benchmark de Computer Vision separado de la aplicación.
