# Project Setup and Run Instructions

This project consists of a backend and a frontend. The backend is built with FastAPI and Python, and the frontend is built with React. Follow the instructions below to initialize and run both parts of the project.

## Prerequisites

- Python 3.12
- Node.js and npm

## Makefile Commands

### Backend

1. **Initialize Backend**: This command creates a Python 3.12 virtual environment and installs the necessary Python packages listed in `backend/requirements.txt`.

    ```sh
    make init_backend
    ```

2. **Run Backend**: This command activates the virtual environment and runs the backend server located at `backend/api.py`.

    ```sh
    make run_backend
    ```

### Frontend

1. **Initialize Frontend**: This command installs the necessary npm packages for the frontend located in the `frontend` folder.

    ```sh
    make init_frontend
    ```

2. **Run Frontend**: This command starts the React frontend server.

    ```sh
    make run_frontend
    ```

## Detailed Steps

### Initializing and Running the Backend

1. **Initialize the backend** by creating a virtual environment and installing dependencies:

    ```sh
    make init_backend
    ```

2. **Run the backend server**:

    ```sh
    make run_backend
    ```

### Initializing and Running the Frontend

1. **Initialize the frontend** by installing the required npm packages:

    ```sh
    make init_frontend
    ```

2. **Run the frontend server**:

    ```sh
    make run_frontend
    ```

### Additional Information

- Ensure you have Python 3.12 installed on your system. You can download it from the official [Python website](https://www.python.org/downloads/).
- Ensure you have Node.js and npm installed on your system. You can download them from the official [Node.js website](https://nodejs.org/).
