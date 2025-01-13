import requests
import re

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
    text = re.sub(r'\s+', ' ', text).strip().lower()

    # Make "group" optional
    text = re.sub(r'\bgroup\b', '', text).strip()

    return text

# Function to fetch executive data from the Flask API
def fetch_executive_data(position):
    """Fetch executive data from the deployed Flask app."""
    url = f'https://hollard-copilot.onrender.com/get_executive?position={position}'
    try:
        response = requests.get(url)
        data = response.json()
        return data.get('name', 'Sorry, no executive found for that position.')
    except Exception as e:
        return f"Error fetching data: {str(e)}"

def process_query(query):
    """Process the user query and match it to an executive position."""
    normalized_query = normalize_text(query)
    
    # Debug: Log normalized query
    print(f"DEBUG: Normalized Query: {normalized_query}")
    
    # Fetch executive name from the API
    executive_name = fetch_executive_data(normalized_query)
    
    # Return executive name or a fallback message
    return executive_name

def main():
    """Main function to handle the conversation."""
    print("Welcome to the Hollard Executive Finder!")
    
    while True:
        query = input("Ask a question (or type 'exit' to quit): ").lower()
        
        # Exit condition
        if query == 'exit':
            break
        
        # Process the query
        response = process_query(query)
        print(response)

if __name__ == "__main__":
    main()
