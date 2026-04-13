from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_cors import CORS
from datetime import datetime, timezone

app = Flask(__name__)
CORS(app) # Allows frontend to communicate with backend

# Connect to MongoDB (Default localhost)
client = MongoClient("mongodb://localhost:27017/")
db = client['tierlist_db']
collection = db['tierlists']

# Serve the frontend interface from the /templates folder
@app.route('/')
def home():
    return render_template('index.html')

# --- CRUD OPERATIONS ---

# 1. CREATE
@app.route('/api/tierlists', methods=['POST'])
def create_tierlist():
    data = request.json
    data['metadata'] = {
        'views': 0,
        'created_at': datetime.now(timezone.utc).isoformat(),
        'last_updated': datetime.now(timezone.utc).isoformat()
    }
    result = collection.insert_one(data)
    return jsonify({"message": "Created successfully", "id": str(result.inserted_id)}), 201

# 2. READ (Get all for searching/listing)
@app.route('/api/tierlists', methods=['GET'])
def get_tierlists():
    lists = []
    for t in collection.find():
        t['_id'] = str(t['_id']) # Convert ObjectId to string for JSON output
        lists.append(t)
    return jsonify(lists), 200

# 2. READ (Get single by ID)
@app.route('/api/tierlists/<id>', methods=['GET'])
def get_single_tierlist(id):
    t = collection.find_one({"_id": ObjectId(id)})
    if t:
        t['_id'] = str(t['_id'])
        return jsonify(t), 200
    return jsonify({"error": "Not found"}), 404

# 3. UPDATE (Overwrite the whole tiers & pool arrays)
@app.route('/api/tierlists/<id>', methods=['PUT'])
def update_tierlist(id):
    data = request.json
    
    # Ensure metadata exists before updating timestamp
    if 'metadata' not in data:
        data['metadata'] = {}
    data['metadata']['last_updated'] = datetime.now(timezone.utc).isoformat()
    
    collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": {
            "unranked_pool": data.get("unranked_pool", []),
            "tiers": data.get("tiers", []),
            "metadata.last_updated": data['metadata']['last_updated']
        }}
    )
    return jsonify({"message": "Updated successfully in MongoDB!"}), 200

# 4. DELETE
@app.route('/api/tierlists/<id>', methods=['DELETE'])
def delete_tierlist(id):
    collection.delete_one({"_id": ObjectId(id)})
    return jsonify({"message": "Deleted successfully"}), 200

# --- REPORTING (Aggregation Pipeline) ---
@app.route('/api/reports/consensus', methods=['GET'])
def get_consensus():
    topic = request.args.get('topic', 'Food')
    pipeline = [
        { "$match": { "topic": topic } },
        { "$unwind": "$tiers" },
        { "$unwind": "$tiers.items" },
        { "$group": {
            "_id": { "item": "$tiers.items", "rank": "$tiers.rank" },
            "count": { "$sum": 1 }
        }},
        { "$sort": { "count": -1 } } # Sort by most frequent ranking
    ]
    results = list(collection.aggregate(pipeline))
    return jsonify(results), 200

if __name__ == '__main__':
    # Runs the server on http://localhost:5000
    app.run(debug=True, use_reloader=False, port=5000)