from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from datetime import datetime

# Data contoh produk skincare yang lebih lengkap
skincare_products = [
    {"id": "1", "name": "Moisturizer Glow", "description": "Hydrating moisturizer for glowing skin.", "price": 150000},
    {"id": "2", "name": "Acne Spot Treatment", "description": "Effective treatment for acne spots.", "price": 95000},
    {"id": "3", "name": "Sunscreen SPF 50", "description": "Protects skin from harmful UV rays.", "price": 125000},
    {"id": "4", "name": "Brightening Serum", "description": "Brightens and evens out skin tone.", "price": 210000},
    {"id": "5", "name": "Exfoliating Toner", "description": "Removes dead skin cells and impurities.", "price": 85000},
    {"id": "6", "name": "Night Repair Cream", "description": "Deeply nourishes and repairs skin overnight.", "price": 175000},
    {"id": "7", "name": "Anti-Aging Eye Cream", "description": "Reduces wrinkles and fine lines around eyes.", "price": 140000},
    {"id": "8", "name": "Vitamin C Serum", "description": "Boosts collagen and brightens skin.", "price": 195000},
    {"id": "9", "name": "Hydrating Sheet Mask", "description": "Instant hydration for dry skin.", "price": 25000},
    {"id": "10", "name": "Pore Minimizing Essence", "description": "Refines pores and improves skin texture.", "price": 110000}
]

# Detail produk skincare yang lebih lengkap
product_details = {product['id']: product for product in skincare_products}

app = Flask(_name_)
api = Api(app)

class ProductList(Resource):
    def get(self):
        return {
            "error": False,
            "message": "success",
            "count": len(skincare_products),
            "products": skincare_products
        }

class ProductDetail(Resource):
    def get(self, product_id):
        if product_id in product_details:
            return {
                "error": False,
                "message": "success",
                "product": product_details[product_id]
            }
        return {"error": True, "message": "Product not found"}, 404

class AddProduct(Resource):
    def post(self):
        data = request.get_json()
        new_product = {
            "id": str(len(skincare_products) + 1),  # Generate a new ID
            "name": data.get('name'),
            "description": data.get('description'),
            "price": data.get('price')
        }
        skincare_products.append(new_product)
        product_details[new_product['id']] = new_product
        return {
            "error": False,
            "message": "Product added successfully",
            "product": new_product
        }, 201

class UpdateProduct(Resource):
    def put(self, product_id):
        data = request.get_json()
        if product_id in product_details:
            product_to_update = product_details[product_id]
            product_to_update['name'] = data.get('name', product_to_update['name'])
            product_to_update['description'] = data.get('description', product_to_update['description'])
            product_to_update['price'] = data.get('price', product_to_update['price'])
            return {
                "error": False,
                "message": "Product updated successfully",
                "product": product_to_update
            }
        return {"error": True, "message": "Product not found"}, 404

class DeleteProduct(Resource):
    def delete(self, product_id):
        if product_id in product_details:
            skincare_products.remove(product_details[product_id])
            del product_details[product_id]
            return {
                "error": False,
                "message": "Product deleted successfully"
            }
        return {"error": True, "message": "Product not found"}, 404

# Menambahkan resource ke API
api.add_resource(ProductList, '/products')
api.add_resource(ProductDetail, '/products/<string:product_id>')
api.add_resource(AddProduct, '/products/add')
api.add_resource(UpdateProduct, '/products/update/<string:product_id>')
api.add_resource(DeleteProduct, '/products/delete/<string:product_id>')

if _name_ == '_main_':
    app.run(debug=True)
