import os
from pyairtable import Api
from dotenv import load_dotenv

load_dotenv()

class ConsultaRestauranteAgent:
    def __init__(self):
        self.api_key = os.environ.get("AIRTABLE_API_KEY")
        self.base_id = os.environ.get("AIRTABLE_BASE_ID")
        self.table_name = os.environ.get("AIRTABLE_TABLE_NAME", "Restaurantes")
        
        if not self.api_key or not self.base_id:
            raise ValueError("AIRTABLE_API_KEY and AIRTABLE_BASE_ID must be set")
            
        self.api = Api(self.api_key)
        self.table = self.api.table(self.base_id, self.table_name)

    def search(self, query):
        """
        Searches for restaurants in Airtable where the name contains the query.
        """
        # Airtable formula to search case-insensitive in 'Nombre' field
        formula = f"FIND(LOWER('{query}'), LOWER({{Nombre}}))"
        
        try:
            records = self.table.all(formula=formula)
            
            formatted_results = []
            for record in records:
                fields = record['fields']
                formatted_results.append({
                    "id": record['id'],
                    "nombre": fields.get('Nombre', 'Sin nombre'),
                    "zona": fields.get('Zona', 'Desconocida'),
                    "fitScore": fields.get('FitScore', 90)
                })
                
            return formatted_results
        except Exception as e:
            print(f"Error searching Airtable: {e}")
            return []
    def get_by_id(self, record_id):
        """
        Fetches a single restaurant record by its Airtable ID.
        """
        try:
            record = self.table.get(record_id)
            fields = record['fields']
            
            # Map ACTUAL Airtable fields to Frontend model
            # Field names verified via debug_airtable.py
            menu_text = fields.get('Menú actual', '')
            platos = [p.strip() for p in menu_text.split(',')] if menu_text else []

            return {
                "id": record['id'],
                "nombre": fields.get('Nombre', 'Sin nombre'),
                "tipoCocina": fields.get('Tipo', 'General'), # Was 'Tipo Cocina'
                "precio": "€€", # Not in Airtable, default
                "zona": fields.get('Zona', 'Desconocida'),
                "ultimaVisita": fields.get('Fecha última visita', 'N/A'), # Was 'Ultima Visita'
                "notas": fields.get('Notas', ''), # Was 'Notas Cliente'
                "fitScore": fields.get('FitScore', 85),
                "menuActual": {
                    "platosDestacados": platos
                }
            }
        except Exception as e:
            print(f"Error fetching restaurant {record_id}: {e}")
            return None
