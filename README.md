# Dorcasity

A basic blog application built with Flask and Bootstrap.

## Installation

1. Install pipenv - `pip install pipenv`

2. Initial pipenv - `pipenv shell`

3. Install dependencies - `pipenv install` | `pipenv install -r requirements.txt`

## Running the server locally

1. Start up the server - Run `python app.py` in the terminal

2. Server should be running on http://localhost:5000/ by default

## Routes

| Routes                               | Description                    | Auth required |
| ------------------------------------ | ------------------------------ | ------------- |
| [GET] &nbsp; /login/                 | Returns a login page           | none          |
| [POST] &nbsp; /login/                | Logs in a user                 | none          |
| [GET] &nbsp; /logout/                | Logs out a user                | true          |
| [GET] &nbsp; /register/              | Returns a registration page    | none          |
| [POST] &nbsp; /register/             | Registers a user               | none          |
| [GET] &nbsp; /                       | Returns the home page          | none          |
| [GET] &nbsp; /articles/              | Returns a list of all articles | none          |
| [GET] &nbsp; /article/<id>           | Returns a single article       | none          |
| [GET] &nbsp; /create/                | Returns a create article page  | true          |
| [POST] &nbsp; /articles/             | Creates an article             | true          |
| [GET] &nbsp; /article/<id>/edit      | Returns an edit article page   | true          |
| [POST] &nbsp; /article/<id>/edit     | Edits an article               | true          |
| [DELETE] &nbsp; /article/<id>/delete | Deletes an article             | true          |
