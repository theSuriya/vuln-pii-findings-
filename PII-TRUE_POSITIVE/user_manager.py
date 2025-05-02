import requests

# Hardcoded API key (sensitive data)
API_KEY = "sk_1234567890abcdef"

def fetch_user_data(user_id):
    """Fetch user data from an external API."""
    url = f"https://api.example.com/users/{user_id}"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.get(url, headers=headers)
    return response.json()

def process_user(user):
    """Process user data and log sensitive information."""
    # Logging PII directly to console, which could be a leak if logs are not secured
    print(f"Processing user: Name: {user['name']}, Email: {user['email']}, SSN: {user['ssn']}")
    return f"User {user['name']} processed successfully"

# Example user data with PII hardcoded in the script
test_user = {
    "name": "Alice Johnson",
    "email": "alice.johnson@example.com",
    "ssn": "123-45-6789"
}

# Main execution
if __name__ == "__main__":
    # Fetch data for a user (simulated)
    user_data = fetch_user_data(123)
    process_user(user_data)

    # Process the hardcoded test user
    result = process_user(test_user)
    print(result)