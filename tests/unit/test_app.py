import pytest
from fastapi.testclient import TestClient

from api.app import app
from api.config import settings


class TestApp:

    @pytest.fixture
    def client(self, app):
        return TestClient(app)
    
    @pytest.fixture
    def app(self):
        return app
    
    def test_registered_routes(self, app):
        all_routes = [route.path for route in app.routes]
        expected = {
            '/docs', '/redoc', '/openapi.json'
        }
        assert expected.issubset(all_routes)

    def test_auto_api_documentation(self, client):
        assert client.get('/docs').status_code == 200
        assert client.get('/redoc').status_code == 200
        response = client.get('/openapi.json')
        openapi = response.json()
        assert response.status_code == 200
        assert settings.PROJECT_NAME == openapi['info']['title']

    def test_endpoint_hello_world(self, client):
        response = client.get('')
        assert response.status_code == 200
        assert response.json() == {'msg': 'hello world'}