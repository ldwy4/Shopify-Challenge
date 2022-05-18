import json
from flask import request, Response
from flask import Flask, redirect, session, send_from_directory
from flask import jsonify
import inventory as api

app = Flask(__name__)

@app.route('/', methods=['GET'])
def api_root():
    return "Shopify Developer Challenge API"

@app.route('/view', methods=['GET'])
def api_view_items():
    inventory = api.view_inventory()
    json_obj = json.dumps(inventory, indent=4)
    return json.loads(json_obj)

@app.route('/create', methods=['POST'])
def api_create_item():
    item_name = str(request.form.get('item_name'))
    print(item_name)
    created = api.create_item(item_name)

    if (created):
        return Response("Created item: " + item_name, status=200)
    return Response(item_name + " has already been created", status=400)

@app.route('/edit', methods=['PUT'])
def api_edit_item():
    item_name = str(request.form.get('item_name'))
    desc = str(request.form.get('description'))
    quantity = str(request.form.get('quantity'))

    if not quantity.isnumeric() and quantity != "None":
        return Response("Invalid Quantity", status=400, mimetype='application/json')
    if api.edit_item(item_name, desc, quantity):
        return Response(item_name + " edited", status=201, mimetype='application/json')
    return Response(item_name + " not found in Inventory", status=404, mimetype='application/json')
    
@app.route('/delete', methods=['DELETE'])
def api_delete_item():
    item_name = str(request.form.get('item_name'))
    if api.delete_item(item_name):
        return Response("Deleted item: " + item_name, status=200)
    return Response(item_name + " not found in Inventory", status=404)

@app.route('/createShip', methods=['POST'])
def api_create_shipment():
    ship_id = api.create_shipment()
    return Response("Shipment ID: " + str(ship_id), status=200)
 
@app.route('/addShip', methods=['PUT'])
def api_add_shipment():
    ship_id = str(request.form.get('ship_id'))
    item_name = str(request.form.get('item_name'))
    quantity = str(request.form.get('quantity'))
    if not quantity.isnumeric() or not ship_id.isnumeric():
        return Response("Invalid Parameters", status=400, mimetype='application/json')
    ret = api.add_to_shipment(int(ship_id), item_name, int(quantity))
    if ret == 1:
        return Response(quantity + " " + item_name + " added to shipment " + ship_id, status=200)
    elif ret == -1:
        return Response(item_name + " not in inventory", status=404)
    else:
        return Response("Shipment " + ship_id + " not found in shipment list", status=404)

@app.route('/removeShip', methods=['PUT'])
def api_remove_from_shipment():
    ship_id = str(request.form.get('ship_id'))
    item_name = str(request.form.get('item_name'))
    quantity = str(request.form.get('quantity'))
    if not quantity.isnumeric() or not ship_id.isnumeric():
        return Response("Invalid Parameters", status=400, mimetype='application/json')
    ret = api.remove_from_shipment(int(ship_id), item_name, int(quantity))
    if ret == 1:
        return Response(quantity + " " + item_name + " removed from shipment " + ship_id, status=200)
    elif ret == -1:
        return Response(item_name + " not in shipment " + ship_id, status=404)
    else:
        return Response("Shipment " + ship_id + " not found in shipment list", status=404)

@app.route('/deleteShip', methods=['DELETE'])
def api_delete_shipment():
    ship_id = str(request.form.get('ship_id'))
    if not ship_id.isnumeric():
        return Response("Invalid ship id: " + ship_id, status=400, mimetype='application/json')
    if api.delete_shipment(int(ship_id)):
        return Response("Shipment ID: " + ship_id + " deleted", status=200)
    return Response("Shipment not found", status=404)


@app.route('/viewShip', methods=['GET'])
def api_view_shipment():
    ship_id = str(request.form.get('ship_id'))
    if not ship_id.isnumeric():
        return Response("Invalid ship id: " + ship_id, status=400, mimetype='application/json')
    shipment = api.view_shipment(int(ship_id))
    if shipment is False:
        return Response(ship_id + " not found in shipment list", status=404)
    return json.dumps(shipment)

@app.route('/viewAllShip', methods=['GET'])
def api_view_all_shipments():
    return json.dumps(api.view_all_shipments())


if __name__ == '__main__':
    app.run(debug=True)
