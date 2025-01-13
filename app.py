from flask import Flask, jsonify, request
import re
from hollard import main as fetch_executive_data

app = Flask(__name__)

# Abbreviations mapping
ABBREVIATIONS = {
    "ceo": "chief executive officer",
    "cfo": "chief financial officer",
    "cio": "chief information officer",
    "cto": "chief technology officer",
    "coo": "chief operating officer",
    "cmo": "chief marketing officer",
    "chro": "chief human resources officer",
}

# Function to normalize text
def normalize_text(text):
    """Normalize text by converting to lowercase, removing extra spaces, resolving abbreviations, and handling 'Group' prefix."""
    # Convert to lowercase for consistent matching
    text = text.lower()

    # Replace non-breaking spaces with regular spaces
    text = text.replace("\u00a0", " ")

    # Replace abbreviations with full forms
    for abbr, full_form in ABBREVIATIONS.items():
        text = re.sub(rf'\b{abbr.lower()}\b', full_form.lower(), text)

    # Remove special characters and extra spaces
    text = re.sub(r'\s+', ' ', text).strip()

    # Make "group" optional
    text = re.sub(r'\bgroup\b', '', text).strip()

    return text

# Fetch executive data at startup
executive_data = fetch_executive_data()

# Normalize executive data
normalized_executive_data = {normalize_text(position): name for position, name in executive_data.items()}

# Debug: Log the normalized executive data
print("DEBUG: Normalized Executive Data Loaded:")
for position, name in normalized_executive_data.items():
    print(f"Normalized Position: {position} -> Name: {name}")

@app.route('/get_executive', methods=['GET'])
def get_executive():
    """API to fetch executive information based on position."""
    position = request.args.get('position', '')

    # Normalize the input query
    normalized_position = normalize_text(position)

    # Debugging logs
    print(f"DEBUG: Original Query: {position}")
    print(f"DEBUG: Normalized Query: {normalized_position}")

    # Fetch executive name
    name = normalized_executive_data.get(normalized_position, "Position not found")
    return jsonify({"position": position, "name": name})

if __name__ == "__main__":
    app.run(debug=True)
