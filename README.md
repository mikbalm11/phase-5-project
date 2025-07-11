
# Phase 5 Project

This repository contains a full-stack web application built using **Flask** for the backend and **React** for the frontend. The project is based on the Flatiron School Phase 5 curriculum template, designed to demonstrate the integration of a Python API backend with a modern React frontend.

---

## Table of Contents

- [Project Overview](#project-overview)  
- [Tech Stack](#tech-stack)  
- [Setup and Installation](#setup-and-installation) 
- [Running the Application](#running-the-application)  
- [Project Structure](#project-structure)  

---

## Project Overview

This project implements a web application that leverages a Flask API backend to handle business logic, database models, and routing, while React manages the frontend user interface. The backend and frontend communicate via RESTful API calls.

The application allows users to interact with models such as `User`, `Olives`, and `Producers` and `Olive Oils`. Each user can have many olive oils, each olive oil belongs to an olive and a producer, establishing relationships between models.

---

## Tech Stack

- **Backend:** Python, Flask, SQLAlchemy, SQLite, Marshmallow 
- **Frontend:** React, JavaScript 
- **Package Management:** Pipenv (Python), npm (Node.js) 

---

## Setup and Installation

### 1. Clone the Repository

```bash
git clone git@github.com:mikbalm11/phase-5-project.git
cd phase-p5-project
```

---

### 2. Backend Setup

Navigate to the `server` directory, create a virtual environment, and install dependencies.

```bash
cd server
```

Use the `Pipfile` with Pipenv:

```bash
pip install pipenv
pipenv install ; pipenv shell
```

---

### 3. Frontend Setup

Navigate to the `client` directory and install the npm packages:

```bash
cd ../client
npm install --prefix client
```

---

## Running the Application

### Backend

Run the Flask server:

```bash
cd server
python app.py
```

This will start the backend server on `http://localhost:5555`.

---

### Frontend

In a separate terminal, start the React app:

```bash
cd client
npm start --prefix client
```

This launches the frontend on `http://localhost:4000`.

---


## Project Structure

```
.
├── client/                  # React frontend
│   ├── public/
│   ├── src/
│   ├── package.json
│   └── README.md
├── server/                  # Flask backend
│   ├── app.py               # Flask application entry point
│   ├── models.py            # Database models
│   ├── schema.py           # Schemas
│   ├── Pipfile             # Alternative Python dependency manager
│   └── ...
├── README.md                # This file
└── ...
```