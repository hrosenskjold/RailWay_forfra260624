from flask import Flask, render_template, request, jsonify
import requests
from arcgis.geometry import Geometry
from arcgis.features import Feature, FeatureSet
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    geojson = request.get_json()

    if not geojson:
        return jsonify(error='No GeoJSON data provided'), 400

    # Convert GeoJSON to ArcGIS Features
    arcgis_features = convert_geojson_to_arcgis_features(geojson)

    # Use proxy to add the features to the ArcGIS Feature Service
    response = proxy_request(arcgis_features)

    if response.status_code == 200:
        return jsonify(message='Layer successfully added'), 200
    else:
        return jsonify(error='Failed to add layer to ArcGIS Feature Service'), 500

def convert_geojson_to_arcgis_features(geojson):
    features = []
    for feature in geojson['features']:
        geometry = Geometry(feature['geometry'])
        attributes = feature['properties']
        arcgis_feature = Feature(geometry=geometry, attributes=attributes)
        features.append(arcgis_feature)

    return FeatureSet(features)

def proxy_request(arcgis_features):
    url = 'https://services6.arcgis.com/QHir1urgnGYroCLG/arcgis/rest/services/PG_versioneret_110624/FeatureServer/0/addFeatures'
    params = {
        'f': 'json',  # Specify JSON format
    }
    data = {
        'features': arcgis_features.as_dict(),
    }
    response = requests.post(url, params=params, json=data)
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
