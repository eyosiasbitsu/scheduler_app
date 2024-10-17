# Scheduler App

Welcome to the **Scheduler App**! This project is built to manage and oversee scheduling tasks easily and effectively. It allows users to create, manage, update, and delete schedules with a secure and intuitive interface.

**Live Demo:** [Scheduler App on Render](https://scheduler-app-lqfa.onrender.com/)

---

## About Scheduler App

The **Scheduler App** is a comprehensive scheduling management system built using Django and Python. It provides users with the ability to authenticate and manage their schedules efficiently. Users can log in, sign up, and handle various operations related to scheduling. The project includes complete API documentation and is fully containerized for development, testing, and production environments.

---

## Built With

The project is built using the following technologies:

- ![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
- ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
- ![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
- ![Swagger](https://img.shields.io/badge/Swagger-85EA2D?style=for-the-badge&logo=swagger&logoColor=white)
- ![Render](https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)

---
## Key Features

- **User Authentication:**
  - User login and signup.
  - Token-based authentication, with token refresh.

- **Schedule Management:**
  - Create, read, update, and delete schedules.
  - Retrieve individual schedules by their ID.
  - Full CRUD support through RESTful API.

- **Swagger Documentation:**
  - Automatically generated API documentation with Swagger, making it easy for developers to understand and use the API.

- **Docker Support:**
  - Comprehensive Docker support with different environments for testing, production, and development.
  - Capability to perform tests locally or from inside Docker containers.

- **CI/CD Integration:**
  - Pre-commit checks for coding standards (via `ruff`).
  - CI/CD pipelines with pre-commit hooks.

- **Test Coverage:**
  - Test coverage included to ensure the project is reliable and bug-free.

- **Deployment:**
  - Deployed on **Render** for live access and scalability.

---

## API Endpoints

Here are the key API endpoints available in the **Scheduler App**:

### Authentication

- **POST** `/auth/login/`: User login.
- **POST** `/auth/signup/`: User signup.
- **POST** `/auth/refresh_token/`: Token refresh.

### Scheduler

- **GET** `/scheduler/schedules/`: Retrieve all schedules.
- **POST** `/scheduler/schedules/`: Create a new schedule.
- **GET** `/scheduler/schedules/{id}/`: Retrieve a specific schedule by ID.
- **PUT** `/scheduler/schedules/{id}/`: Update a specific schedule.
- **PATCH** `/scheduler/schedules/{id}/`: Partially update a schedule.
- **DELETE** `/scheduler/schedules/{id}/`: Delete a schedule.

For a full list of API endpoints, refer to the **Swagger Documentation**.

---

## Screenshots

Here are some screenshots from the **Swagger UI** showcasing the available API endpoints:

![Swagger UI Screenshot](https://user-images.githubusercontent.com/your-image-link)

---

## Setup and Installation

Follow the steps below to set up and run the project locally:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/eyosiasbitsu/scheduler_app.git
   ```

2. **Navigate into the project directory:**

   ```bash
   cd scheduler-app
   ```

3. **Set up a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

4. **Install the required dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

5. **Apply migrations:**

   ```bash
   python manage.py migrate
   ```

6. **Run the development server:**

   ```bash
   python manage.py runserver
   ```

7. **Access the app:**

   Open your browser and visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to access the app locally.

### Docker Setup

To run the project using Docker, follow these steps:

1. **Build and start the Docker containers:**

   ```bash
   docker-compose up --build
   ```

2. **Run the tests from within Docker:**

   ```bash
   docker-compose run web pytest
   ```

---

## Roadmap

- Pre-commit configuration for code quality enforcement (using ruff).
- Swagger API Documentation.
- Docker setup for development, testing, and production.
- CI/CD pipelines with pre-commit hooks.
- Add async logging (via Logfire).
- Docker image building and push to Docker Hub.
- Makefile for migrations and server management.

---

## Contributing

Contributions are welcome and greatly appreciated! To contribute:

1. **Fork the repository.**
2. **Create a new branch:**

   ```bash
   git checkout -b feature/YourFeatureName
   ```

3. **Commit your changes:**

   ```bash
   git commit -m 'Add some feature'
   ```

4. **Push to the branch:**

   ```bash
   git push origin feature/YourFeatureName
   ```

5. **Open a pull request.**

---

## License

Distributed under the MIT License. See `LICENSE` for more information.

---

## Contact

Project Link: [https://github.com/your-username/scheduler-app](https://github.com/your-username/scheduler-app)

---

## Acknowledgments

- Django
- Docker
- Swagger
- Render

---

### Adjustments:
- Replace the placeholder `https://github.com/your-username/scheduler-app` with your actual GitHub project link.
- Replace the placeholder image links and badge URLs with actual links, if necessary.

This README is designed to be easily copied and pasted directly into your project repository! Let me know if you need any further customizations!
