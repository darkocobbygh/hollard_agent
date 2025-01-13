from hollard import main as fetch_executive_data
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

# Fetch executive data at startup
executive_data = fetch_executive_data()

# Normalize executive data
normalized_executive_data = {normalize_text(position): name for position, name in executive_data.items()}

# Debug: Log the executive data
print("DEBUG: Executive Data Loaded:")
for position, name in executive_data.items():
    print(f"Position: {position} -> Name: {name}")
    print(f"Normalized Position: {normalize_text(position)}")

def process_query(query):
    """Process the user query and match it to an executive position."""
    normalized_query = normalize_text(query)

    # Debug: Log normalized query
    print(f"DEBUG: Normalized Query: {normalized_query}")

    # Check if the query matches any position
    for position, name in normalized_executive_data.items():
        if position in normalized_query:
            return name

    # If no match is found, return a message
    return "Sorry, I couldn't find anyone with that position."

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
