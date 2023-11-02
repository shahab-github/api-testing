# import requests


# def get_workspace_tags(api_token, workspace_name):
#     # Define the Terraform Cloud API base URL
#     api_base_url = "https://app.terraform.io/api/v2/"

#     # Define the API URL to get the list of tags for the workspace
#     api_url = f"{api_base_url}workspaces/{workspace_name}/relationships/tags"

#     # Create a session with the API token in the headers
#     session = requests.Session()
#     session.headers.update({"Authorization": f"Bearer {api_token}"})

#     # Send a GET request to retrieve the list of tags
#     response = session.get(api_url)

#     if response.status_code == 200:
#         tags_data = response.json().get("data", [])
#         tags = [tag["attributes"]["name"] for tag in tags_data]
#         return tags
#     else:
#         print(f"Failed to retrieve tags for workspace '{workspace_name}'. Status code: {response.status_code}, Response: {response.text}")
#         return []

# # Example usage:
# api_token = ".atlasv1.rd2J0hsLwiSrapazpLmbbpMU2Rb9YscXNNbV1FEsAn5VRQLQJTnCiu0OOtmnf8TE8II"
# workspace_list = ["ws-dmk5RGphWNffAjaL1", "ws-FKrxt2QW5Lok6jKC"]

# for workspace in workspace_list:
#     tags = get_workspace_tags(api_token, workspace)
#     print("Workspace Tags:", tags)


import requests
import pandas as pd

class TerraformAPIError(Exception):
    pass

def get_workspace_tags(api_token, workspace_name):
    # Define the Terraform Cloud API base URL
    api_base_url = "https://app.terraform.io/api/v2/"

    # Define the API URL to get the list of tags for the workspace
    api_url = f"{api_base_url}workspaces/{workspace_name}/relationships/tags"

    # Create a session with the API token in the headers
    session = requests.Session()
    session.headers.update({"Authorization": f"Bearer {api_token}"})

    # Send a GET request to retrieve the list of tags
    response = session.get(api_url)

    if response.status_code == 200:
        tags_data = response.json().get("data", [])
        tags = [tag["attributes"]["name"] for tag in tags_data]
        return tags
    else:
        error_message = f"Failed to retrieve tags for workspace '{workspace_name}'. Status code: {response.status_code}, Response: {response.text}"
        raise TerraformAPIError(error_message)
    

def check_required_tags(api_token, workspace_id, required_tags):
    # Define the Terraform Cloud API base URL
    api_base_url = "https://app.terraform.io/api/v2/"

    # Define the API URL to get the list of tags for the workspace
    api_url = f"{api_base_url}workspaces/{workspace_id}/relationships/tags"

    # Create a session with the API token in the headers
    session = requests.Session()
    session.headers.update({"Authorization": f"Bearer {api_token}"})

    # Send a GET request to retrieve the list of tags
    response = session.get(api_url)

    if response.status_code == 200:
        tags_data = response.json().get("data", [])
        tag_names = [tag["attributes"]["name"] for tag in tags_data]

        missing_tags = set(required_tags) - set(tag_names)

        if not missing_tags:
            print(f"Workspace '{workspace_id}' has all the required tags: {', '.join(required_tags)}")
            return True
        else:
            print(f"Workspace '{workspace_id}' is missing the following required tags: {', '.join(missing_tags)}")
            return False
    else:
        print(f"Failed to retrieve tags for workspace '{workspace_id}'. Status code: {response.status_code}, Response: {response.text}")
        return False
    

def add_tags_to_workspace(api_token, workspace_id, tags):
    # Define the Terraform Cloud API base URL
    api_base_url = "https://app.terraform.io/api/v2/"

    # Define the API URL to add tags to the workspace
    api_url = f"{api_base_url}workspaces/{workspace_id}/relationships/tags"

    # Create a session with the API token in the headers
    session = requests.Session()
    session.headers.update({"Authorization": f"Bearer {api_token}", "Content-Type": "application/vnd.api+json"})

    # Prepare the JSON payload to add tags to the workspace
    payload = {
        "data": [
            {
                "type": "tags",
                "attributes": {"name": tag}
            } for tag in tags
        ]
    }

    # Send a POST request to add tags to the workspace
    response = session.post(api_url, json=payload)

    if response.status_code == 204:
        print(f"Tags added to workspace '{workspace_id}' successfully.")
    else:
        error_message = f"Failed to add tags to workspace '{workspace_id}'. Status code: {response.status_code}, Response: {response.text}"
        raise TerraformAPIError(error_message)

# Example usage:
api_token = ".atlasv1.rd2J0hsLwiSrapazpLmbbpMU2Rb9YscXNNbV1FEsAn5VRQLQJTnCiu0OOtmnf8TE8II"
# workspace_names = ["ws-345679", "ws-dmk5RGphWNffAjaL", "ws-FKrxt2QW5Lok6jKC", "ws-123456"]

# for workspace in workspace_names:
#     try:
#         tags = get_workspace_tags(api_token, workspace)
#         print("Workspace Tags:", tags)
#     except TerraformAPIError as e:
#         print(e)

csv_file_path = "workspaces.csv"

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(csv_file_path, names=["WorkspaceID", "EnvTag", "AccountTag"])

# Iterate through each row in the DataFrame
for index, row in df.iterrows():
    workspace_id = row["WorkspaceID"]
    env_tag = row["EnvTag"]
    account_tag = row["AccountTag"]

    required_tags = ["aexp-app-carid", "aexp-app-env"]
    
    # Check if the workspace has the required tags
    if check_required_tags(api_token, workspace_id, required_tags):
        print(f"Workspace '{workspace_id}' already has the required tags.")
    else:
        # Update the tags for the workspace
        new_tags = [env_tag, account_tag]
        add_tags_to_workspace(api_token, workspace_id, new_tags)

