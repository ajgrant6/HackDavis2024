import time

from app import *

from flask_login import LoginManager, login_required, login_user, logout_user

# If there is no admin account, make a default one.
if User.query.filter_by(username="admin").first() == None:
	db.session.add(User("admin", "password", 0))
	db.session.commit()

loginManager = LoginManager()
loginManager.init_app(app)
loginManager.login_view = "login"

@loginManager.user_loader
def load_user(id: int):
	return User.query.get(id)

@app.route("/login", methods=["POST"])
def login():

	assert "username" in request.form.keys() and "password" in request.form.keys()
	user = User.login(request.form["username"], request.form["password"])

	if user == None:
		time.sleep(1)  # Prevent brute.
		return render_template("index.html", failed=True)

	login_user(user)
	return redirect(url_for("application"))

@app.route("/logout", methods=["GET"])
@login_required
def logout():

	logout_user()
	return render_template("index.html")

