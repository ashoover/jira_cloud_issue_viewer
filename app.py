from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

# Jira Cloud Configuration
JIRA_BASE_URL = "https://your-jira-instance.atlassian.net"  # Replace with your Jira instance URL
JIRA_API_TOKEN = "your_api_token"  # Replace with your Jira API token
JIRA_EMAIL = "your_email@example.com"  # Replace with your Jira account email

# HTML Template for the Flask app
HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
    <head>
        <title>Jira Issue Search</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .container { max-width: 600px; margin: auto; }
            .result { margin-top: 20px; }
            pre { background-color: #f8f8f8; padding: 10px; border: 1px solid #ddd; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Search Jira Issue</h1>
            <form method="POST">
                <input type="text" name="issue_key" placeholder="Enter Jira Issue Key (e.g., PROJ-123)" required>
                <button type="submit">Search</button>
            </form>
            {% if issue_data %}
                <div class="result">
                    <h2>Issue Details</h2>
                    <pre>{{ issue_data }}</pre>
                </div>
            {% elif error_message %}
                <div class="result">
                    <h2>Error</h2>
                    <p style="color: red;">{{ error_message }}</p>
                </div>
            {% endif %}
        </div>
    </body>
</html>
"""

# Route for the main page
@app.route("/", methods=["GET", "POST"])
def search_issue():
    issue_data = None
    error_message = None

    if request.method == "POST":
        issue_key = request.form.get("issue_key")
        try:
            # Query Jira API for the issue
            response = requests.get(
                f"{JIRA_BASE_URL}/rest/api/3/issue/{issue_key}",
                auth=(JIRA_EMAIL, JIRA_API_TOKEN),
                headers={"Accept": "application/json"}
            )
            
            if response.status_code == 200:
                issue_data = response.json()
            else:
                error_message = f"Failed to fetch the issue. Status Code: {response.status_code} - {response.text}"

        except Exception as e:
            error_message = f"An error occurred: {str(e)}"

    return render_template_string(HTML_TEMPLATE, issue_data=issue_data, error_message=error_message)

if __name__ == "__main__":
    app.run(debug=True)
