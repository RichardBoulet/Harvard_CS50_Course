import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd
app.jinja_env.globals.update(usd=usd, lookup=lookup, int=int)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")




# Get the useres portfolio and portfolio value
@app.route("/")
@login_required
def index():

    # Get cash amount
    user_info = db.execute('SELECT cash from users WHERE id=:id', id = session['user_id'])

    cash = user_info[0]['cash']

    # User portfolio
    portfolio = db.execute('SELECT stock, quantity FROM portfolio')

    if not portfolio:
        return apology('You have no holdings')

    grand_total = cash

    # Get portfolio value
    for stock in portfolio:
        price = lookup(stock['stock'])['price']
        total = stock['quantity'] * price
        stock.update({'price': price, 'total':total})
        grand_total += total

    return render_template('index.html', stocks = portfolio, cash = cash, total = grand_total)


# Buys shares of stocks
@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():

    if request.method == "POST":

        if (not request.form.get("stock")) or (not request.form.get("shares")):
            return apology("Provide stock and number of shares")


        if int(request.form.get("shares")) <= 0:
            return apology("Provide correct number of shares")


        quote = lookup(request.form.get("stock"))

        if quote == None:
            return apology("Stock symbol not valid")

        cost = int(request.form.get("shares")) * quote['price']
        result = db.execute("SELECT cash FROM users WHERE id=:id", id=session["user_id"])

        if cost > result[0]["cash"]:
            return apology("Not enough funds")

        db.execute("UPDATE users SET cash=cash-:cost WHERE id=:id", cost=cost, id = session["user_id"])

        add_transaction = db.execute("INSERT INTO transactions (user_id, stock, quantity, price, date) VALUES (:user_id, :stock, :quantity, :price, :date)", user_id = session["user_id"], stock=quote["symbol"], quantity=int(request.form.get("shares")), price=quote['price'], date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        curr_portfolio = db.execute("SELECT quantity FROM portfolio WHERE stock=:stock", stock = quote["symbol"])

        if not curr_portfolio:
            db.execute("INSERT INTO portfolio (stock, quantity) VALUES (:stock, :quantity)", stock = quote["symbol"], quantity = int(request.form.get("shares")))

        else:
            db.execute("UPDATE portfolio SET quantity=quantity+:quantity WHERE stock=:stock", quantity = int(request.form.get("shares")), stock=quote["symbol"])

        return redirect(url_for("index"))

    else:
        return render_template("buy.html")





# Get the users history of transactions
@app.route("/history")
@login_required
def history():

    # Get user transactions
    portfolio = db.execute("SELECT stock, quantity, price, date FROM transactions WHERE user_id=:id", id = session["user_id"])

    if not portfolio:
        return apology("No transactions")

    return render_template("history.html", stocks=portfolio)





@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")





@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")





# Code to check ticker symbol and return html page containing stock info, or return apology
@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():

    if request.method == 'POST':

        # Check if stock symbol entered
        if not request.form.get('ticker'):
            return apology('Please enter a stock ticker')

        quote = lookup(request.form.get('ticker'))

        # Check if ticker is valid
        if quote == None:
            return apology('Not a valid ticker symbol')

        else:
            return render_template('stock.html', quote = quote)

    else:
        return render_template('quote.html')






# Registering a new user section
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == 'POST':

        # User input variables
        user = request.form.get('username')
        password = request.form.get('password')
        confirm = request.form.get('confirmation')

        if not user:
            return apology('You must provide a username', 403)

        if not password:
            return apology('You must provide a password', 403)

        if not confirm:
            return apology('You must provide matching passwords', 418)

        if not password == confirm:
            return apology('Passwords must match', 418)


        # Check database for username
        username = db.execute('SELECT username FROM users WHERE username = :username', username = user)

        # Check to make sure username not already in use
        if len(username) == 1:
            return apology('Username is already taken!', 403)

        else:
            new_user = db.execute('INSERT INTO users (username, hash) VALUES (:username, :password)', username = user, password = generate_password_hash(password, method = 'pbkdf2:sha256', salt_length = 8))

            if new_user:
                session['user_id'] = new_user

            # flash info for new user
            flash(f'Registered as {user}')

            # go to homepage
            return redirect('/')

    else:
        return render_template('register.html')





@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():

    if request.method == "POST":

        # Check if shares and stock symbol given
        if (not request.form.get("stock")) or (not request.form.get("shares")):
            return apology("Provide stock name and number of shares")

        # Check number of shares is correct
        if int(request.form.get("shares")) <= 0:
            return apology("Provide proper share amount")

        available = db.execute("SELECT quantity FROM portfolio WHERE :stock=stock", stock=request.form.get("stock"))


        # Check if amount of shares can be sold based on portfolio
        if int(request.form.get("shares")) > available[0]['quantity']:
            return apology("You cannot sell that many shares")


        quote = lookup(request.form.get("stock"))

        if quote == None:
            return apology("Stock symbol not valid, please try again")

        # Cost for transaction
        cost = int(request.form.get("shares")) * quote['price']

        # Update user cash
        db.execute("UPDATE users SET cash=cash+:cost WHERE id=:id", cost = cost, id = session["user_id"])

        # Put transactions on DB
        add_transaction = db.execute("INSERT INTO transactions (user_id, stock, quantity, price, date) VALUES (:user_id, :stock, :quantity, :price, :date)", user_id = session["user_id"], stock = quote["symbol"], quantity=-int(request.form.get("shares")), price=quote['price'], date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        # Update quantity of stock owned
        db.execute("UPDATE portfolio SET quantity=quantity-:quantity WHERE stock=:stock", quantity = int(request.form.get("shares")), stock = quote["symbol"])

        return redirect(url_for("index"))


    else:
        # pull all transactions belonging to user
        portfolio = db.execute("SELECT stock FROM portfolio")

        return render_template("sell.html", stocks=portfolio)




# Code to add funds on seperate page

@app.route("/add", methods=["GET", "POST"])
@login_required
def add():

    if request.method == "POST":

        # Check funds amount is correct
        if int(request.form.get("add")) <= 1:
            return apology("Provide proper fund amount")

        added_cash = int(request.form.get("add"))

        # Update user cash
        db.execute("UPDATE users SET cash=cash+:added_cash WHERE id=:id", added_cash = added_cash, id = session["user_id"])


        return redirect(url_for("index"))

    else:
        return render_template('add.html')




def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
