from app import *
from functions.scrapers.locationScraper import *
from functions.lgbtPolicy import *
from functions.abortionAccess import *
from functions.scrapers.jobDescScraper import *
from functions.resumeCoach import *
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
				try:
					transit_description = walkscore_data['transit']['description']
					transit_summary = walkscore_data['transit']['summary']
					transit_score = walkscore_data['transit']['score']
				except KeyError:
					transit_description = "No Transit"
					transit_summary = "No public transit routes available nearby"
					transit_score = 0
			else:
				return jsonify({'error': 'Failed to retrieve walkscore data'}), response.status_code
			return jsonify({'abortion_policy': abortion_policy, 'walkscore': walkscore, 'walk_description': walk_description, 'bike_description': bike_description, 'bike_score': bike_score, 'transit_description': transit_description, 'transit_summary': transit_summary, "transit_score": transit_score, "ei_value": ei_value, "legal_ei_value": legal_ei_value, "po_ei_value": po_ei_value, "employment_discrimination": employment_discrimination, "housing_discrimination": housing_description, "transrights_legality": transrights_legality, "genderafirm_legality": genderafirm_legality, "lat": lat, "lon": lon})
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