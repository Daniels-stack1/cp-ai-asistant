import pytest
from unittest.mock import patch, MagicMock
from server import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@patch('agents.consulta_restaurante.Api')
def test_search_endpoint(mock_api, client):
    # Mock Airtable response
    mock_table = MagicMock()
    mock_api.return_value.table.return_value = mock_table
    
    mock_record = {
        'id': 'rec123',
        'fields': {
            'Nombre': 'Test Restaurant',
            'Zona': 'Test Zone',
            'FitScore': 95
        }
    }
    mock_table.all.return_value = [mock_record]

    response = client.post('/api/restaurantes/search', json={'query': 'test'})
    
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['nombre'] == 'Test Restaurant'
    assert data[0]['id'] == 'rec123'

def test_search_endpoint_short_query(client):
    response = client.post('/api/restaurantes/search', json={'query': 'a'})
    assert response.status_code == 400
