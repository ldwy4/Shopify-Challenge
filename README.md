# Shopify-Challenge
Shopify Technical Challenge

## Notes
- The extra feature chosen was the shipments option.
- The replit link you can only run a console version of the application.
- If the repo is cloned, one can run flask app from their machine and using an application such as PostMan can call the API.

## REST API form format
|Command | Required Form Parameters | Optional Parameters| Endpoint |
| -----------------|---------------|--------------------|-----------|
|Create | item_name| | /create |
|Edit | item_name | description, quantity| /edit|
|Delete | item_name | | /delete |
|View | | | /view |
|Create Shipment| | | /createShip|
|Add to Shipment| ship_id, item_name, quantity| | /addShip|
|Remove from Shipment | ship_id, item_name, quantity| | /removeShip |
|View shipment | ship_id | | /viewShip|
|View all shipments | | | /viewAllShip|

### Example
![example API call via Postman](https://github.com/ldwy4/Shopify-Challenge/blob/master/Capture.PNG)
