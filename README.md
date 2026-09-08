# Emergency Housing — MVP 0.4

Prototipo de investigación para el **registro rápido, caracterización y pre-triage de viviendas afectadas después de un terremoto**.

El objetivo es explorar un posible puente entre el primer reporte realizado por una familia afectada y una posterior evaluación técnica profesional.

> ⚠️ **Research prototype — please do not submit real personal, property or emergency information.**
>
> This prototype is for demonstration and research purposes only. It is **not an emergency service**, does not replace emergency response systems, and does not determine whether a building is safe or habitable.

## Qué hace el prototipo

El usuario puede:

- Localizar la vivienda mediante un **mapa interactivo**.
- Proporcionar la **dirección** como información independiente.
- Responder un conjunto reducido de preguntas para caracterizar rápidamente la situación.
- Adjuntar entre **1 y 10 fotografías** del inmueble.
- Obtener un **Priority Score experimental**.
- Clasificar preliminarmente el caso como **ALTA / MEDIA / BAJA prioridad**.
- Generar un expediente visual de la información registrada.
- Indicar una **ventana tentativa para una eventual visita profesional**.

La aplicación busca organizar la información inicial y explorar mecanismos de priorización.

**No determina si una vivienda es segura, habitable o estructuralmente estable.** La evaluación estructural definitiva debe ser realizada por profesionales competentes.

## Corrección de mapas en 0.4.1

Esta entrega corrige el problema del mapa de Carto que podía mostrar `API KEY REQUIRED`.

- El mapa de ubicación utiliza **OpenStreetMap** sin API key.
- El usuario puede hacer clic directamente sobre el mapa para seleccionar la vivienda.
- Las coordenadas seleccionadas se actualizan en el formulario.
- La **dirección permanece como un campo independiente**.
- El mapa operativo también utiliza OpenStreetMap.
- Las capas `Expedientes DEMO` y `Expedientes registrados` son independientes y pueden activarse/desactivarse.
- Los nuevos expedientes registrados pueden visualizarse en el mapa operativo.

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
- Capas DEMO y expedientes registrados independientes

## Lógica de priorización

La versión actual utiliza una **ecuación heurística sencilla** para generar un Priority Score a partir de la información registrada por el usuario.

Este score es experimental y tiene únicamente una función de **pre-triage**.

No representa una evaluación estructural, no calcula probabilidad de colapso y no determina habitabilidad o seguridad.

Una evolución futura podría incorporar criterios más rigurosos y pesos derivados de conocimiento de **ingeniería estructural**, así como otras variables técnicas y geoespaciales.

La intención es que la priorización pueda evolucionar progresivamente desde una lógica heurística hacia un enfoque basado en evidencia, manteniendo siempre la evaluación profesional como etapa necesaria para las decisiones técnicas.

## Diseño para escenarios de conectividad limitada

Una consideración importante para el desarrollo futuro de Emergency Housing es que la aplicación está pensada para escenarios de **conectividad limitada o intermitente**.

Después de un terremoto u otro desastre de gran magnitud, pueden producirse interrupciones de las redes móviles, pérdida de acceso a Internet o caída temporal de servicios digitales durante horas o incluso días.

Por esta razón, el diseño del sistema contempla como objetivo futuro una arquitectura **offline-first**, que permita:

- registrar información aun sin conexión a Internet;
- almacenar temporalmente los datos y fotografías en el dispositivo;
- utilizar información geográfica disponible localmente;
- mantener los registros pendientes de sincronización;
- sincronizar la información cuando se restablezca la conectividad.

La versión actual es un prototipo web desplegado en Streamlit y **requiere conectividad para su funcionamiento**.

El enfoque offline-first forma parte de la evolución prevista del sistema y deberá ser validado en futuras versiones.

## Privacidad y uso de datos

Esta aplicación es un **prototipo de investigación y demostración**.

No introduzca:

- nombres reales;
- números de identificación;
- teléfonos;
- información personal sensible;
- fotografías que contengan información personal sensible;
- información de emergencias reales;
- información que pueda poner en riesgo a personas o propiedades.

Para demostraciones públicas se recomienda utilizar únicamente **datos ficticios o información anonimizada**.

## Mapas

El prototipo utiliza **OpenStreetMap**.

El uso de los mapas debe respetar la política de uso de teselas de OpenStreetMap.

Para un despliegue público de mayor escala o un sistema operativo real, será necesario utilizar un proveedor de mapas/tiles apropiado y configurar la infraestructura correspondiente.

## Google Colab

Para ejecutar el prototipo en Google Colab:

```python
%cd /content/Emergency_Housing_MVP_0_4
!pip install -r requirements.txt
!streamlit run app.py --server.port 8501 &