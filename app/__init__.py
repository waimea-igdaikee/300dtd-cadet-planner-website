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
from app.helpers.auth    import login_required, admin_required
from app.helpers.time    import init_datetime, utc_timestamp, utc_timestamp_now

import datetime
from math import ceil

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
def login():
    return render_template("pages/login.jinja")

#-----------------------------------------------------------
# Allocations page route
#-----------------------------------------------------------
@app.get("/allocations")
@login_required
def allocations():
    # The user id is used to display which roles the user themselves is allocated
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
            ORDER BY role_name
        """
        params=[]
        result_allocations = client.execute(sql_allocations, params)
        allocations = result_allocations.rows


        # Filter the dates into either this week, next week, or discard them.
        # I'm not using SQL to filter them as this would require 2 sql queries for the 2 weeks.
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
    
@app.get("/allocate_admin")
@admin_required
def allocate_admin():
    # Retrieve the neccesary data to make the allocation query
    remove = request.args.get("remove")
    if remove == "1":
        user_id = "NULL"
    else:
        user_id = request.args.get("user_id")
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
# Route for instantiating all parade roles for this or next week
#-----------------------------------------------------------
@app.get("/allocations_create")
@login_required
def allocations_create():
    # Retrieve the neccesary data to make the allocation query
    week = int(request.args.get("week"))


    # Calculate how many days away the coming `day 1` (tuesday) is
    days_away = (1 - datetime.date.today().weekday() + 7) % 7
    if week == 1:
        days_away += 7 # Add a week if we are wanting the next tuesday after this tuesday

    date_to_insert = datetime.date.today() + datetime.timedelta(days=days_away)
    date_to_insert = date_to_insert.isoformat() # Convert to string
    
    with connect_db() as client:
        # Update the DB
        sql = """
            INSERT INTO allocations (role, date, user)
            SELECT roles.id, ?, NULL
            FROM roles
        """

        params=[date_to_insert]
        client.execute(sql, params)
        return redirect("/allocations")


#-----------------------------------------------------------
# Roles page route
# - Passes in a list of roles
#-----------------------------------------------------------
@app.get("/roles")
@login_required
def roles():
    with connect_db() as client:
        # Get all roles from the DB
        sql = """
            SELECT *

            FROM roles

            ORDER BY roles.name ASC
        """
        params=[]
        result = client.execute(sql, params)
        roles = result.rows

        # Show them on the page
        return render_template("pages/roles.jinja", roles=roles)
    
@app.get("/role_delete")
@admin_required 
def role_delete():
    role = int(request.args.get("role"))
    with connect_db() as client:
        # Get all the things from the DB
        sql = """
            DELETE FROM roles
            WHERE id=?
        """
        params=[role]
        client.execute(sql, params)

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
        flash(f"Role deleted", "success")
        return render_template("pages/roles.jinja", roles=roles)
    
    

#-----------------------------------------------------------
# Person Stats page route
# - Passes in a nested dictionary with a sub-dictionary for how many times
#   and how many weeks it's been since this user did each role
# - Only includes allocation data from the past 10 weeks
#-----------------------------------------------------------
@app.get("/stats_personal")
@login_required
def stats_personal():

    # Collect some data for the SQL query and further processing
    user_id = session["user_id"]
    current_date = datetime.date.today()
    current_date_string = current_date.isoformat()

    with connect_db() as client:
        # Count how many times the current user has done each role over the past 10 weeks.
        sql_allocations = """
            SELECT roles.name AS name,
                COUNT(allocations.user) AS count,
                MAX(allocations.date) AS last_date

            FROM roles
            LEFT JOIN allocations
                ON allocations.role = roles.id
                AND allocations.user = ?
                AND allocations.date < ?
            GROUP BY roles.name
        """
        params=[user_id, current_date_string]
        result = client.execute(sql_allocations, params)
        allocations_count_last_date = result.rows # Has the date of the last time this role was done by this user

        allocations_count_weeks_since = {} # This nested dictionary will hold a sub-dictionary for each role. 
                                           # These sub-dictionaries will hold how many times and weeks since this role was done by this user.
        
        for role in allocations_count_last_date:

            count = role["count"]

            allocations_count_weeks_since[role["name"]] = {} # Create a sub dictionary for each role

            # Calculate whether the user has done this role in the past 10 weeks, and if so, how many weeks it's been
            if role["last_date"]:
                last_date = datetime.datetime.strptime(role["last_date"], '%Y-%m-%d').date() # Convert the string to a date object
                weeks_since = ceil((current_date - last_date).days / 7) # Figure out how many weeks it's been, rounding up.

                # Use the correct grammar depending on how many long it's been
                if weeks_since > 1:
                    last_done = f"{weeks_since} weeks ago"
                elif weeks_since == 1:
                    last_done = "Last week"
                else: # Time data gets lost when converting to date, so this is if the user is doing this role later today
                    last_done = "Never"
            else:
                last_done = "Never"

            # Put this data in the dictionary
            allocations_count_weeks_since[role["name"]]["count"] = count
            allocations_count_weeks_since[role["name"]]["weeks_since"] = last_done

        return render_template("pages/stats_personal.jinja", allocations_count=allocations_count_weeks_since)
    
#-----------------------------------------------------------
# Route for a user editing their name
# - Restricted to logged in users
#-----------------------------------------------------------
@app.post("/user_name_edit")
@login_required
def user_name_edit():
    # Get the data from the form
    name  = request.form.get("name")

    # Sanitise the text input
    name = html.escape(name)

    user_id = session['user_id']

    with connect_db() as client:
        # Add the thing to the DB
        sql = """
            UPDATE users

            SET name=?

            WHERE id=?
        """
        params = [name, user_id]
        client.execute(sql, params)

        # Updat the session to reflect the name change
        session["user_name"] = name

        # Go back to the home page
        flash(f"Display name updated to '{name}'", "success")
        return redirect("/stats_personal")
    

#-----------------------------------------------------------
# Unit Stats page route
# - Passes in list of roles
# - Passes in nested dictionary of {each user : {each role : allocation count}}
# - Only includes allocations over the past 10 weeks
#-----------------------------------------------------------
@app.get("/stats_unit")
@admin_required
def stats_unit():

    with connect_db() as client:

        # Get all the roles for display as table headings
        sql = """
            SELECT name,
                   abbreviation

            FROM roles
            ORDER BY name
        """
        params=[]
        result = client.execute(sql, params)
        roles = result.rows

        # Get the count of times each user has done each role over the past 10 weeks
        current_date_string = datetime.date.today().isoformat()

        sql = """
            SELECT users.name AS user,
                roles.name AS role,
                COUNT(allocations.user) AS count
            FROM users
            CROSS JOIN roles
            LEFT JOIN allocations
                ON allocations.user = users.id
                AND allocations.role = roles.id
                AND allocations.date < ?
            GROUP BY users.id, roles.id
            ORDER BY user, role;
        """
        params=[current_date_string]
        result = client.execute(sql, params)
        allocations_count_rows = result.rows # There is one row for each combination of user and role

        allocations_count = {} # This nested dictionary will hold a sub-dictionary for each user. 
                               # These sub-dictionaries will hold {each role: allocation count}.

        # Convert the returned rows into a nested dictionary as described above. This allows easy iteration in jinja.
        for row in allocations_count_rows:
            user = row['user']
            role = row['role']
            count = row['count']

            # Make a sub-dictionary for this user if we haven't already
            if user not in allocations_count:
                allocations_count[user] = {}

            allocations_count[user][role] = count # Take the count from the row and put in the sub-dictionary

        return render_template("pages/stats_unit.jinja", roles=roles, allocations_count=allocations_count)


#-----------------------------------------------------------
# Route for adding a role, using data posted from a form
# - Restricted to logged in users
#-----------------------------------------------------------
@app.post("/role_new")
@admin_required
def role_new():
    # Get the data from the form
    name  = request.form.get("name")
    abbreviation = request.form.get("abbreviation")
    description = request.form.get("description")

    # Sanitise the text inputs
    name = html.escape(name)
    abbreviation = html.escape(abbreviation)
    description=html.escape(description)

    with connect_db() as client:
        # Add the thing to the DB
        sql = "INSERT INTO roles (name, abbreviation, description) VALUES (?, ?, ?)"
        params = [name, abbreviation, description]
        client.execute(sql, params)

        # Go back to the home page
        flash(f"Role '{name}' added", "success")
        return redirect("/roles")
    

#-----------------------------------------------------------
# Route for editing a role, using data posted from a form
# - Restricted to logged in users
#-----------------------------------------------------------
@app.post("/role_edit")
@admin_required
def role_edit():
    # Get the data from the form
    name  = request.form.get("name")
    abbreviation = request.form.get("abbreviation")
    description = request.form.get("description")
    role = request.form.get("role")

    # Sanitise the text inputs
    name = html.escape(name)
    abbreviation = html.escape(abbreviation)
    description=html.escape(description)
    

    with connect_db() as client:
        # Add the thing to the DB
        sql = """
            UPDATE roles

            SET name=?,
                abbreviation=?,
                description=?

            WHERE roles.id=?
        """
        params = [name, abbreviation, description, role]
        client.execute(sql, params)

        # Go back to the home page
        flash(f"Role '{name}' updated", "success")
        return redirect("/roles")




#-----------------------------------------------------------
# User registration form route
#-----------------------------------------------------------
@app.get("/register")
def register():
    return render_template("pages/register.jinja")


#-----------------------------------------------------------
# Route for adding a user when registration form submitted
#-----------------------------------------------------------
@app.post("/add_user")
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
            return redirect("/")

        # Found an existing record, so prompt to try again
        flash("Username already exists. Try again...", "error")
        return redirect("/register")


#-----------------------------------------------------------
# Route for processing a user login
#-----------------------------------------------------------
@app.post("/login_user")
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

