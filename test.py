import os
import time
from flask import Flask, request, jsonify
import logging
from git import Repo, GitCommandError
from together import Together

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Path to your local testing repository
CODE_REPO_PATH = r"C:\Users\ramna\Documents\autodoc-testing"
client = Together(api_key="69ec5a5bc40d2784ec58256e035b6535581bc97e70ef2796f73c01a64cecc39c")

# Add a global variable to track the last update time
LAST_UPDATE_TIME = 0
UPDATE_COOLDOWN = 60  # Cooldown period in seconds

@app.route('/webhook', methods=['POST'])
def webhook():
    global LAST_UPDATE_TIME
    current_time = time.time()
    
    event = request.headers.get('X-GitHub-Event')
    payload = request.json

    logging.info(f"Received event: {event}")
    logging.debug(f"Payload: {payload}")

    if event in ['push', 'pull_request', 'pull_request_review']:
        # Check if the update is due to our own push
        if current_time - LAST_UPDATE_TIME < UPDATE_COOLDOWN:
            logging.info("Ignoring webhook due to recent update")
            return jsonify({'message': 'Ignored due to recent update'}), 200

        try:
            file_name = get_changed_file_name(payload)
            update_documentation(file_name, payload)
            LAST_UPDATE_TIME = current_time
            return jsonify({'message': 'Documentation updated'}), 200
        except Exception as e:
            logging.error(f"Error updating documentation: {str(e)}", exc_info=True)
            return jsonify({'message': 'Failed to update documentation'}), 500

    return jsonify({'message': 'No action taken'}), 200

def get_changed_file_name(payload):
    if 'pull_request' in payload:
        return payload['pull_request'].get('title', 'Unknown PR')
    elif 'commits' in payload and payload['commits']:
        modified_files = payload['commits'][0].get('modified', [])
        return modified_files[0] if modified_files else 'Unknown file'
    elif 'ref' in payload:
        return payload['ref'].split('/')[-1]  # Branch name
    return 'Unknown change'

def get_file_content(file_path, commit_sha='HEAD'):
    repo = Repo(CODE_REPO_PATH)
    try:
        return repo.git.show(f'{commit_sha}:{file_path}')
    except GitCommandError:
        return ""

def update_documentation(file_name, payload):
    readme_path = os.path.join(CODE_REPO_PATH, 'README.md')
    file_path = os.path.join(CODE_REPO_PATH, file_name)

    # Get current and previous file content
    current_content = get_file_content(file_name)
    previous_content = get_file_content(file_name, payload['before'])

    # Generate diff
    diff = generate_diff(previous_content, current_content)

    # Read the existing README.md file
    try:
        with open(readme_path, 'r', encoding='utf-8') as file:
            existing_content = file.read()
    except FileNotFoundError:
        existing_content = "# Autodoc - Automatically Updating Documentation\n\n"

    # Generate description using Together API
    description = generate_description(file_name, existing_content, payload, current_content, previous_content, diff)

    # Update README content
    updated_content = update_readme_content(existing_content, file_name, description)

    # Check if content has actually changed
    if updated_content == existing_content:
        logging.info("No changes detected in README. Skipping update.")
        return

    # Write the updated content back to README.md
    try:
        with open(readme_path, 'w', encoding='utf-8') as file:
            file.write(updated_content)
    except Exception as e:
        logging.error(f"Error writing to README.md file: {e}")
        raise

    # Commit and push changes
    push_updated_documentation()

def generate_diff(old_content, new_content):
    diff = difflib.unified_diff(old_content.splitlines(), new_content.splitlines(), lineterm='')
    return '\n'.join(diff)

def update_readme_content(existing_content, file_name, new_description):
    header = """# Autodoc - Automatically Updating Documentation

Autodoc works by using GitHub Actions to detect when a pull request is made. It then reviews the file, takes the previous docs, and annexes the new information into the docs using Llama 3, then pushes it to the README file to update the GitHub page automatically.
"""

    new_update = f"""## Latest Update: {file_name}

{new_description}

---

"""

    # Split the existing content
    parts = existing_content.split('## Latest Update:', 1)
    
    if len(parts) > 1:
        previous_updates = parts[1].split('## Previous Updates', 1)
        if len(previous_updates) > 1:
            previous_updates = "## Previous Updates" + previous_updates[1]
        else:
            previous_updates = ""
    else:
        previous_updates = ""

    # Combine all parts
    return f"{header}\n{new_update}{previous_updates}"

def generate_description(file_name, readme_content, payload, current_content, previous_content, diff):
    event_type = payload.get('action', 'push') if 'pull_request' in payload else 'push'
    prompt = f"""Analyze the following information and generate a concise description of the changes:

File Name: {file_name}
Event Type: {event_type}
Payload Excerpt: {str(payload)[:500]}...

Current File Content:
{current_content[:1000]}...

Previous File Content:
{previous_content[:1000]}...

Diff:
{diff[:1000]}...

Current README Content:
{readme_content[:1000]}...

Please provide a structured response in the following format:
1. Brief description of the change (1-2 sentences)
2. Key modifications or additions (bullet points)
3. Impact on existing documentation (if any)
4. Any additional relevant information

Keep the response concise and relevant to the specific change."""

    try:
        response = client.chat.completions.create(
            model="meta-llama/Llama-3-8b-chat-hf",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        logging.info(f"Response received: {response.choices[0].message.content}")
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"Together API call failed: {e}")
        raise

def push_updated_documentation():
    repo = Repo(CODE_REPO_PATH)
    try:
        # Check if there's an ongoing merge
        if repo.git.status('--porcelain'):
            logging.warning("There are uncommitted changes. Attempting to resolve...")
            repo.git.add('.')
            repo.git.commit('-m', 'Resolve merge conflicts')
        
        # Pull changes
        origin = repo.remotes.origin
        origin.pull()
        
        # Add and commit README changes
        repo.git.add('README.md')
        repo.index.commit('Update documentation')
        
        # Push changes
        origin.push()
        logging.info("Successfully pushed the updated documentation")
    except GitCommandError as e:
        logging.error(f"Git operation failed: {e}")
        if "CONFLICT" in str(e):
            logging.error("Merge conflict detected. Please resolve manually.")
        raise

if __name__ == '__main__':
    logging.info("Starting the Flask application")
    app.run(debug=True, port=5000)