@app.route('/add-layer', methods=['POST'])
def add_layer():
    geojson = request.get_json()

    # Convert GeoJSON to ArcGIS JSON
    arcgis_json = convert_geojson_to_arcgis_json(geojson)  # You'll need to implement this function

    # Add the GeoJSON layer to the ArcGIS Feature Service
    response = requests.post('https://services6.arcgis.com/QHir1urgnGYroCLG/arcgis/rest/services/PG_versioneret_110624/FeatureServer/0/addFeatures', {
        'features': json.dumps(arcgis_json)
    })

    if response.status_code == 200:
        return jsonify(message='Layer successfully added'), 200
    else:
        return jsonify(error='Failed to add layer to ArcGIS Feature Service'), 500
