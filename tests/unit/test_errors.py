import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

from api.errors import error_handler

def build_error_payload(code, message):
    return {'error': {'code': code, 'message': message}}

@pytest.fixture
def test_app():
    class InputSchema(BaseModel):
        a: float
        b: int
    
    app = FastAPI()

    @app.post('/42200')
    def _(inputs: InputSchema):
        return inputs

    @app.get('/50010')
    def _():
        raise Exception('Unhandled error')
    
    error_handler(app)

    return app

@pytest.fixture
def test_client(test_app):
    return TestClient(test_app, raise_server_exceptions=False)

class TestErrorHandler:

    @pytest.mark.parametrize('code,status,message', [
        (50010, 500, 'Internal Server Error.')
    ])
    def test_5xx_error_handlers(self, test_client, code, status, message):
        response = test_client.get(f'/{code}')
        expected = build_error_payload(code, message)

        assert response.status_code == status
        assert response.json() == expected

    def test_validation_error(self, test_client):
        response = test_client.post('/42200', json={
            'a': 'test'
        })
        expected = build_error_payload(42200, 'Validation error.')
        expected['error']['errors'] = [{
            'location': 'body.a',
            'message': 'Input should be a valid number, unable to parse string as a number'
        }, {
            'location': 'body.b',
            'message': 'Field required'
        }]
        assert response.status_code == 422
        assert response.json() == expected


    def test_404_error(self, test_client):
        response = test_client.get('/<invalid_url>')
        expected = build_error_payload(40400, 'Not Found')

        assert response.status_code == 404
        assert response.json() == expected

    def test_405_error(self, test_client):
        response = test_client.delete('/50010')
        expected = build_error_payload(40500, 'Method Not Allowed')

        assert response.status_code == 405
        assert response.json() == expected