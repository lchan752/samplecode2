## Overview
This samplecode is a tool for managing customers, and sending anniversary postcards via lob.com

It includes webapp to LIST/ADD/EDIT/DELETE customers.
Each customer, we store the name, address, creation date.

If customerA is created on 2018-04-01, then a postcard should be sent on 2019-04-01, 2020-04-01, 2021-04-01 etc.

The web app should also show the postcard sending history, for each customer it should show a table showing the lob ID, lob URL for rendered postcard, postcard creation date, expected delivery date.

The system will NOT need to listen for lob web hooks for postcard tracking events.
The system will NOT need any authentication or authorisation. Everyone can do everything, no need to login/logout.


## Backend API

POST /customer/ to create a customer. Each customer will have following fields (i.e. info needed for lob to send out a postcard)
* first_name, last_name
* address_line1, address_line2, address_city, address_state, address_zip

PUT /customer/<customer_id>/ to edit a customer

DELETE /customer/<customer_id>/ to delete a customer

GET /customer/<customer_id>/ to get customer detail by ID

GET /customer/ to list all customers

GET /postcard/?customer_id=123 to list postcards by customer_id
Include lob ID, lob URL for rendered postcard, expected_delivery_date, postcard creation date
There will be no authentication authorization logic


## Frontend

Customer list page, shows a table of all customer
* Each row will show customer full name, address, number of postcards for this customer
* Edit button on each row. Click it to show a form to edit a customer, PUT /customer/<customer_id> to backend
* Delete button on each row. Click it will DELETE /customer/<customer_id> to backend
* Create button. Click it to show a form to create a customer, POST /customer/ to backend
* Click the customer name to go to customer detail page described below

Customer detail page
* Shows customer full name, address
* Shows a table of postcards created for this customer.
* Each row show the lob ID, URL for rendered postcard, expected delivery date, creation timestamp


## Flask custom command

Make API call to lob to create postcard for each customer on anniversary.
Run this via a cronjob on a daily basis.