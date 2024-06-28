from flask import Flask, render_template, request, jsonify
import requests
import arcgisbinding

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
    response = requests.post('https://services6.arcgis.com/QHir1urgnGYroCLG/arcgis/rest/services/PG_versioneret_110624/FeatureServer/0/addFeatures', {
        'features': json.dumps(arcgis_json)
    })

    if response.status_code == 200:
        return jsonify(message='Layer successfully added'), 200
    else:
        return jsonify(error='Failed to add layer to ArcGIS Feature Service'), 500

def convert_geojson_to_arcgis_json(geojson):
    # Convert GeoJSON to ArcGIS JSON
    arcgis_json = arcgisbinding.arc.write(geojson)

    return arcgis_json

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
