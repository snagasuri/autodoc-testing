# import os
# from flask import Flask, request, jsonify
# import logging
# from git import Repo, GitCommandError

# app = Flask(__name__)

# # Configure logging
# logging.basicConfig(level=logging.INFO)

# # Path to your local testing repository
# CODE_REPO_PATH = r"C:\Users\ramna\Documents\autodoc-testing"

# @app.route('/webhook', methods=['POST'])
# def webhook():
#     event = request.headers.get('X-GitHub-Event')
#     payload = request.json

#     logging.info(f"Received event: {event}")

#     if event == 'pull_request_review':
#         action = payload.get('action')
#         logging.info(f"Action: {action}")

#         if action == 'submitted':
#             review = payload.get('review')
#             state = review.get('state')
#             logging.info(f"Review state: {state}")

#             if state == 'approved':
#                 logging.info("Pull request detected and approved")
#                 try:
#                     update_documentation()
#                     return jsonify({'message': 'Pull request detected and approved, documentation updated'}), 200
#                 except Exception as e:
#                     logging.error(f"Error updating documentation: {e}")
#                     return jsonify({'message': 'Failed to update documentation'}), 500

#     return jsonify({'message': 'No action taken'}), 200

# def update_documentation():
#     # Pull the latest code changes
#     pull_latest_code_changes()

#     # Update the README.md file
#     update_readme()

#     # Commit and push the updated README.md file
#     push_updated_documentation()

# def pull_latest_code_changes():
#     try:
#         repo = Repo(CODE_REPO_PATH)
#         origin = repo.remotes.origin
#         origin.pull()
#         logging.info("Successfully pulled the latest changes")
#     except GitCommandError as e:
#         logging.error(f"Git pull failed: {e}")
#         raise

# def update_readme():
#     readme_path = os.path.join(CODE_REPO_PATH, 'README.md')

#     # Read the existing README.md file
#     with open(readme_path, 'r', encoding='utf-8') as file:
#         content = file.read()

#     # Update the content as needed
#     updated_content = content + "\n\n# Documentation Updated\nThe documentation has been updated."

#     # Write the updated content back to README.md
#     with open(readme_path, 'w', encoding='utf-8') as file:
#         file.write(updated_content)

# def push_updated_documentation():
#     try:
#         repo = Repo(CODE_REPO_PATH)
#         repo.git.add('README.md')
#         repo.index.commit('Update documentation after approved pull request')
#         origin = repo.remotes.origin
#         origin.push()
#         logging.info("Successfully pushed the updated documentation")
#     except GitCommandError as e:
#         logging.error(f"Git push failed: {e}")
#         raise

# if __name__ == '__main__':
#     app.run(debug=True, port=5000)

# ^^ working code to push readme update to repo automatically

# import os
# from flask import Flask, request, jsonify
# import logging
# from git import Repo, GitCommandError
# import anthropic
# from together import Together

# app = Flask(__name__)

# # Configure logging
# logging.basicConfig(level=logging.INFO)

# # Path to your local testing repository
# CODE_REPO_PATH = r"C:\Users\ramna\Documents\autodoc-testing"

# @app.route('/webhook', methods=['POST'])
# def webhook():
#     event = request.headers.get('X-GitHub-Event')
#     payload = request.json

#     logging.info(f"Received event: {event}")

#     if event == 'pull_request_review':
#         action = payload.get('action')
#         logging.info(f"Action: {action}")

#         if action == 'submitted':
#             review = payload.get('review')
#             state = review.get('state')
#             logging.info(f"Review state: {state}")

#             if state == 'approved':
#                 logging.info("Pull request detected and approved")
#                 try:
#                     update_documentation(payload)
#                     return jsonify({'message': 'Pull request detected and approved, documentation updated'}), 200
#                 except Exception as e:
#                     logging.error(f"Error updating documentation: {e}")
#                     return jsonify({'message': 'Failed to update documentation'}), 500

#     return jsonify({'message': 'No action taken'}), 200

# def update_documentation(payload):
#     # Get the file name from the pull request payload
#     file_name = "hi_there.txt" #get_changed_file_name(payload)

#     # Pull the latest code changes
#     pull_latest_code_changes()

#     # Update the README.md file
#     update_readme(file_name)

#     # Commit and push the updated README.md file
#     push_updated_documentation()

# # def get_changed_file_name(payload):
# #     # Assuming only one file is changed for simplicity
# #     return payload['pull_request']['head']['repo']['full_name']

# def pull_latest_code_changes():
#     try:
#         repo = Repo(CODE_REPO_PATH)
#         origin = repo.remotes.origin
#         origin.pull()
#         logging.info("Successfully pulled the latest changes")
#     except GitCommandError as e:
#         logging.error(f"Git pull failed: {e}")
#         raise

# def update_readme(file_name):
#     readme_path = os.path.join(CODE_REPO_PATH, 'README.md')

#     # Read the existing README.md file
#     with open(readme_path, 'r', encoding='utf-8') as file:
#         content = file.read()

#     # Generate description using OpenAI API
#     description = generate_description(file_name, content)

#     # Update the content with the generated description
#     updated_content = content + f"\n\n# Documentation Updated for {file_name}\n{description}"

#     # Write the updated content back to README.md
#     with open(readme_path, 'w', encoding='utf-8') as file:
#         file.write(updated_content)

# def generate_description(file_name, readme_content):
#     prompt = f"Analyze the file name and generate a description of the possible contents of the file. Make an educated guess.\n\nFile Name: {file_name}\n\nREADME Content:\n{readme_content}"
#     client = anthropic.Anthropic(
#         # defaults to os.environ.get("ANTHROPIC_API_KEY")
#         api_key="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",
#     ) 
#     try:
#         message = client.messages.create(
#             model="claude-3-opus-20240229",
#             max_tokens=1024,
#             messages=[
#                 {"role": "user", "content": prompt},
#                 {"role": "assistant", "content": "You are a documentation generator."}
#             ]
#     )
#         print(prompt)
#         print(message.content[0].text)
#         return message.content[0].text
#     except Exception as e:
#         logging.error(f"Claude API call failed: {e}")
#         raise
# def push_updated_documentation():
#     try:
#         repo = Repo(CODE_REPO_PATH)
#         repo.git.add('README.md')
#         repo.index.commit('Update documentation after approved pull request')
#         origin = repo.remotes.origin
#         origin.pull()
#         origin.push()
#         logging.info("Successfully pushed the updated documentation")
#     except GitCommandError as e:
#         logging.error(f"Git push failed: {e}")
#         raise

# if __name__ == '__main__':
#     app.run(debug=True, port=5000)

# working code to send filename + readme content to claude

import os
from flask import Flask, request, jsonify
import logging
from git import Repo, GitCommandError
from together import Together

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Path to your local testing repository
CODE_REPO_PATH = r"C:\Users\ramna\Documents\autodoc-testing"
client = Together(api_key="69ec5a5bc40d2784ec58256e035b6535581bc97e70ef2796f73c01a64cecc39c")  # os.environ.get("TOGETHER_API_KEY")

@app.route('/webhook', methods=['POST'])
def webhook():
    event = request.headers.get('X-GitHub-Event')
    payload = request.json

    logging.info(f"Received event: {event}")

    if event == 'pull_request_review':
        action = payload.get('action')
        logging.info(f"Action: {action}")

        if action == 'submitted':
            review = payload.get('review')
            state = review.get('state')
            logging.info(f"Review state: {state}")

            if state == 'approved':
                logging.info("Pull request detected and approved")
                try:
                    update_documentation(payload)
                    return jsonify({'message': 'Pull request detected and approved, documentation updated'}), 200
                except Exception as e:
                    logging.error(f"Error updating documentation: {e}")
                    return jsonify({'message': 'Failed to update documentation'}), 500

    return jsonify({'message': 'No action taken'}), 200

def update_documentation(payload):
    # Get the file name from the pull request payload
    file_name = "hi_there.txt"  # get_changed_file_name(payload)

    # Pull the latest code changes
    pull_latest_code_changes()

    # Update the README.md file
    update_readme(file_name)

    # Commit and push the updated README.md file
    push_updated_documentation()

# def get_changed_file_name(payload):
#     # Assuming only one file is changed for simplicity
#     return payload['pull_request']['head']['repo']['full_name']

def pull_latest_code_changes():
    try:
        repo = Repo(CODE_REPO_PATH)
        origin = repo.remotes.origin
        origin.pull()
        logging.info("Successfully pulled the latest changes")
    except GitCommandError as e:
        logging.error(f"Git pull failed: {e}")
        raise

def update_readme(file_name):
    readme_path = os.path.join(CODE_REPO_PATH, 'README.md')

    # Read the existing README.md file
    try:
        with open(readme_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        logging.error(f"README.md file not found at path: {readme_path}")
        raise
    except Exception as e:
        logging.error(f"Error reading README.md file: {e}")
        raise

    # Generate description using Together API
    description = generate_description(file_name, content)

    # Update the content with the generated description
    updated_content = content + f"\n\n# Documentation Updated for {file_name}\n{description}"

    # Write the updated content back to README.md
    try:
        with open(readme_path, 'w', encoding='utf-8') as file:
            file.write(updated_content)
    except Exception as e:
        logging.error(f"Error writing to README.md file: {e}")
        raise

def generate_description(file_name, readme_content):
    prompt = f"Analyze the file name and generate a description of the possible contents of the file. Make an educated guess.\n\nFile Name: {file_name}\n\nREADME Content:\n{readme_content}"
    try:
        response = client.chat.completions.create(
            model="meta-llama/Llama-3-8b-chat-hf",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        logging.info(f"Prompt sent: {prompt}")
        logging.info(f"Response received: {response.choices[0].message.content}")
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"Together API call failed: {e}")
        raise

def push_updated_documentation():
    try:
        repo = Repo(CODE_REPO_PATH)
        repo.git.add('README.md')
        repo.index.commit('Update documentation after approved pull request')
        origin = repo.remotes.origin
        origin.pull()
        origin.push()
        logging.info("Successfully pushed the updated documentation")
    except GitCommandError as e:
        logging.error(f"Git push failed: {e}")
        raise

if __name__ == '__main__':
    app.run(debug=True, port=5000)

