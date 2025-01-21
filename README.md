# Messaging App Backend

This project provides a backend service for managing messages, including sending, fetching, and deleting messages. It is built with [FastAPI](https://fastapi.tiangolo.com/).

## Requirements

- **Python:** Version 3.6 or higher. 
- **Virtual Environment:** It is recommended to use `venv` for dependency management.  
  See [Steps to Run the Project Locally](#steps-to-run-the-project-locally) for setup instructions.
- **Database:** A SQL database (MySQL) hosted on [Railway](https://railway.app/). (No setup required)


## API Routes

Can be tested using curl or postman but it is recommended to test the API endpoints using Swagger by navigating to `/docs` after running the app locally. 

By default, the application runs at **[http://127.0.0.1:8000](http://127.0.0.1:8000)**.

### Available Endpoints:

There is one endpoint corresponding to each functional requirement specified in the test assignment. 

1. **POST /messages/** – Submit a new message. Message is passed in the request body.
   
   **Sample Request Body:** ```
{
  "recipient": "test@gmail.com",
  "content": "Hello, this is a test message"
}```
2. **GET /messages/unread** – Fetch unread messages for a specific recipient if recipient is provided as a query parameter otherwise returns unread messages for all recipients. (marks fetched messages as read)
3. **DELETE /messages/{message_id}** – Remove a specific message by its ID. `ID` (*int*) is passed as path parameter.
4. **DELETE /messages/batch** – Remove multiple messages by providing message IDs and/or recipients. Request body consists of json in the following format where you can add ids or recipients. (supports partial deletion)

   **Sample Request Body:** ```
{
  "message_ids": [
    1, 2, 3
  ],
  "recipients": [
    "test@gmail.com", "anothertest@gmail.com"
  ]
}```
5. **GET /messages/** – Fetch all messages with optional pagination. `recipient` (*string*), `start` (*int*), `stop` (*int*) are provided as query parameters. (marks fetched messages as read)

## Steps to Run the Project Locally

For convenience, the `.env` files with the database URL have been committed to the repository. So the only required steps to get started are:

1. **Set up the virtual environment and install dependencies**

   Run the following command to create a virtual environment and install the necessary dependencies:

   ```bash
   make setup-env
   ```
2. **Start the Server Pointing to the Railway SQL Server**

   Once the environment is set up, start the FastAPI server using:

   ```bash
   make run-dev
   ```

3. **Access the API documentation**

   Once the service is running open browser and navigate to the following URL to test the API endpoints using Swagger:
   
   **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**
