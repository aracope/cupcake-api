from flask import Flask, request, jsonify
from models import db, Cupcake

app = Flask(__name__)
import os
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql:///cupcakes')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# Route to get all cupcakes
@app.route('/api/cupcakes', methods=['GET'])
def get_cupcakes():
    cupcakes = Cupcake.query.all()
    cupcakes_list = []
    
    for cupcake in cupcakes:
        cupcakes_list.append({
            'id': cupcake.id,
            'flavor': cupcake.flavor,
            'size': cupcake.size,
            'rating': cupcake.rating,
            'image': cupcake.image
        })
    
    return jsonify(cupcakes=cupcakes_list)

# Route to get a single cupcake
@app.route('/api/cupcakes/<int:id>', methods=['GET'])
def get_cupcake(id):
    cupcake = Cupcake.query.get(id)
    
    if cupcake:
        return jsonify(cupcake={
            'id': cupcake.id,
            'flavor': cupcake.flavor,
            'size': cupcake.size,
            'rating': cupcake.rating,
            'image': cupcake.image
        })
    
    return jsonify({"error": "Cupcake not found"}), 404

# Route to create a new cupcake
@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    data = request.get_json()

    flavor = data.get('flavor')
    size = data.get('size')
    rating = data.get('rating')
    image = data.get('image', "https://tinyurl.com/demo-cupcake")  # Default image if not provided

    if not flavor or not size or not rating:
        return jsonify({"error": "Missing data"}), 400

    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)
    
    db.session.add(new_cupcake)
    db.session.commit()

    return jsonify(cupcake={
        'id': new_cupcake.id,
        'flavor': new_cupcake.flavor,
        'size': new_cupcake.size,
        'rating': new_cupcake.rating,
        'image': new_cupcake.image
    }), 201

# Route to update a cupcake
@app.route('/api/cupcakes/<int:id>', methods=['PATCH'])
def update_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    data = request.get_json()

    cupcake.flavor = data['flavor']
    cupcake.size = data['size']
    cupcake.rating = data['rating']
    cupcake.image = data['image']

    db.session.commit()

    return jsonify(cupcake={
        'id': cupcake.id,
        'flavor': cupcake.flavor,
        'size': cupcake.size,
        'rating': cupcake.rating,
        'image': cupcake.image
    })

# Route to delete a cupcake
@app.route('/api/cupcakes/<int:id>', methods=['DELETE'])
def delete_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Deleted")



if __name__ == '__main__':
    app.run(debug=True)