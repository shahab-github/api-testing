import requests

# API endpoint for Terraform workspaces
api_url = "https://example.com/api/workspaces"

# Initialize pagination parameters
page = 1
per_page = 20  # Adjust as needed

all_workspaces = []

while True:
    # Make an API request with pagination parameters
    params = {
        "page": page,
        "per_page": per_page,
        # Add any other required parameters
    }

    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        workspaces = response.json()
        all_workspaces.extend(workspaces)

        # Check if there are more pages
        if len(workspaces) < per_page:
            break

        # Increment the page number for the next request
        page += 1
    else:
        print(f"Error fetching workspaces: {response.status_code}")
        break

# Now, all_workspaces contains all the fetched workspaces
print(all_workspaces)
