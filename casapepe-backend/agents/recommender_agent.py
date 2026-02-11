import os
import json

class RecommenderAgent:
    def __init__(self, notebook_id):
        self.notebook_id = notebook_id
        self.token = os.environ.get("NOTEBOOKLM_TOKEN")
        self.client = None
        
        if self.token:
            try:
                from notebooklm import NotebookLM
                self.client = NotebookLM(self.token)
                print(f"DEBUG: NotebookLM Client initialized for {self.notebook_id}")
            except ImportError:
                print("WARNING: notebooklm-py not found. Using Mock.")
            except Exception as e:
                print(f"ERROR initializing NotebookLM: {e}")

    def get_recommendations(self, restaurant):
        """
        Generates product recommendations based on restaurant profile.
        """
        # Context construction
        context = (
            f"Restaurante: {restaurant['nombre']}\n"
            f"Cocina: {restaurant['tipoCocina']}\n"
            f"Zona: {restaurant['zona']}\n"
            f"Notas: {restaurant['notas']}\n"
            f"Platos destacados: {', '.join(restaurant['menuActual']['platosDestacados'])}\n"
        )
        
        # PROMPT for NotebookLM
        prompt = (
            f"Actúa como un sommelier y experto gastronómico comercial de 'Casa Pepe'.\n"
            f"Analiza este cliente:\n{context}\n\n"
            f"TAREA: Recomienda 3 productos de nuestro catálogo que encajen perfectamente con su carta actual.\n"
            f"FORMATO JSON REQUERIDO:\n"
            f"[\n"
            f"  {{\n"
            f"    \"id\": \"ID_DEL_PRODUCTO (ej: prod_01)\",\n"
            f"    \"nombre\": \"Nombre del Producto\",\n"
            f"    \"categoria\": \"Categoría\",\n"
            f"    \"prioridad\": \"alta\" | \"media\",\n"
            f"    \"matchReason\": \"Razón corto (1 frase)\",\n"
            f"    \"storytelling\": \"Argumento de venta largo (2 lineas)\",\n"
            f"    \"cierre\": \"Frase de cierre comercial\",\n"
            f"    \"costeRacion\": \"Calculo aproximado\",\n"
            f"    \"margen\": \"x3.0\"\n"
            f"  }}\n"
            f"]\n"
            f"Usa IDs reales si los conoces, o 'prod_XX' si no."
        )

        # 1. REAL CALL (If configured)
        if self.client:
            try:
                print(f"DEBUG: Querying NotebookLM for {restaurant['nombre']}...")
                # NOTE: The library method structure might vary. 
                # Assuming 'query' method exists and takes notebook_id and query.
                response = self.client.query(self.notebook_id, prompt)
                
                # Check response structure (library specific)
                # Assuming response is a string or object with .content
                text_response = response.content if hasattr(response, 'content') else str(response)
                
                # Extract JSON from Markdown code blocks if present
                if "```json" in text_response:
                    text_response = text_response.split("```json")[1].split("```")[0].strip()
                elif "```" in text_response:
                     text_response = text_response.split("```")[1].split("```")[0].strip()
                
                data = json.loads(text_response)
                print("DEBUG: Successfully parsed NotebookLM response.")
                return data

            except Exception as e:
                print(f"ERROR querying NotebookLM: {e}")
                print("Falling back to Mock data.")

        # 2. MOCK FALLBACK (If no token or error)
        print("DEBUG: Using MOCK implementation.")
        if "Celler" in restaurant['nombre']:
             return [
                {
                    "id": "prod_01",
                    "nombre": "Queso Garrotxa Bauma",
                    "categoria": "Quesos",
                    "prioridad": "alta",
                    "margen": "x3.5",
                    "matchReason": f"Ideal para potenciar la oferta de {restaurant['tipoCocina']}.",
                    "storytelling": "Este queso de piel florida elaborado en el Berguedà aporta una cremosidad única...",
                    "cierre": "¿Le gustaría probar una muestra para su tabla de quesos?",
                    "costeRacion": "2.45 €"
                },
                 {
                    "id": "prod_02",
                    "nombre": "Sobrasada de Mallorca",
                    "categoria": "Embutidos",
                    "prioridad": "media",
                    "margen": "x2.8",
                    "matchReason": "Clásico indispensable.",
                    "storytelling": "Auténtica sobrasada de porc negre...",
                    "cierre": "¿Reponemos stock?",
                    "costeRacion": "1.10 €"
                }
            ]
        else:
             return [
                {
                    "id": "prod_03",
                    "nombre": "Jamón Ibérico Bellota",
                    "categoria": "Embutidos",
                    "prioridad": "alta",
                    "margen": "x4.0",
                    "matchReason": "Producto estrella para ticket alto.",
                    "storytelling": "Curación de 36 meses, perfecto para raciones.",
                    "cierre": "¿Añadimos una pata al pedido?",
                    "costeRacion": "12.00 €"
                }
            ]
