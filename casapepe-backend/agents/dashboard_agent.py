import os
from pyairtable import Api
from dotenv import load_dotenv
from datetime import datetime, date

load_dotenv()

class DashboardAgent:
    def __init__(self):
        self.api_key = os.environ.get("AIRTABLE_API_KEY")
        self.base_id = os.environ.get("AIRTABLE_BASE_ID")
        
        if not self.api_key or not self.base_id:
            raise ValueError("AIRTABLE_API_KEY and AIRTABLE_BASE_ID must be set")
            
        self.api = Api(self.api_key)
        self.visitas_table = self.api.table(self.base_id, "Visitas")
        self.ventas_table = self.api.table(self.base_id, "Ventas")

    def get_summary(self):
        """
        Devuelve el resumen del dashboard.
        """
        print("DEBUG: Getting Dashboard Summary...")
        
        # 1. Fetch Visits - Relaxed strategy for debugging
        # Instead of generic 'IS_SAME', let's just fetch recent records and filter in Python
        # to avoid formula errors or timezone mismatches being silent.
        
        visitas_hoy = []
        try:
            # Fetch last 20 visits sorted by date descending
            records = self.visitas_table.all(max_records=20, sort=['-Fecha de visita'])
            print(f"DEBUG: Found {len(records)} raw visits in Airtable.")

            # Filter for "Today" manually in Python to be safe with timezones/formats
            today_str = date.today().isoformat() # YYYY-MM-DD
            
            for r in records:
                # Airtable date field: '2024-06-12' or '2024-06-12T00:00:00.000Z'
                fecha_raw = r['fields'].get('Fecha de visita', '')
                if not fecha_raw: continue
                
                # Simple string match for date part
                is_today = fecha_raw.startswith(today_str)
                
                # DEBUG: Force include ALL for now to verify data flow if user wants to see *something*
                # Uncomment line below to force show all recent visits
                # is_today = True 
                
                if is_today:
                    rest_ids = r['fields'].get('Restaurante visitado', [])
                    rest_id = rest_ids[0] if rest_ids else "unknown"
                    hora_raw = r['fields'].get('Hora', '09:00')
                    
                    visitas_hoy.append({
                        "restauranteId": rest_id,
                        "hora": hora_raw,
                        "objetivo": r['fields'].get('Tipo de visita', 'Visita')
                    })
            
            print(f"DEBUG: Filtered {len(visitas_hoy)} visits matching today ({today_str}).")

        except Exception as e:
            print(f"ERROR fetching visits: {e}")
            visitas_hoy = []

        # 2. Alerts (Still Mocked - Phase 3)
        alertas = [
             {
                "id": "alerta_01",
                "tipo": "menu_change",
                "texto": "Tresmacarrons ha actualizado su carta de vinos",
                "date": "Hace 2h",
                "restauranteId": "rec_tm_02", # ID dummy
                "productoRelacionado": None
            }
        ]
        
        # 3. KPIs (Mocked for now as we don't have Ventas logic clearly defined)
        kpis = {
            "ventasMes": "45.2k€",
            "ventasVsObj": "+15%",
            "cierresPendientes": 3
        }
        
        return {
            "visitasHoy": visitas_hoy,
            "alertas": alertas,
            "kpis": kpis
        }
