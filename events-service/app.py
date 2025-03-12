from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Habilita CORS para toda la aplicación

# Configuración de MongoDB
mongo_uri = "mongodb+srv://franciscoseguravalencia:TZ6zBlsgO3Q1dsfh@cluster0.zjpre.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(mongo_uri)
db = client['event-microservice']
events_collection = db['events']

# Ruta para obtener todos los eventos
@app.route('/events', methods=['GET'])
def get_events():
    events = list(events_collection.find())
    for event in events:
        event['_id'] = str(event['_id'])  # Convertir ObjectId a string
    return jsonify(events)

@app.route('/events/<int:id>', methods=['GET'])
def get_event(id):
    event = events_collection.find_one({'id': id})  # Busca por el campo 'id'
    if event:
        event['_id'] = str(event['_id'])  # Convertir ObjectId a string
        return jsonify(event)
    else:
        return jsonify({'error': 'Event not found'}), 404

# Ruta para crear un nuevo evento
@app.route('/events', methods=['POST'])
def create_event():
    new_event = request.json
    new_event['date'] = datetime.strptime(new_event['date'], '%Y-%m-%dT%H:%M:%S')
    result = events_collection.insert_one(new_event)
    return jsonify({'_id': str(result.inserted_id)}), 201

# Ruta para actualizar un evento existente
@app.route('/events/<id>', methods=['PUT'])
def update_event(id):
    updated_event = request.json
    if 'date' in updated_event:
        updated_event['date'] = datetime.strptime(updated_event['date'], '%Y-%m-%dT%H:%M:%S')
    result = events_collection.update_one({'_id': ObjectId(id)}, {'$set': updated_event})
    if result.matched_count:
        return jsonify({'message': 'Event updated successfully'})
    else:
        return jsonify({'error': 'Event not found'}), 404

# Ruta para eliminar un evento
@app.route('/events/<id>', methods=['DELETE'])
def delete_event(id):
    result = events_collection.delete_one({'_id': ObjectId(id)})
    if result.deleted_count:
        return jsonify({'message': 'Event deleted successfully'})
    else:
        return jsonify({'error': 'Event not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5001)
