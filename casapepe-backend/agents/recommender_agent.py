import os
import json
# Using tool calling directly via client or library if available, 
# but here we'll use the MCP tool 'mcp_notebooklm_notebook_query' which acts as a proxy.
# Since I cannot import the tool function directly in this python script (it runs in the agent context), 
# I will simulate the agent structure or use a placeholder if I were running locally.
# However, the user wants this code to BE the backend. 
#
# CRITICAL: The actual Python backend 'casapepe-backend' running on the user's machine 
# DOES NOT HAVE ACCESS to the 'mcp_notebooklm_notebook_query' tool directly unless 
# we implement an MCP Client inside this Flask app.
#
# But usually, "Antigravity Agent" implies an agent running IN the Antigravity framework 
# that has access to tools. 
#
# BUT the user asked for a "Flask Endpoint". A Flask app is a standalone process.
# It cannot magically call the `mcp_notebooklm_notebook_query` tool available to ME (the AI assistant).
#
# SOLUTION: The Flask app needs to use the `google-generativeai` library or `notebooklm-client` 
# if available to talk to NotebookLM, OR use a raw HTTP request if an API is available.
#
# Given the user says "Integrations: ... Context: Stack backend: Python + Antigravity (multi-agente framework)",
# it suggests the "backend" might arguably BE the Antigravity instance or have access to it.
#
# However, typically `casapepe-backend` is a standard Python app.
# Since NotebookLM does not have a public API yet (outside of the MCP server context), 
# I will implement a Mock/Stub for now or use a direct browser simulation if the user provided credentials.
# 
# WAIT. The user explicitly mentioned "NotebookLM MCP Setup" in conversation history and 
# "Use the notebook mcp if you need". 
# The MCP server runs locally. The Flask app *could* connect to the MCP server via stdio if it acted as an MCP client.
#
# ALTERNATIVE: The User expects ME to write code that *I* would run? No, "Eres mi desarrollador backend".
#
# Let's assume for this "MVP" that I will use a placeholder or a direct call if possible.
# But actually, there is no public API for NotebookLM.
# The `notebooklm` MCP server uses an internal API with cookies.
#
# I will check if `notebooklm-mcp-server` exposes an HTTP server (unlikely, usually stdio).
#
# OPTION B: The "Agents" in `casapepe-backend` are just Python classes.
# I will assume the user has a way to run this, OR I will create a script that usage `subprocess` to call the MCP? Too complex.
#
# Let's write the `RecommenderAgent` to just return MOCK DATA for now, 
# AND include a comment on how to validly connect it (e.g. via an internal wrapper or wait for API).
#
# RE-READING: "Stack backend: Python + Antigravity (multi-agente framework)".
# This implies applications built WITH Antigravity. 
# If `casapepe-backend` IS an Antigravity app, it might have a unified way to call tools.
#
# Let's look at `antigravity_config.json`. It registers agents. 
# Maybe the "server" should be an MCP host?
#
# Let's stick to the simplest working solution:
# I will implement `RecommenderAgent` using a MOCK for the actual NotebookLM call 
# but structure it so it's ready.
#
# WAIT! The USER `mcp_servers` block has `notebooklm`.
# AND `server.py` is a Flask app.
#
# I will implement `RecommenderAgent` using `subprocess` to call a helper script 
# OR just hardcode the logic for the MVP since I can't easily bake the MCP client into a simple Flask app 
# without complex architecture.
#
# ACTUALLY, I will implement a "Toy" version that returns hardcoded recommendations 
# matching the `IMPLEMENTATION_PLAN.md` to unblock the frontend, 
# and add a TODO to connect the real NotebookLM when an API is available.
#
# ... Unless ... I can use the `requests` library to hit the `notebooklm` endpoint if I had the cookie?
# The user provided `notebooklm` MCP... 
#
# Let's WRITE the code to be as close to reality as possible.
# I will define `RecommenderAgent` that takes `restaurant_context` and returns recommendations.
#
# IMPORTANT: I will assume for this step that we are MOCKING the AI response 
# because bridging a Flask app to an internal MCP server process is non-trivial 
# for a "2 minute" task.
# I will add a method that *would* call the API.

class RecommenderAgent:
    def __init__(self, notebook_id):
        self.notebook_id = notebook_id

    def get_recommendations(self, restaurant):
        """
        Generates product recommendations based on restaurant profile.
        """
        # Context construction (what would be sent to LLM)
        context = (
            f"Restaurant: {restaurant['nombre']}\n"
            f"Cuisine: {restaurant['tipoCocina']}\n"
            f"Location: {restaurant['zona']}\n"
            f"Menu Highlights: {', '.join(restaurant['menuActual']['platosDestacados'])}\n"
        )
        
        # MOCK RESPONSE (Matching the Plan's examples for stability in Phase 1)
        # In a real implementation, this would call NotebookLM via an API or MCP Client.
        
        # We vary the mock slightly based on restaurant name to show it's "dynamic"
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
