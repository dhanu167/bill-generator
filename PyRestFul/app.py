from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

# instance of flask
app = Flask(__name__)
# Api object
api = Api(app)
# DB creation
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///customer.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# SQLALCHEMY mapper
db = SQLAlchemy(app)

# Class for Customers
class Customers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(13), nullable=False)
    gst_number = db.Column(db.String(20), nullable=False)
    pin_code = db.Column(db.Integer, nullable=False)
    state = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f"{self.name} - {self.address} - {self.phone_number} - {self.gst_number} - {self.pin_code} - {self.state}"


# GET request
class GetCustomers(Resource):
    def get(self):
        customers = Customers.query.all()
        customer_list = []
        for customer in customers:
            customer_data = {'Id': customer.id,
                             'Name': customer.name,
                             'Address': customer.address,
                             'PhoneNo': customer.phone_number,
                             'GST': customer.gst_number,
                             'State': customer.state,
                             'PinCode': customer.pin_code}
            customer_list.append(customer_data)
        return {"Customers": customer_list}, 200


# POST request
class AddCustomers(Resource):
    def post(self):
        if request.is_json:
            customer = Customers(name=request.json['Name'],
                                 address=request.json['Address'],
                                 phone_number=request.json['PhoneNo'],
                                 gst_number=request.json['GST'],
                                 pin_code=request.json['PinCode'],
                                 state=request.json['State'])
            db.session.add(customer)
            db.session.commit()

            return make_response(jsonify({
                'Id': customer.id,
                'Name': customer.name,
                'Address': customer.address,
                'PhoneNo': customer.phone_number,
                'GST': customer.gst_number,
                'State': customer.state,
                'PinCode': customer.pin_code
            }), 201)
        else:
            return {'error': 'Request must be in JSON'}, 400


# PUT request
class UpdateCustomers(Resource):
    def put(self, id):
        if request.is_json:
            customer = Customers.query.get(id)
            if customer is None:
                return {'error': 'not found'}, 404
            else:
                customer.name = request.json['Name']
                customer.address = request.json['Address']
                customer.phone_number = request.json['PhoneNo']
                customer.gst_number = request.json['GST']
                customer.pin_code = request.json['PinCode']
                customer.state = request.json['State']
                db.session.commit()
                return 'Updated', 200
        else:
            return {'error':'Request must be JSON'}, 400


# DELETE request
class DeleteCustomers(Resource):
    def delete(self, id):
        customer = Customers.query.get(id)
        if customer is None:
            return {'error': 'not found'}, 404
        db.session.delete(customer)
        db.session.commit()
        return f'{id} was deleted', 200


# API Routs
api.add_resource(GetCustomers, '/')
api.add_resource(AddCustomers, '/add')
api.add_resource(UpdateCustomers, '/update/<id>')
api.add_resource(DeleteCustomers, '/delete/<id>')


if __name__ == '__main__':
    app.run(debug=True)