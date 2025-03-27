from flask import Flask, request, jsonify
from flask_cors import CORS
from http import HTTPStatus

from src.settings import load_config
from src.run_api import run_api


class Text2SQLServer:
    """Flask server class for Text2SQL API"""

    def __init__(self):
        """Initialize Flask application and configuration"""
        self.app = Flask(__name__)
        CORS(self.app)
        self.config = load_config()

        # Load server configuration
        self.server_config = self.config.get('server', {'host':'0.0.0.0', 'port':5000, 'debug':False})

        # Register routes
        self.register_routes()


    def register_routes(self):
        """Register all API routes"""
        self.app.add_url_rule(rule='/api/query', endpoint='text2sql', view_func=self.text2sql_endpoint, methods=['POST'], )
        self.app.add_url_rule(rule='/api/health', endpoint='health_check', view_func=self.health_check, methods=['GET'])


    def text2sql_endpoint(self):
        """Endpoint to handle Text2SQL queries and return the result"""
        try:
            data = request.get_json()

            if not data or 'query' not in data:
                return jsonify({'error': 'Missing query parameter'}), HTTPStatus.BAD_REQUEST

            query = data['query']
            result = run_api(query)

            return jsonify({'status':'success', 'result':result}), HTTPStatus.OK

        except Exception as e:
            return jsonify({'status':'error', 'message': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


    def health_check(self):
        """Health check endpoint to verify the server status"""
        return jsonify({'status':'healthy', 'message':'Text2SQL API is running'}), HTTPStatus.OK


    def run(self):
        """Run the Flask server with configuration from config.yml"""
        host = self.server_config.get('host', '0.0.0.0')
        port = self.server_config.get('port', 5000)
        debug = self.server_config.get('debug', False)

        print(f"Starting Text2SQL server on {host}:{port}")
        self.app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    # Create and run server instance
    server = Text2SQLServer()
    server.run()



