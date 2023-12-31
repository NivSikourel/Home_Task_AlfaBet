# Event Management RESTful API

Manage and schedule events using a simple RESTful API built with Python's http.server.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Setup Instructions](#setup-instructions)
- [API Endpoints](#api-endpoints)
- [Performance Optimizations](#performance-optimizations)
- [Contributing](#contributing)
- [License](#license)

## Overview

The Event Management RESTful API allows users to schedule, update, and delete events.

## Architecture

The project is built using Python's `http.server` for handling HTTP requests. Event data is stored in a simple relational database. Reminders are implemented to send notifications 30 minutes before an event's scheduled time.

## Setup Instructions

### Prerequisites

- Python 3.x

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/NivSikourel/Home_Task_AlfaBet.git
   cd HomeTaskAlfaBet
   ```

2. Run the following command to start the API server:

   ```bash
   python main.py
   ```

3. The API will be accessible at `http://localhost:8080`.

## API Endpoints

### Schedule a New Event

- **Endpoint:** `/events`
- **Method:** `POST`
- **Request Format:**
  ```json
  {
    "name": "Event Name",
    "location": "Event Location",
    "date": "YYYY-MM-DDTHH:MM:SS",
    "popularity": 100
  }
  ```
- **Response Format:**
  ```json
  {
    "id": 1,
    "name": "Event Name",
    "location": "Event Location",
    "date": "YYYY-MM-DDTHH:MM:SS",
    "popularity": 100,
    "created_at": "YYYY-MM-DD HH:MM:SS"
  }
  ```

### Retrieve All Events

- **Endpoint:** `/events`
- **Method:** `GET`
- **Response Format:**
  ```json
  [
    {
      "id": 1,
      "name": "Event Name",
      "location": "Event Location",
      "date": "YYYY-MM-DDTHH:MM:SS",
      "popularity": 100,
      "created_at": "YYYY-MM-DD HH:MM:SS"
    },
    // ... other events
  ]
  ```

### Retrieve Details of a Specific Event

- **Endpoint:** `/events/{event_id}`
- **Method:** `GET`
- **Response Format:**
  ```json
  {
    "id": 1,
    "name": "Event Name",
    "location": "Event Location",
    "date": "YYYY-MM-DDTHH:MM:SS",
    "popularity": 100,
    "created_at": "YYYY-MM-DD HH:MM:SS"
  }
  ```

### Update Details of a Specific Event

- **Endpoint:** `/events/{event_id}`
- **Method:** `PUT`
- **Request Format:**
  ```json
  {
    "name": "Updated Event Name",
    "location": "Updated Event Location",
    "date": "YYYY-MM-DDTHH:MM:SS",
    "popularity": 120
  }
  ```
- **Response Format:**
  ```json
  {
    "id": 1,
    "name": "Updated Event Name",
    "location": "Updated Event Location",
    "date": "YYYY-MM-DDTHH:MM:SS",
    "popularity": 120,
    "created_at": "YYYY-MM-DD HH:MM:SS"
  }
  ```

### Delete a Specific Event

- **Endpoint:** `/events/{event_id}`
- **Method:** `DELETE`
- **Response Format:**
  ```json
  {
    "message": "Event deleted successfully."
  }
  ```
