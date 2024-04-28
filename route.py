from app import *
from locationScraper import *
import requests
from dotenv import load_dotenv
import os

from flask_cors import CORS, cross_origin
# Apply CORS to whole app or just one route
# NEEDED FOR REACT TO WORK
CORS(app)

load_dotenv()

googleAPI = os.getenv("GOOGLEAPI")
walkscoreAPI = os.getenv("WALKSCOREAPI")

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
			
			state_id = location.split(',')[-1].strip()[:2]
			print(state_id)
			# Replace 'LOCATION' with the location obtained from the API call
			geocode_url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + location + '&key='	+ googleAPI

			lat = 0
			lon = 0
			response = requests.get(geocode_url)
			if response.status_code == 200:
				geocode_data = response.json()
				lat = geocode_data['results'][0]['geometry']['location']['lat']
				lon = geocode_data['results'][0]['geometry']['location']['lng']
			else:
				return jsonify({'error': 'Failed to retrieve geocode data'}), response.status_code


			walkscore_url = f"https://api.walkscore.com/score?format=json&lat={lat}&transit=1&bike=1&wsapikey={walkscoreAPI}&lon={lon}"
			response = requests.get(walkscore_url)
			if response.status_code == 200:
				walkscore_data = response.json()
				walkscore = walkscore_data['walkscore']
				walk_description = walkscore_data['description']
				bike_description = walkscore_data['bike']['description']
				bike_score = walkscore_data['bike']['score']
				transit_description = walkscore_data['transit']['description']
				transit_summary = walkscore_data['transit']['summary']
				transit_score = walkscore_data['transit']['score']
			else:
				return jsonify({'error': 'Failed to retrieve walkscore data'}), response.status_code
			return jsonify({'location': location, 'walkscore': walkscore, 'walk_description': walk_description, 'bike_description': bike_description, 'bike_score': bike_score, 'transit_description': transit_description, 'transit_summary': transit_summary, "transit_score": transit_score})
		else:
			return jsonify({'error': 'Missing link parameter'}), 400
	else:
		return jsonify({'error': 'Request must be JSON'}), 400