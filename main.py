from flask import Flask, render_template, request, jsonify
import requests
import json
from geojson import Feature, FeatureCollection
from arcgis.geometry import Geometry

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    geojson = request.get_json()

    # Convert GeoJSON to ArcGIS JSON
    arcgis_json = convert_geojson_to_arcgis_json(geojson)

    # Add the GeoJSON layer to the ArcGIS Feature Service
    response = requests.post(
        'https://services6.arcgis.com/QHir1urgnGYroCLG/arcgis/rest/services/PG_versioneret_110624/FeatureServer/0/addFeatures',
        json={
            'features': arcgis_json['features']
        }
    )

    if response.status_code == 200:
        return jsonify(message='Layer successfully added'), 200
    else:
        return jsonify(error='Failed to add layer to ArcGIS Feature Service'), 500

def convert_geojson_to_arcgis_json(geojson):
    features = []
    for feature in geojson['features']:
        geom = Geometry(feature['geometry'])
        arcgis_feature = {
            'geometry': geom,
            'attributes': feature['properties']
        }
        features.append(arcgis_feature)
    return {'features': features}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
