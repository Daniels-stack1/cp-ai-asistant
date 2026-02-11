from flask import Blueprint, request, jsonify
from agents.consulta_restaurante import ConsultaRestauranteAgent
from agents.recommender_agent import RecommenderAgent

api_blueprint = Blueprint('api', __name__)
# Notebook ID provided by user
NOTEBOOK_ID = "5501f8ff-0b76-4ffe-aa12-85a2618565c0"

@api_blueprint.route('/', methods=['GET'])
def api_root():
    return jsonify({"message": "Casa Pepe AI Backend Running", "version": "1.0"}), 200

@api_blueprint.route('/restaurantes/search', methods=['POST'])
def search_restaurantes():
    data = request.get_json()
    query = data.get('query', '')
    
    if len(query) < 2:
        return jsonify({"error": "Query must be at least 2 characters"}), 400

    agent = ConsultaRestauranteAgent()
    results = agent.search(query)
    
    return jsonify(results)

@api_blueprint.route('/restaurantes/detail', methods=['POST'])
def get_restaurant_detail():
    data = request.get_json()
    rec_id = data.get('id')
    
    if not rec_id:
        return jsonify({"error": "Restaurant ID is required"}), 400

    # 1. Get Static Data
    search_agent = ConsultaRestauranteAgent()
    restaurant = search_agent.get_by_id(rec_id)
    
    if not restaurant:
        return jsonify({"error": "Restaurant not found"}), 404

    # 2. Get AI Recommendations
    recommender = RecommenderAgent(NOTEBOOK_ID)
    recommendations = recommender.get_recommendations(restaurant)
    
    # 3. Merge Results
    restaurant['productosRecomendados'] = recommendations
    
    return jsonify(restaurant)

from agents.visita_agent import VisitaAgent

@api_blueprint.route('/visita/registrar', methods=['POST'])
def registrar_visita():
    data = request.get_json()
    
    restaurante_id = data.get('restauranteId')
    cart = data.get('cart', [])
    timestamp = data.get('timestamp')
    
    if not restaurante_id:
        return jsonify({"error": "restauranteId is required"}), 400
        
    agent = VisitaAgent()
    result = agent.registrar_visita(restaurante_id, cart, timestamp)
    
    if result.get("success"):
        return jsonify(result), 200
    else:
        return jsonify(result), 500

from agents.dashboard_agent import DashboardAgent

@api_blueprint.route('/dashboard/summary', methods=['GET'])
def get_dashboard_summary():
    agent = DashboardAgent()
    summary = agent.get_summary()
    return jsonify(summary)

@api_blueprint.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok"}), 200
