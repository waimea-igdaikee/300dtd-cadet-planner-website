#===========================================================
# YOUR PROJECT TITLE HERE
# YOUR NAME HERE
#-----------------------------------------------------------
# BRIEF DESCRIPTION OF YOUR PROJECT HERE
#===========================================================


from flask import Flask, render_template, request, flash, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import html

from app.helpers.session import init_session
from app.helpers.db      import connect_db
from app.helpers.errors  import init_error, not_found_error
from app.helpers.logging import init_logging
from app.helpers.auth    import login_required
from app.helpers.time    import init_datetime, utc_timestamp, utc_timestamp_now

import datetime

# Create the app
app = Flask(__name__)

# Configure app
init_session(app)   # Setup a session for messages, etc.
init_logging(app)   # Log requests
init_error(app)     # Handle errors and exceptions
init_datetime(app)  # Handle UTC dates in timestamps


#-----------------------------------------------------------
# User login page route
#-----------------------------------------------------------
@app.get("/")
def login_form():
    return render_template("pages/login.jinja")

#-----------------------------------------------------------
# Allocations page route
#-----------------------------------------------------------
@app.get("/allocations")
@login_required
def allocations():
    # The user id is used to display which roles the user themselves is allocated
    user_id = session["user_id"]
    current_date = datetime.date.today()

    with connect_db() as client:
        # Get all the future allocations from the DB
        sql_allocations = """
            SELECT allocations.date,
                   roles.id as role_id,
                   roles.name as role_name,
                   users.id as user_id,
                   users.name as user_name

            FROM allocations
            JOIN roles ON allocations.role = roles.id
            LEFT JOIN users on allocations.user = users.id
        """
        params=[]
        result_allocations = client.execute(sql_allocations, params)
        allocations = result_allocations.rows


        # Filter the dates into either this week, next week, or discard them
        allocations_this_week = []
        allocations_next_week = []
        for allocation in allocations:
            allocation_date = datetime.datetime.strptime(allocation["date"], '%Y-%m-%d').date()
            date_delta = (allocation_date - current_date).days
            if 0 <= date_delta < 7:
                allocations_this_week.append(allocation)
            elif 7 <= date_delta < 14:
                allocations_next_week.append(allocation)

        # Get all the users from the DB for the admin allocation dropdown menu
        sql_users = """
            SELECT users.id as id,
                   users.name as name
                
            FROM users
        """
        params=[]
        result_users = client.execute(sql_users, params)
        users = result_users.rows
        

        # And show them on the page
        return render_template(
            "pages/allocations.jinja",
            allocations_this_week=allocations_this_week, 
            allocations_next_week=allocations_next_week,
            users=users,
            user_id=user_id
        )
    
#-----------------------------------------------------------
# Route for processing a user allocating themselves
#-----------------------------------------------------------
@app.get("/allocate")
@login_required
def allocate():
    # Retrieve the neccesary data to make the allocation query
    remove = request.args.get("remove")
    if remove == "1":
        user_id = "NULL"
    else:
        user_id = session["user_id"]
    date = request.args.get("date")
    role = request.args.get("role")

    with connect_db() as client:
        # Update the DB
        sql = """
            UPDATE allocations
            SET user = ?
            WHERE date = ? AND role = ?
        """

        params=[user_id, date, role]
        client.execute(sql, params)
        return redirect("/allocations")
    

#-----------------------------------------------------------
# Route for processing an admin allocating a user
#-----------------------------------------------------------
@app.post("/allocation")
@login_required # Perhaps I should make an @admin_req'd
def allocate_admin():
    # Get the data from the form
    user_id  = request.form.get("user_id")
    date = request.form.get("date")
    role = request.form.get("role")

    with connect_db() as client:
        # Update the DB
        sql = """
            UPDATE allocations
            SET user = ?
            WHERE date = ? AND role = ?
        """

        params=[user_id, date, role]
        client.execute(sql, params)
        return redirect("/allocations")


#-----------------------------------------------------------
# Roles page route
#-----------------------------------------------------------
@app.get("/roles/")
@login_required
def show_all_roles():
    with connect_db() as client:
        # Get all the things from the DB
        sql = """
            SELECT *

            FROM roles

            ORDER BY roles.name ASC
        """
        params=[]
        result = client.execute(sql, params)
        roles = result.rows

        # And show them on the page
        return render_template("pages/roles.jinja", roles=roles)
    

#-----------------------------------------------------------
# Person Stats page route
# Filters previous allocations
#-----------------------------------------------------------
@app.get("/stats_personal")
@login_required
def stats_personal():
    # The user id is used to display which roles the user themselves is allocated
    user_id = session["user_id"]
    current_date = datetime.date.today()

    with connect_db() as client:
        # Get all the current user's allocations from the DB.
        sql = """
            SELECT allocations.date,
                   roles.id as role_id,
                   roles.name as role_name,
                   users.id as user_id

            FROM allocations
            JOIN roles ON allocations.role = roles.id
            JOIN users on allocations.user = users.id
            WHERE user_id = ?
        """
        params=[user_id]
        result = client.execute(sql, params)
        allocations = result.rows


        # Filter the dates into either this week, next week, or discard them
        allocations_past = []
        for allocation in allocations:
            allocation_date = datetime.datetime.strptime(allocation["date"], '%Y-%m-%d').date() # Extract a date object from the string
            if current_date > allocation_date:
                allocations_past.append(allocation)

        # And show them on the page
        return render_template("pages/stats_personal.jinja", allocations_past=allocations_past)
    

#-----------------------------------------------------------
# Unit Stats page route
# Filters previous allocations
#-----------------------------------------------------------
@app.get("/stats_unit")
@login_required
def stats_unit():
    # The user id is used to display which roles the user themselves is allocated
    user_id = session["user_id"]
    current_date = datetime.date.today()

    with connect_db() as client:
        # Get all the current user's allocations from the DB
        sql = """
            SELECT allocations.date,
                   roles.id as role_id,
                   roles.name as role_name,
                   users.id as user_id,
                   users.name as user_name

            FROM allocations
            JOIN roles ON allocations.role = roles.id
            JOIN users on allocations.user = users.id
        """
        params=[]
        result = client.execute(sql, params)
        allocations = result.rows


        # Filter the dates into either this week, next week, or discard them
        allocations_past = []
        for allocation in allocations:
            allocation_date = datetime.datetime.strptime(allocation["date"], '%Y-%m-%d').date() # Extract a date object from the string
            if current_date > allocation_date:
                allocations_past.append(allocation)

        # And show them on the page
        return render_template("pages/stats_unit.jinja", allocations_past=allocations_past)


#-----------------------------------------------------------
# Thing page route - Show details of a single thing
#-----------------------------------------------------------
@app.get("/thing/<int:id>")
def show_one_thing(id):
    with connect_db() as client:
        # Get the thing details from the DB, including the owner info
        sql = """
            SELECT things.id,
                   things.name,
                   things.price,
                   things.user_id,
                   users.name AS owner

            FROM things
            JOIN users ON things.user_id = users.id

            WHERE things.id=?
        """
        params = [id]
        result = client.execute(sql, params)

        # Did we get a result?
        if result.rows:
            # yes, so show it on the page
            thing = result.rows[0]
            return render_template("pages/thing.jinja", thing=thing)

        else:
            # No, so show error
            return not_found_error()


#-----------------------------------------------------------
# Route for adding a role, using data posted from a form
# - Restricted to logged in users
#-----------------------------------------------------------
@app.post("/role")
@login_required # Perhaps I should make an @admin_req'd
def add_a_thing():
    # Get the data from the form
    name  = request.form.get("name")
    description = request.form.get("description")

    # Sanitise the text inputs
    name = html.escape(name)
    description=html.escape(description)

    with connect_db() as client:
        # Add the thing to the DB
        sql = "INSERT INTO roles (name, description) VALUES (?, ?)"
        params = [name, description]
        client.execute(sql, params)

        # Go back to the home page
        flash(f"Role '{name}' added", "success")
        return redirect("/roles")


#-----------------------------------------------------------
# Route for deleting a thing, Id given in the route
# - Restricted to logged in users
#-----------------------------------------------------------
@app.get("/delete/<int:id>")
@login_required
def delete_a_thing(id):
    # Get the user id from the session
    user_id = session["user_id"]

    with connect_db() as client:
        # Delete the thing from the DB only if we own it
        sql = "DELETE FROM things WHERE id=? AND user_id=?"
        params = [id, user_id]
        client.execute(sql, params)

        # Go back to the home page
        flash("Thing deleted", "success")
        return redirect("/things")







#-----------------------------------------------------------
# User registration form route
#-----------------------------------------------------------
@app.get("/register")
def register_form():
    return render_template("pages/register.jinja")


#-----------------------------------------------------------
# Route for adding a user when registration form submitted
#-----------------------------------------------------------
@app.post("/add-user")
def add_user():
    # Get the data from the form
    name = request.form.get("name")
    username = request.form.get("username")
    password = request.form.get("password")

    with connect_db() as client:
        # Attempt to find an existing record for that user
        sql = "SELECT * FROM users WHERE username = ?"
        params = [username]
        result = client.execute(sql, params)

        # No existing record found, so safe to add the user
        if not result.rows:
            # Sanitise the name
            name = html.escape(name)

            # Salt and hash the password
            hash = generate_password_hash(password)

            # Add the user to the users table
            sql = "INSERT INTO users (name, username, password_hash) VALUES (?, ?, ?)"
            params = [name, username, hash]
            client.execute(sql, params)

            # And let them know it was successful and they can login
            flash("Registration successful", "success")
            return redirect("/allocations")

        # Found an existing record, so prompt to try again
        flash("Username already exists. Try again...", "error")
        return redirect("/register")


#-----------------------------------------------------------
# Route for processing a user login
#-----------------------------------------------------------
@app.post("/login-user")
def login_user():
    # Get the login form data
    username = request.form.get("username")
    password = request.form.get("password")

    with connect_db() as client:
        # Attempt to find a record for that user
        sql = "SELECT * FROM users WHERE username = ?"
        params = [username]
        result = client.execute(sql, params)

        # Did we find a record?
        if result.rows:
            # Yes, so check password
            user = result.rows[0]
            hash = user["password_hash"]

            # Hash matches?
            if check_password_hash(hash, password):
                # Yes, so save info in the session
                session["user_id"]   = user["id"]
                session["user_name"] = user["name"]
                session["admin"] = user["admin"]
                session["logged_in"] = True

                # And to the allocations landing page
                flash("Login successful", "success")
                return redirect("/allocations")

        # Either username not found, or password was wrong
        flash("Invalid credentials", "error")
        return redirect("/")


#-----------------------------------------------------------
# Route for processing a user logout
#-----------------------------------------------------------
@app.get("/logout")
def logout():
    # Clear the details from the session
    session.pop("user_id", None)
    session.pop("user_name", None)
    session.pop("logged_in", None)
    session.pop("admin", None)

    # And head back to the home page
    flash("Logged out successfully", "success")
    return redirect("/")

