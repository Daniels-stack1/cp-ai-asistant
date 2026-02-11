import os
from pyairtable import Api
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class VisitaAgent:
    def __init__(self):
        self.api_key = os.environ.get("AIRTABLE_API_KEY")
        self.base_id = os.environ.get("AIRTABLE_BASE_ID")
        self.table_name = "Visitas" # Explicitly Visitas
        
        if not self.api_key or not self.base_id:
            raise ValueError("AIRTABLE_API_KEY and AIRTABLE_BASE_ID must be set")
            
        self.api = Api(self.api_key)
        self.table = self.api.table(self.base_id, self.table_name)

    def registrar_visita(self, restaurante_id, productos_ids, timestamp=None):
        """
        Registra una nueva visita en la tabla 'Visitas'.
        """
        print(f"DEBUG: Registrar visita. RestID={restaurante_id}, Products={productos_ids}")

        # 1. Prepare Timestamp
        if not timestamp:
            timestamp = datetime.now().isoformat()
        
        # 2. Handle Mock Products
        # Real Airtable IDs usually start with 'rec'. Mock IDs are 'prod_'.
        # If we send 'prod_' IDs to a Link field, Airtable will throw 422.
        valid_product_ids = []
        mock_product_names = []
        
        for pid in productos_ids:
            if str(pid).startswith('rec'):
                valid_product_ids.append(pid)
            else:
                mock_product_names.append(pid)
        
        feedback_text = "Visita registrada desde Casa Pepe Assistant."
        if mock_product_names:
            feedback_text += f" Productos ref (Simulados): {', '.join(mock_product_names)}"

        # 3. Map Payload
        fields = {
            "Fecha de visita": timestamp,
            "Restaurante visitado": [restaurante_id], # Must be an array of IDs
            "Productos presentados": valid_product_ids, # Only valid IDs
            "Tipo de visita": "Visita de cortesía",
            "Feedback del chef": feedback_text
        }
        
        try:
            print(f"DEBUG: Sending fields to Airtable: {fields}")
            record = self.table.create(fields)
            print(f"DEBUG: Success. ID={record['id']}")
            return {"success": True, "visitId": record['id']}
        except Exception as e:
            print(f"ERROR registering visit: {e}")
            return {"success": False, "error": str(e)}
