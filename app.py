from flask import Flask, jsonify
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow frontend requests from any origin

# Load data once at startup
df = pd.read_csv('data/geobias_matrix.csv')

@app.route('/')
def home():
    return jsonify({"message": "Welcome to GeoBias API"})


@app.route('/api/matrix', methods=['GET'])
def get_matrix():
    """Return the full GeoBias matrix as JSON."""
    return jsonify(df.to_dict(orient='records'))


@app.route('/api/countries', methods=['GET'])
def get_country_lists():
    """Return unique source and target country lists."""
    return jsonify({
        "sources": sorted(df["source_country"].dropna().unique().tolist()),
        "targets": sorted(df["target_country"].dropna().unique().tolist())
    })


@app.route('/api/filter/<source>/<target>', methods=['GET'])
def get_filtered(source, target):
    """Return filtered sentiment data."""
    filtered = df.copy()
    if source != "All":
        filtered = filtered[filtered["source_country"] == source]
    if target != "All":
        filtered = filtered[filtered["target_country"] == target]
    return jsonify(filtered.to_dict(orient='records'))
