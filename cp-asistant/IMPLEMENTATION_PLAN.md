# Implementation Plan - Casa Pepe Assistant
## Backend Integration Roadmap

Este documento detalla la especificación técnica para conectar el frontend de "Casa Pepe Assistant" con el backend "Antigravity".

---

## 1. ARQUITECTURA ACTUAL (Frontend)

### 1.1 Modo de Operación
- **Estado actual:** Standalone (Mock Data).
- **Lógica de datos:** Centralizada en el objeto `MOCK_DATA` dentro de `index.html`.
- **Simulación API:** La función `apiCall()` intercepta las peticiones y devuelve datos hardcodeados con un delay artificial de 800ms.
- **Renderizado:** JavaScript Vanilla manipulando el DOM directamente basado en `AppState`.

### 1.2 Endpoints Esperados
El frontend está construido para consumir los siguientes endpoints REST.

#### A. Búsqueda de Restaurantes
*Usado en:* Barra de búsqueda (autocompletado).

*   **Método:** `POST`
*   **Ruta:** `/restaurantes/search`
*   **Request Body:**
    ```json
    {
      "query": "celler" // string (min 2 chars)
    }
    ```
*   **Response Esperado:**
    ```json
    [
      {
        "id": "rec_cj_01",
        "nombre": "Celler Jordana",
        "zona": "Alella",
        "fitScore": 96
      },
      ...
    ]
    ```

#### B. Detalle de Restaurante (Contexto + Recomendaciones)
*Usado en:* Selección de restaurante (`loadRestaurant`).
*Nota:* El backend debe ejecutar los agentes de NotebookLM y devolver los productos ya filtrados y priorizados.

*   **Método:** `POST`
*   **Ruta:** `/restaurantes/detail`
*   **Request Body:**
    ```json
    {
      "id": "rec_cj_01" // string (ID único restaurante)
    }
    ```
*   **Response Esperado:**
    ```json
    {
      "id": "rec_cj_01",
      "nombre": "Celler Jordana",
      "tipoCocina": "Tradicional Catalana",
      "precio": "€€",
      "zona": "Alella / El Masnou",
      "ultimaVisita": "Hace 20 días", // O timestamp ISO
      "notas": "Preferencia por quesos artesanos...",
      "fitScore": 96,
      "menuActual": {
        "platosDestacados": ["Canelones", "Setas"]
      },
      "productosRecomendados": [ // ARRAY CRÍTICO
        {
          "id": "prod_01",
          "nombre": "Queso Garrotxa",
          "categoria": "Quesos",
          "prioridad": "alta", // alta | media | baja
          "margen": "x3.5",
          "matchReason": "Encaja con tabla de quesos actual",
          "storytelling": "Texto largo generado por NotebookLM...",
          "cierre": "Frase de cierre comercial...",
          "costeRacion": "2.45 €"
        }
      ]
    }
    ```

#### C. Registrar Visita
*Usado en:* Botón flotante "Registrar Visita".

*   **Método:** `POST`
*   **Ruta:** `/visita/registrar`
*   **Request Body:**
    ```json
    {
      "restauranteId": "rec_cj_01",
      "cart": ["prod_01", "prod_03"], // Array de Product IDs
      "timestamp": "2025-02-28T10:00:00Z"
    }
    ```
*   **Response Esperado:**
    ```json
    {
      "success": true,
      "visitId": "vis_12345"
    }
    ```

### 1.3 Estructura de Datos Mock (Referencia)
Ver sección 10 para el JSON completo. Los campos clave que el backend debe mapear son:
- `fitScore`: 0-100 (Calculado por backend basado en menú vs catálogo).
- `prioridad`: 'alta' (renderiza borde rojo) vs 'media' (borde gris).
- `matchReason`: Texto corto (1 linea).
- `storytelling`: Texto largo (párrafo) para el modal.

---

## 2. FLUJOS DE USUARIO IMPLEMENTADOS

### Pantalla: Dashboard (Inicio)
- **Trigger:** Carga inicial de la app.
- **Datos:**
  1. Lista de `visitasHoy` (Ruta del día).
  2. Lista de `alertas` (Notificaciones dropdown).
  3. KPIs (Ventas mes, Cierres pendientes).
- **Endpoints:** Actualmente mockeado en `AppState.init()`.
  - *Requisito Backend:* Crear endpoint `GET /dashboard/summary` que devuelva esta estructura combinada.
- **Interacciones:** Click en item de ruta -> Carga detalle restaurante.

### Pantalla: Búsqueda
- **Trigger:** Input usuario (> 2 caracteres).
- **Datos:** Lista ligera de restaurantes (ID, nombre, zona, score).
- **Estados:**
  - *Loading:* Spinner en input.
  - *Success:* Lista desplegable.
  - *Empty:* "No se encontraron resultados".
- **Interacciones:** Debounce de 300ms implementado en frontend.

### Pantalla: Detalle Restaurante + Productos
- **Trigger:** Selección desde Búsqueda o Dashboard.
- **Datos:** Objeto completo del restaurante + Array de productos recomendados.
- **Lógica Backend requerida:**
  1. El Backend recibe ID.
  2. Consulta Firebase/Airtable para datos estáticos.
  3. **NotebookLM Agent** determina qué productos del catálogo hacen match con el menú actual.
  4. Devuelve respuesta unificada.
- **Interacciones:**
  - Click en carta producto -> Abre Modal.
  - Click botón "Añadir" -> Agrega a `AppState.cart`.

### Pantalla: Modal Argumentario
- **Trigger:** Click en card de producto.
- **Datos:** Utiliza los datos ya cargados en memoria (no hace fetch adicional).
- **Interacciones:**
  - Copiar al portapapeles (usa API navegador).
  - Enviar Whatsapp (abre `wa.me` con deep link).

---

## 3. PRIORIZACIÓN DE IMPLEMENTACIÓN

### FASE 1 - MVP Core (Crítico)
**Objetivo:** Que el comercial pueda buscar un cliente y ver qué venderle.
1. **Endpoint `/restaurantes/search`:** Búsqueda rápida contra Airtable.
2. **Endpoint `/restaurantes/detail`:** El core del valor. Integración con NotebookLM para devolver `storytelling` y `matchReason` dinámicos.
   - *Complejidad:* Alta (Requiere orquestación de agentes).

### FASE 2 - Funcionalidad Transaccional
**Objetivo:** Cerrar el ciclo de venta.
1. **Endpoint `/visita/registrar`:** Guardar el resultado en CRM (Airtable).
2. **Endpoint `/dashboard/summary`:** Llenar la pantalla inicial con datos reales del usuario.

### FASE 3 - Inteligencia Proactiva
1. **Alertas (Websockets/Polling):** Notificar cambios de menú detectados por el scraper ("Tresmacarrons ha cambiado carta").
2. **Sincronización Offline:** Implementar Service Workers para cachear respuestas GET.

---

## 4. DEPENDENCIAS Y REQUISITOS

### 4.1 Configuración
Variables necesarias en `window.CONFIG` o `.env`:
- `API_URL`: `https://api.antigravity.com/v1`
- `REQUEST_TIMEOUT`: 30000ms (NotebookLM puede tardar).

### 4.2 Formatos de Datos
- **Precios:** Strings formateados ("24.50 €/kg") o Numbers (24.50). El frontend solo renderiza texto, el backend decide el formato.
- **Fechas:** Strings relativos ("Hace 2h") preferidos para visualización directa, o ISO-8601 si el backend prefiere que el frontend calcule (requiere librería fecha ligera o `Intl.RelativeTimeFormat`).

### 4.3 Validaciones Frontend
- Búsqueda: Mínimo 2 caracteres.
- Checkout: Carrito > 0 items.
- El backend debe validar que los `productIds` existan y el `restauranteId` sea válido.

---

## 5. ESTADOS Y PERSISTENCIA

### 5.1 LocalStorage
- `casapepe_cart`: Array de Strings `['prod_01', 'prod_02']`. Persiste la selección si se recarga la página.
- Se limpia automáticamente al recibir `200 OK` de `/visita/registrar`.

### 5.2 AppState (Memoria)
- `user`: Datos del comercial logueado.
- `currentRestaurant`: Objeto completo del restaurante visualizado.
- `currentProduct`: Objeto del producto activo en el modal.

---

## 6. MANEJO DE ERRORES

### 6.1 UI Feedback
- **Toast Error:** El frontend tiene una función `showError(msg)` que muestra una alerta roja superior. El backend debe enviar mensajes de error `message` en el JSON de respuesta 4xx/5xx para ser mostrados directamente.
- **Loading:** Overlay completo con spinner (`showLoadingState`).

### 6.2 Edge Cases
- **Restaurante sin productos:** El endpoint `/detail` debe devolver `productosRecomendados: []`. El frontend mostrará lista vacía (falta implementar "Empty State" visual bonito).
- **Timeouts:** Si Antigravity tarda >30s, el frontend captura la excepción y muestra "Error de conexión".

---

## 7. CAMBIOS NECESARIOS PARA PRODUCCIÓN

1. **index.html:**
   - Cambiar `const CONFIG = { MODE: 'mock' ... }` a `MODE: 'production'`.
   - Actualizar `API_URL` real.
   - Eliminar el bloque gigante de `const MOCK_DATA = {...}` para reducir peso del archivo.
   - Eliminar `setTimeout` en `apiCall` y dejar solo el `fetch`.

2. **Testing:**
   - Probar flujo: Buscar "Celler" -> Click Resultado -> Añadir Queso -> Registrar.
   - Verificar que el `storytelling` en el modal corresponde al producto seleccionado.

---

## 8. INTEGRACIÓN CON SISTEMAS BACKEND

### 8.1 Airtable (CRM)
El frontend espera los siguientes campos mapeados:
- `Nombre`, `Zona`, `Tipo Cocina`, `Precio Medio`.
- `Ultima Visita` (Fecha).
- `Notas Cliente` (Texto libre).

### 8.2 NotebookLM (Agente)
El backend debe consultar al modelo con el prompt:
*"Dada la carta actual de [Restaurante] y nuestro catálogo, selecciona los 3 mejores productos, explica por qué encajan (matchReason) y genera un storytelling de venta."*

El output de NotebookLM debe ser parseado a JSON para llenar:
- `productosRecomendados[i].matchReason`
- `productosRecomendados[i].storytelling`
- `productosRecomendados[i].cierre`

---

## 9. ESPECIFICACIONES TÉCNICAS

### 9.1 Seguridad
- **CORS:** El backend debe permitir origen `*` o el dominio específico donde se aloje el frontend PWA.
- **Auth:** Actualmente no implementado. Se sugiere añadir header `Authorization: Bearer <token>` en `apiCall` si se implementa login.

### 9.2 Performance
- El frontend es muy ligero. La latencia percibida dependerá 100% del tiempo de inferencia de NotebookLM en el endpoint `/detail`.
- **Estrategia sugerida:** Pre-calcular recomendaciones en background (cron job nocturno) y guardarlas en base de datos para que `/detail` sea rápido.

---

## 10. ANEXOS

### 10.1 Estructura Data Objects (Referencia)

**Producto (Frontend Model):**
```javascript
{
  id: "prod_01",
  nombre: "Queso Garrotxa Bauma",
  categoria: "Quesos", // Tag visual
  origen: "Borredà (Berguedà)",
  precio: "24.50 €/kg", // Display only
  costeRacion: "2.45 €", // Dato técnico modal
  margen: "x3.5", // Highlight verde
  prioridad: "alta", // alta = borde rojo, media = gris
  matchReason: "Encaja perfecto en su tabla de quesos...", // En card
  storytelling: "Queso de cabra de piel florida...", // En modal
  cierre: "¿Te dejo una cuña de muestra...?" // En modal
}
```

### 10.2 Funciones Clave (index.html)
- `apiCall(endpoint, method, body)`: Wrapper central de fetch.
- `loadRestaurant(id)`: Orquestador de carga de detalle.
- `finalizarVisita()`: Orquestador de checkout.
- `AppState.init()`: Bootstrap de la aplicación.
