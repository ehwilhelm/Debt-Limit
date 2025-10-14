import requests
import json

# Your API token
token = "d6027311765c9070fe95852811d21d10a75c6657"  # Replace with your actual token

# Set up headers
headers = {
    'Authorization': f'Token {token}'
}

# Query 1: Search in filing_specific_lobbying_issues
params1 = {
    'filing_specific_lobbying_issues': ["debt limit", "debt ceiling"],
    'filing_year': ['2008','2009']
}

# Query 2: Search in description
params2 = {
    'description': ["debt limit", "debt ceiling"],
    'filing_year': ['2008','2009']
}

# Make both requests
response1 = requests.get(
    'https://lda.senate.gov/api/v1/filings/',
    headers=headers,
    params=params1
)

response2 = requests.get(
    'https://lda.senate.gov/api/v1/filings/',
    headers=headers,
    params=params2
)

# Check if both requests were successful
if response1.status_code == 200 and response2.status_code == 200:
    # Get results from both queries
    results1 = response1.json().get('results', [])
    results2 = response2.json().get('results', [])
    
    # Combine results and remove duplicates based on filing_uuid
    seen_ids = set()
    combined_results = []
    
    for result in results1 + results2:
        filing_id = result.get('filing_uuid')
        if filing_id not in seen_ids:
            seen_ids.add(filing_id)
            combined_results.append(result)
    
    # Create new data structure matching API response format
    data = {
        'count': len(combined_results),
        'results': combined_results
    }
    
    # Print the results nicely formatted
    print(f"Total unique results: {data.get('count')}")
    print(f"Results from query 1 (filing_specific_lobbying_issues): {len(results1)}")
    print(f"Results from query 2 (description): {len(results2)}")
    print("\n" + "="*50)
    
    # Print each filing
    for filing in data.get('results', []):
        print(f"\nFiling ID: {filing.get('filing_uuid')}")
        print(f"Year: {filing.get('filing_year')}")
        print(f"Registrant: {filing.get('registrant', {}).get('name')}")
        print(f"Client: {filing.get('client', {}).get('name')}")
        print("-" * 50)
    
    # Save full response to a JSON file
    with open('lda_results3.json', 'w') as f:
        json.dump(data, f, indent=2)
    print("\nFull results saved to 'lda_results3.json'")
    
else:
    if response1.status_code != 200:
        print(f"Error in Query 1 (filing_specific_lobbying_issues): {response1.status_code}")
        print(response1.text)
    if response2.status_code != 200:
        print(f"Error in Query 2 (description): {response2.status_code}")
        print(response2.text)