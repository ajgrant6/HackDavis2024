from app import *
from functions.scrapers.locationScraper import *
from functions.lgbtPolicy import *
from functions.abortionAccess import *
from functions.scrapers.jobDescScraper import *
from functions.resumeCoach import *
from functions.stateID import *
from PyPDF2 import *
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import os
import json
from io import BytesIO

from flask_cors import CORS, cross_origin
# Apply CORS to whole app or just one route
# NEEDED FOR REACT TO WORK
CORS(app)

load_dotenv()

googleAPI = os.getenv("GOOGLEAPI")
walkscoreAPI = os.getenv("WALKSCOREAPI")
equalDexAPI = os.getenv("EQUALDEXAPI")
#from flask_login import current_user, login_required

def extract_text_from_pdf(pdf_content):
    pdf_reader = PdfReader(BytesIO(pdf_content))
    text = ''
    for page_num in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page_num].extract_text()
    return text

@app.route("/", methods=["GET"])
@app.route("/login", methods=["GET"])
def index():

#	if current_user.is_authenticated:
#		return redirect(url_for("application"))
	return render_template("index.html")



@app.route("/resumetest", methods=["GET"])
def resumetest():
	return render_template("resumetest.html")

#@app.route("/app", methods=["GET"])
#@login_required
#def application():
#
#	return render_template("app.html")	
#


@app.route('/api/getInfo', methods=['POST'])
def api_get_location():
    # Initialize a dictionary with all keys set to "No Data"
    response_data = {
        "abortion_policy": "No Data",
        "walkscore": "No Data",
        "walk_description": "No Data",
        "bike_description": "No Data",
        "bike_score": "No Data",
        "transit_description": "No Data",
        "transit_summary": "No Data",
        "transit_score": "No Data",
        "ei_value": "No Data",
        "legal_ei_value": "No Data",
        "po_ei_value": "No Data",
        "employment_discrimination": "No Data",
        "housing_discrimination": "No Data",
        "transrights_legality": "No Data",
        "genderafirm_legality": "No Data",
        "lat": "No Data",
        "lon": "No Data",
        "state_id": "No Data"
    }

    if request.is_json:
        data = request.json
        if 'link' in data:
            link = data['link']
            location = get_location(link)
            if location == "not found":
                return jsonify({'error': 'Location not found'}), 404

            # Use Google Maps API to get structured address components
            try:
                geocode_url = f'https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={googleAPI}'
                response = requests.get(geocode_url)
                if response.status_code == 200:
                    geocode_data = response.json()
                    if len(geocode_data['results']) > 0:
                        address_components = geocode_data['results'][0]['address_components']
                        # Extract the state ID from the address components
                        state_id = next((component['short_name'] for component in address_components if 'administrative_area_level_1' in component['types']), None)
                        if state_id:
                            response_data["state_id"] = state_id
                            response_data["lat"] = geocode_data['results'][0]['geometry']['location']['lat']
                            response_data["lon"] = geocode_data['results'][0]['geometry']['location']['lng']
                        else:
                            return jsonify({'error': 'State ID not found in location data'}), 400
                    else:
                        return jsonify({'error': 'Geocode data not found for the location'}), 404
                else:
                    return jsonify({'error': 'Failed to retrieve geocode data'}), response.status_code
            except Exception as e:
                print(f"Failed to fetch geocode data: {e}")
                return jsonify({'error': 'An error occurred while fetching geocode data'}), 500

            # Fetch data from EqualDex API
            try:
                url = "https://www.equaldex.com/api/region"
                querystring = {"regionid": "US-" + state_id, "formatted": "false", "apiKey": equalDexAPI}
                headers = {"Accept": "application/json"}
                response = requests.get(url, headers=headers, params=querystring)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    pre_content = soup.find('pre').text
                    state_data = json.loads(pre_content)

                    response_data["ei_value"] = state_data['regions']['region']['ei']
                    response_data["legal_ei_value"] = state_data['regions']['region']['ei_legal']
                    response_data["po_ei_value"] = state_data['regions']['region']['ei_po']
                    response_data["employment_discrimination"] = state_data['regions']['region']['issues']['employment-discrimination']['current_status']['description']
                    response_data["housing_discrimination"] = state_data['regions']['region']['issues']['housing-discrimination']['current_status']['description']
                    response_data["transrights_legality"] = state_data['regions']['region']['issues']['changing-gender']['current_status']['value']
                    response_data["genderafirm_legality"] = state_data['regions']['region']['issues']['gender-affirming-care']['current_status']['value']
                else:
                    print("Error:", response.status_code)
            except Exception as e:
                print(f"Failed to fetch EqualDex data: {e}")

            # Fetch abortion policy
            try:
                response_data["abortion_policy"] = abortionAccess(state_id)
            except Exception as e:
                print(f"Failed to fetch abortion policy: {e}")

            # Fetch WalkScore data
            try:
                if response_data["lat"] != "No Data" and response_data["lon"] != "No Data":
                    walkscore_url = f"https://api.walkscore.com/score?format=json&lat={response_data['lat']}&transit=1&bike=1&wsapikey={walkscoreAPI}&lon={response_data['lon']}"
                    response = requests.get(walkscore_url)
                    if response.status_code == 200:
                        walkscore_data = response.json()
                        response_data["walkscore"] = walkscore_data['walkscore']
                        response_data["walk_description"] = walkscore_data['description']
                        response_data["bike_description"] = walkscore_data['bike']['description']
                        response_data["bike_score"] = walkscore_data['bike']['score']
                        try:
                            response_data["transit_description"] = walkscore_data['transit']['description']
                            response_data["transit_summary"] = walkscore_data['transit']['summary']
                            response_data["transit_score"] = walkscore_data['transit']['score']
                        except KeyError:
                            response_data["transit_description"] = "No Transit"
                            response_data["transit_summary"] = "No public transit routes available nearby"
                            response_data["transit_score"] = 0
                    else:
                        print("Error:", response.status_code)
            except Exception as e:
                print(f"Failed to fetch WalkScore data: {e}")

            return jsonify(response_data)

        else:
            return jsonify({'error': 'Missing link parameter'}), 400
    else:
        return jsonify({'error': 'Request must be JSON'}), 400
    


@app.route('/api/getJobDescription', methods=['POST'])
def api_get_job_description():
	if request.is_json:
		data = request.json
		if 'link' in data:
			link = data['link']
			job_description = get_job_description(link)
			if job_description == "not found":
				return jsonify({'error': 'Job description not found'}), 404
			return jsonify({'job_description': job_description})
		else:
			return jsonify({'error': 'Missing link parameter'}), 400
	else:
		return jsonify({'error': 'Request must be JSON'}), 400
	


@app.route('/api/upload', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file and file.filename.endswith('.pdf'):
        # Read PDF content
        pdf_content = file.read()

        # Extract text from the uploaded PDF
        text = extract_text_from_pdf(pdf_content)

        # Store the text in sessionStorage
        return jsonify({'text': text})

    else:
        return jsonify({'error': 'Invalid file format'})
	


@app.route('/api/compareResume', methods=['POST'])
def compare_resume():
	if request.is_json:
		data = request.json
		
		if 'resume_text' in data and 'job_description' in data:
			resume = data['resume_text']
			job_description = data['job_description']
			response = resumeCoach(resume, job_description)
			return jsonify(response)
		else:
			return jsonify({'error': 'Missing resume or job_description parameter'}), 400
	else:
		return jsonify({'error': 'Request must be JSON'}), 400