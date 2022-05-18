import json
from pprint import pprint

INVENTORY = dict()
SHIPMENTS = dict()
SHIPMENT_ID = 0

class Item:
    def __init__(self, name, desc):
        self.name = name
        self.desc = desc
        self.quantity = 1

    def __repr__(self):
        return self.desc + ", quantity: " + str(self.quantity)

    def __str__(self):
        return self.name + ": " + self.desc + ", quantity: " + str(self.quantity)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

    def set_desc(self, desc):
        self.desc = desc

    def set_quantity(self, quantity):
        self.quantity = int(quantity)

    def set_name(self, new_name):
        self.name = new_name

    def change_inventory_quantity(self, amount):
        if (amount > self.quantity and amount>0):
            self.quantity = 0
            return self.quantity
        else:
            self.quantity = self.quantity - amount
            return amount

def create_item(item_name):
    if item_name not in INVENTORY.keys():
        INVENTORY[item_name] = Item(item_name, "")
        print("Created item: " + item_name)
        return True
    return False

def edit_item(item_name, desc, quantity):
    if item_name in INVENTORY.keys():
        item = INVENTORY[item_name]
        if desc != "None":
            item.set_desc(desc)
        if quantity != "None":
            item.set_quantity(int(quantity))
        return True
    return False

def delete_item(item_name):
    if item_name in INVENTORY.keys():
        INVENTORY.pop(item_name)
        return True
    return False

def view_inventory():
    inv = {'inventory':[]}
    for i in INVENTORY.values():
        inv['inventory'].append(json.loads(i.toJSON()))
    return inv

def create_shipment():
    global SHIPMENT_ID
    SHIPMENT_ID += 1
    SHIPMENTS[SHIPMENT_ID] = []
    return SHIPMENT_ID

def delete_shipment(ship_id):
    if ship_id in SHIPMENTS.keys():
        for i in SHIPMENTS[ship_id]:
            if i[0] not in INVENTORY.keys():
                # if item has been deleted from inventory
                # assume that we do not want it back in inventory
                # could refactor to make it create new item with quantity in shipment
                continue
            item = INVENTORY[i[0]]
            item.change_inventory_quantity(-i[1])
        SHIPMENTS.pop(ship_id)
        return True
    else:
        return False

def view_shipment(ship_id):
    if ship_id in SHIPMENTS.keys():
        return SHIPMENTS[ship_id]
    else:
        return False
    
def view_all_shipments():
    return SHIPMENTS

def add_to_shipment(ship_id, item_name, amount):
    if ship_id in SHIPMENTS.keys():
        if item_name in INVENTORY.keys():
            item = INVENTORY[item_name]
            if item.quantity <= 0:
                print(item.name+" is sold out!")
                return
            quan = item.change_inventory_quantity(amount)
            SHIPMENTS[ship_id].append((item_name, quan))
            print("Quantity added to shipment: " + str(quan))
            return 1
        else:
            print("Item is not in inventory!")
            return -1
    else:
        print("ShipID cannot be found")
        return 0

def remove_from_shipment(ship_id, item_name, amount):
    if ship_id in SHIPMENTS.keys():
        item_remove = None
        item_found = False
        shipment = SHIPMENTS[ship_id]
        for i in shipment:
            if i[0] == item_name and item_name in INVENTORY.keys():
                item_found = True
                item = INVENTORY[item_name]
                item_remove = i
                if (amount > i[1]):
                    amount = i[1]
                    break
                shipment.append((item_name, i[1]-amount))
                print("Quantity of " + item_name + " removed from shipment: " + str(amount))
                break

        if not item_found:
            print(item_name + " not in shipment")
            return -1

        shipment.remove(item_remove)

        # update inventory quantity
        item.change_inventory_quantity(-amount)
        return 1
    else:
        print("ShipID cannot be found")
        return 0

if __name__ == '__main__':
    ship_id = -1
    while True:
        inp = input('''Please choose from Options mentioned below:
            1. Create Item
            2. Edit Item
            3. Delete Item
            4. View Items
            5. Create Shipment
            6. Add item to Shipment
            7. Remove item from Shipment
            8. Delete Shipment
            0. Quit
            ''')
        if inp == '' or not inp.isnumeric():
            print("Please type numbers from 0 to 8")
        elif int(inp) == 1:
            inp = input('''Please enter an item name: ''')
            create_item(inp)
        elif int(inp) == 2:
            pprint(view_inventory())
            item = input('''Please enter an item name: ''')
            desc = input('''If you want to update, enter new description: ''')
            quantity = input('''If want to update, enter new quantity: ''')
            if quantity.isnumeric():
                if desc == '':
                    desc = "None"
                if quantity == '':
                    quantity = "None"
                edit_item(item, desc, int(quantity))
            else:
                print("Please input a number for quantity")
            view_inventory()
        elif int(inp) == 3:
            pprint(view_inventory())
            item = input('''Please enter item to delete: ''')
            delete_item(item)
        elif int(inp) == 4:
            pprint(view_inventory())
        elif int(inp) == 5:
            ship_id = create_shipment()
            print("Shipment created! ShipID: " + str(ship_id))
        elif int(inp) == 6:
            if ship_id > 0:
                pprint(view_inventory())
                inp = input('''Please select an item to add to shipment: ''')
                quantity = input('''Please specific the quantity of the item: ''')
                if quantity.isnumeric():
                    add_to_shipment(ship_id, inp, int(quantity))
                    view_shipment(ship_id)
                else:
                    print("Please input a number for quantity")
            else:
                print("No shipment has been created!")
        elif int(inp) == 7:
            if ship_id > 0:
                pprint(view_shipment(ship_id))
                inp = input('''Please select an item to remove from shipment: ''')
                quantity = input('''Please specific the quantity of the item: ''')
                if quantity.isnumeric():
                    remove_from_shipment(ship_id, inp, int(quantity))
                    view_shipment(ship_id)
                else:
                    print("Please input a number for quantity")
            else:
                print("No shipment has been created!")
        elif int(inp) == 8:
            if ship_id > 0:
                print(view_shipment(ship_id))
            else:
                print("No shipment has been created!")
        elif int(inp) == 9:
            if ship_id > 0:
                delete_shipment(ship_id)
                print("Shipment has been deleted")
                ship_id -= 1
            else:
                print("No shipment has been created!")
        elif int(inp) == 0:
            print("Quitting the process!")
            break
        elif int(inp) > 9:
            print("Please type numbers from 0 to 9")
        else:
            print("Only numbers are accepted. Please select right option")

    # create_item("apple")
    # view_inventory()
    # edit_item("apple", "juicy", 2)
    # view_inventory()
    # id = create_shipment()
    # add_to_shipment(id, "apple", 1)
    # print(SHIPMENTS)
    # add_to_shipment(id, INVENTORY["apple"])
