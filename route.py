from app import *
from functions.scrapers.locationScraper import *
from functions.lgbtPolicy import *
from functions.abortionAccess import *
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import os
import json

load_dotenv()

googleAPI = os.getenv("GOOGLEAPI")
walkscoreAPI = os.getenv("WALKSCOREAPI")
equalDexAPI = os.getenv("EQUALDEXAPI")
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


			url = "https://www.equaldex.com/api/region"
			querystring = {"regionid": "us-" + state_id, "formatted": "false", "apiKey": equalDexAPI}
			headers = {"Accept": "application/json"}

			response = requests.get(url, headers=headers, params=querystring)

			# Check if the request was successful
			if response.status_code == 200:
				# Parse the response text using BeautifulSoup
				soup = BeautifulSoup(response.text, 'html.parser')

				# Extract the content within <pre> tags
				pre_content = soup.find('pre').text

				# Parse the content as JSON
				state_data = json.loads(pre_content)


				ei_value = state_data['regions']['region']['ei']
				legal_ei_value = state_data['regions']['region']['ei_legal']
				po_ei_value = state_data['regions']['region']['ei_po']
				employment_discrimination = state_data['regions']['region']['issues']['employment-discrimination']['current_status']['description']
				housing_description = state_data['regions']['region']['issues']['housing-discrimination']['current_status']['description']
				transrights_legality = state_data['regions']['region']['issues']['changing-gender']['current_status']['value']
				genderafirm_legality = state_data['regions']['region']['issues']['gender-affirming-care']['current_status']['value']


			else:
				print("Error:", response.status_code)






			abortion_policy = abortionAccess(state_id)
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
			return jsonify({'abortion_policy': abortion_policy, 'walkscore': walkscore, 'walk_description': walk_description, 'bike_description': bike_description, 'bike_score': bike_score, 'transit_description': transit_description, 'transit_summary': transit_summary, "transit_score": transit_score, "ei_value": ei_value, "legal_ei_value": legal_ei_value, "po_ei_value": po_ei_value, "employment_discrimination": employment_discrimination, "housing_discrimination": housing_description, "transrights_legality": transrights_legality, "genderafirm_legality": genderafirm_legality})
		else:
			return jsonify({'error': 'Missing link parameter'}), 400
	else:
		return jsonify({'error': 'Request must be JSON'}), 400