import requests
import json

# Your API token
token = "d6027311765c9070fe95852811d21d10a75c6657"  # Replace with your actual token

# Set up headers
headers = {
    'Authorization': f'Token {token}'
}

# Set up query parameters
params = {
    'filing_specific_lobbying_issues': ["public debt"],
    'filing_year': ['2008', '2009']
}

# Make the request to the filings endpoint
response = requests.get(
    'https://lda.senate.gov/api/v1/filings/',
    headers=headers,
    params=params
)

# Check if request was successful
if response.status_code == 200:
    data = response.json()
    
    # Print the results nicely formatted
    print(f"Total results: {data.get('count', 'N/A')}")
    print(f"\nNumber of results on this page: {len(data.get('results', []))}")
    print("\n" + "="*50)
    
    # Print each filing
    for filing in data.get('results', []):
        print(f"\nFiling ID: {filing.get('filing_uuid')}")
        print(f"Year: {filing.get('filing_year')}")
        print(f"Registrant: {filing.get('registrant', {}).get('name')}")
        print(f"Client: {filing.get('client', {}).get('name')}")
        print("-" * 50)
    
    # Save full response to a JSON file
    with open('lda_results.json', 'w') as f:
        json.dump(data, f, indent=2)
    print("\nFull results saved to 'lda_results.json'")
    
else:
    print(f"Error: {response.status_code}")
    print(response.text)