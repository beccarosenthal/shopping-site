"""Ubermelon shopping application Flask server.

Provides web interface for browsing melons, seeing detail about a melon, and
put melons in a shopping cart.

Authors: Joel Burton, Christian Fernandez, Meggie Mahnken, Katie Byers.
"""

from flask import Flask, render_template, redirect, flash, session
import jinja2

import melons

app = Flask(__name__)

# A secret key is needed to use Flask sessioning features

app.secret_key = 'this-should-be-something-unguessable...whoops'

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.

app.jinja_env.undefined = jinja2.StrictUndefined


@app.route("/")
def index():
    """Return homepage."""

    return render_template("homepage.html")


@app.route("/melons")
def list_melons():
    """Return page showing all the melons ubermelon has to offer"""

    melon_list = melons.get_all()
    return render_template("all_melons.html",
                           melon_list=melon_list)


@app.route("/melon/<melon_id>")
def show_melon(melon_id):
    """Return page showing the details of a given melon.

    Show all info about a melon. Also, provide a button to buy that melon.
    """

    melon = melons.get_by_id(melon_id)
    return render_template("melon_details.html",
                           display_melon=melon)


@app.route("/cart")
def show_shopping_cart():
    """Display content of shopping cart."""

        #
    # Make sure your function can also handle the case wherein no cart has
    # been added to the session
    cart_dict = session["cart"]

    melon_ordered = []
    order_total = 0
    
    for melon in cart_dict:
        #get instance of melon object
        melon_object = melons.get_by_id(melon)
        #cost multiples price of melon with qty in cart
        cost = melon_object.price * cart_dict[melon]
        #cost added as attribute

        melon_object.cost = cost
        
        order_total += cost

        #make pretty price to display when we print cart
        display_price = melon_object.price_str()
        melon_object.display_price = display_price

        display_cost = "${:.2f}".format(melon_object.cost)
        melon_object.display_cost = display_cost

        melon_object.qty = cart_dict[melon]

        melon_ordered.append(melon_object)

    session["order_total"] = "${:.2f}".format(order_total)

    return render_template("cart.html", total_cost=order_total, 
                                        list_of_melon_objects=melon_ordered)


@app.route("/add_to_cart/<melon_id>")
def add_to_cart(melon_id):
    """Add a melon to cart and redirect to shopping cart page.

    When a melon is added to the cart, redirect browser to the shopping cart
    page and display a confirmation message: 'Melon successfully added to
    cart'."""

    #if session dict has nothing in it, make a key called cart with blank dict value
    # session.setdefault("cart", {})

    #other way to do the same thing in line above:
    if "cart" not in session:
        session["cart"] = {}

    session["cart"][melon_id] = session["cart"].get(melon_id, 0) + 1

    flash("You added a melon to your cart!")

    # #bring user to the cart

    return redirect("/cart")


@app.route("/login", methods=["GET"])
def show_login():
    """Show login form."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site.

    Find the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session.
    """

    # TODO: Need to implement this!

    # The logic here should be something like:
    #
    # - get user-provided name and password from request.form
    # - use customers.get_by_email() to retrieve corresponding Customer
    #   object (if any)
    # - if a Customer with that email was found, check the provided password
    #   against the stored one
    # - if they match, store the user's email in the session, flash a success
    #   message and redirect the user to the "/melons" route
    # - if they don't, flash a failure message and redirect back to "/login"
    # - do the same if a Customer with that email doesn't exist

    return "Oops! This needs to be implemented"


@app.route("/checkout")
def checkout():
    """Checkout customer, process payment, and ship melons."""

    # For now, we'll just provide a warning. Completing this is beyond the
    # scope of this exercise.

    flash("Sorry! Checkout will be implemented in a future version.")
    return redirect("/melons")


if __name__ == "__main__":
    app.run(debug=True)
