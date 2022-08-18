# Shop

this project is a shop writen in python

## store App
  * models:
    * Customer: each user is a customer customer should have email and name
    * Product:  each product should have title and price you can set a image or it will use the defualt
    * Order: each order is for a customer and it has a date of creation and a boolean that it is done and a transaction
    * OrderItem: each order has many orderItems and each orderItem shows a product and it has the quantity of that product in this order 
    * ShippingAddress: shipping info for the order when it is done
  * Views:
    * productCreateView: this view is for creating product 
    * productUpdateView: this view is for updating product
    * productListView: it is the home page and shows all of the product it is paginated and if the number of products are more than 6 it will create another page for showing the rest of the products
    * cart: if user is logged in it will get the orders in the cart from data base else from cart cookie
    * checkout: if user is logged in can see this page and it shows the items in the cart
    * productDetailView: show the product separated in a page
    * updateItem: it will apply the update on the selected product
    * processOrder: it will make the transaction and save it in the data base
  * functions:
    * getCartSpec: returns the cart detail for anonymous user
    * getUserSpec: returns the order and cart detail for logged in user
    * mergeItems: if a user log in it will merger the products that were selected before loged in and the products were in the cart of the user
    * makeTransaction: it will save the transaction info in the data base 
    
## user App   
  * views: 
    * registerView: this view is for register and if user create an account it will create a customer 
    * loginView: this view is for login and if user logs in it will merge the items that were selected before login and the items were selected in the account by calling mergeItems func
    * LogoutViewCustom: this view is for logout
    
    
   
    
 
  

## superuser info
**username**: ali\
**password**: Passw0rd$96

(or you can create a new superuser by `python manage.py createsuperuser`)
