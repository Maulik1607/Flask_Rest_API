from flask import Flask,request
from flask_restful import Resource,Api,reqparse
from flask_jwt import JWT,jwt_required

from security import authenticate,identity

app = Flask(__name__)
app.secret_key = 'jose'
api = Api(app)

jwt = JWT(app,authenticate,identity)    #/auth

items = []

# fetch items with name---------------------------------
class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type = float,
        required = True,
        help = "This field cannot be blank"
        
        )
    @jwt_required()
    def get(Self,name):
        item = next(filter(lambda x: x['name'] == name,items),None)
        return {'item':item}, 200 

# create item-------------------------------------------
    def post(self,name):
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data =Item.parser.parse_args()
        
        item = {'name':name,'price':data['price']}
        items.append(item)
        return item, 201
   
    # deletd item-------------------------------------------
    def delete(self,name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'Item deleted'}

    # updated item-------------------------------------------
    # @jwt_required()
    def put(self, name):
       
        data = Item.parser.parse_args()
        # Once again, print something not in the args to verify everything works
        
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item

# creating itemlist-------------------------------------
class Itemlist(Resource):
    def get(self):
        return {'items':items}


api.add_resource(Item,'/item/<string:name>')
api.add_resource(Itemlist,'/items')
app.run(port=5000,debug=True)