# Erasmusbot Application

This project is a Flask web application that incorporates user authentication, chat functionality, and integration with Azure's OpenAI service to provide chatbot responses. The application allows users to register, log in, and interact with a chatbot that answers questions related to Erasmushogeschool Brussel.

## Features

- **User Authentication**: Users can register, log in, and log out.
- **Chat Functionality**: Users can send messages to the chatbot and receive responses related to Erasmushogeschool Brussel.
- **Azure OpenAI Integration**: The chatbot uses Azure's OpenAI service to generate responses.
- **Data Storage**: User credentials and chat messages are stored in an SQLite database.
- **Password Requirements**: Enforces strong password policies.
- **Chat Message Management**: Users can clear their chat history.

## Technologies Used

- **Flask**: Web framework used to build the application.
- **Flask-SQLAlchemy**: ORM for interacting with the SQLite database.
- **Flask-Bcrypt**: Library for hashing passwords.
- **Flask-Login**: User session management.
- **Azure OpenAI**: AI service used for chatbot responses.
- **Dotenv**: For loading environment variables from a `.env` file.

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/jarnedegraeve/ai-essentials.git
    cd yourproject
    ```

2. **Install the dependencies**:
    ```bash
    pip install -r .\requirements.txt
    OR
    pip install --user -r .\requirements.txt
    ```

3. **Create a `.env` file** with the following content:
    ```
    ENDPOINT=your_azure_endpoint
    API_KEY=your_azure_api_key
    SEARCH_ENDPOINT=your_search_endpoint
    SEARCH_KEY=your_search_key
    ```

## Running the Application

1. **Run the Flask development server**:
    ```bash
    python .\app.py
    ```
2. Open your web browser and go to `http://127.0.0.1:5000`.

## Application Structure

- **app.py**: Main application file containing routes, models, and logic.
- **templates/**: HTML templates for rendering web pages.
  - `index.html`: Homepage template.
  - `register.html`: Registration page template.
  - `login.html`: Login page template.
  - `dashboard.html`: User dashboard template.
- **static/**: Folder for static files like CSS and JavaScript.
- **.env**: Environment variables file (not included in the repository for security reasons).

## Security Considerations

- **Password Hashing**: Passwords are hashed using Flask-Bcrypt before storing in the database.
- **Login Required**: Certain routes require users to be logged in to access.

## Acknowledgements

- Flask documentation and tutorials.
- Azure OpenAI for providing the AI service.
