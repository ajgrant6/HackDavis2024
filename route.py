from app import *
from locationScraper import *
import requests

#from flask_login import current_user, login_required

@app.route("/", methods=["GET"])
@app.route("/login", methods=["GET"])
def index():

#	if current_user.is_authenticated:
#		return redirect(url_for("application"))
	return render_template("index.html")

#@app.route("/app", methods=["GET"])
#@login_required
#def application():
#
#	return render_template("app.html")
#


@app.route('/api/getInfo', methods=['POST'])
def api_get_location():
	if request.is_json:
		data = request.json
		if 'link' in data:
			link = data['link']
			location = get_location(link)
			if location == "not found":
				return jsonify({'error': 'Location not found'}), 404
			

			# Replace 'LOCATION' with the location obtained from the API call
			geocode_url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + location + '&key=AIzaSyDQZG8GKpEqkx6_XCzrkrWGEH9D7a6hJXo'

			lat = 0
			lon = 0
			response = requests.get(geocode_url)
			if response.status_code == 200:
				geocode_data = response.json()
				lat = geocode_data['results'][0]['geometry']['location']['lat']
				lon = geocode_data['results'][0]['geometry']['location']['lng']
			else:
				return jsonify({'error': 'Failed to retrieve geocode data'}), response.status_code


			walkscore_url = f"https://api.walkscore.com/score?format=json&lat={lat}&transit=1&bike=1&wsapikey=e8a5a7dc1e1348952e542b644beb371c&lon={lon}"
			response = requests.get(walkscore_url)
			if response.status_code == 200:
				walkscore_data = response.json()
				# Extract the desired information from the walkscore_data
				# and use it as needed in your code
				walkscore = walkscore_data['walkscore']
				walk_description = walkscore_data['description']
				bike_description = walkscore_data['bike']['description']
				bike_score = walkscore_data['bike']['score']
				transit_description = walkscore_data['transit']['description']
				transit_summary = walkscore_data['transit']['summary']
				transit_score = walkscore_data['transit']['score']

				print("Walkscore:", walkscore)
				print("Walk Description:", walk_description)
				print("Bike Description:", bike_description)
				print("Bike Score:", bike_score)
				print("Transit Description:", transit_description)
				print("Transit Summary:", transit_summary)
				print("Transit Score:", transit_score)
			else:
				return jsonify({'error': 'Failed to retrieve walkscore data'}), response.status_code



			print("Location:", location)
			print("Latitude:", lat)
			print("Longitude:", lon)
			return jsonify({'location': location})
		else:
			return jsonify({'error': 'Missing link parameter'}), 400
	else:
		return jsonify({'error': 'Request must be JSON'}), 400