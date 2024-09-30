from flask import Flask, session, url_for  # Import necessary modules from Flask
from flask_httpauth import HTTPBasicAuth  # Import HTTPBasicAuth for authentication

app = Flask(__name__)  # Create an instance of the Flask class
auth = HTTPBasicAuth()  # Create an instance of HTTPBasicAuth for handling authentication

# Secret key for session management; used to secure sessions and cookies
app.secret_key = 'your_secret_key_here'

# Dictionary of users and passwords (simulates a user database)
users = {
    "admin": "password123",  # Admin user credentials
    "user1": "mypassword",    # Another user credential
}

# Function to verify the username and password provided by the client
@auth.verify_password
def verify_password(username, password):
    # Check if the username exists and the password matches
    if username in users and users[username] == password:
        session['logged_in'] = True  # Set session as logged in
        session['username'] = username  # Store the username in the session
        return username  # Return the username for successful authentication
    return None  # Return None if authentication fails

# Define a root route for the homepage (no authentication required)
@app.route('/')
def index():
    # Dynamically generate the URL for the /protected route
    protected_url = url_for('protected')
    return f"Welcome to the homepage! Please navigate to <a href='{protected_url}'>protected</a> for authentication."

# Define a protected route that requires authentication
@app.route('/protected')
@auth.login_required  # Ensures this route is accessible only if the user is authenticated
def protected():
    # Generate the URL for the sensitive data route
    sensitive_data_url = url_for('sensitive_data')
    # Return a message indicating successful authentication and a link to sensitive data
    return (f'Hello, {auth.current_user()}! You have access to the protected content. '
            f'To access sensitive data navigate to <a href=\'{sensitive_data_url}\'>sensitive data</a>.')

# Define another protected route for sensitive data
@app.route('/sensitive-data')
@auth.login_required  # This route also requires authentication
def sensitive_data():
    logout_url = url_for('logout')  # Generate the URL for the logout route
    # Return a message showing sensitive data and a link to logout
    return (f'This is sensitive data that requires authentication! '
            f'To logout visit <a href=\'{logout_url}\'>logout</a>.')

# Logout route that clears the session
@app.route('/logout')
def logout():
    home_url = url_for('index')  # Generate the URL for the homepage
    session.clear()  # Clears the session, effectively logging the user out
    # Return a message indicating successful logout and a link to return to the homepage
    return (f'message: You have been logged out. '
            f'navigate to home page <a href=\'{home_url}\'> home page</a>.')

# Running the Flask app
if __name__ == '__main__':
    app.run(debug=True)  # Run the app in debug mode for easier troubleshooting

