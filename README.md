# AuctionsApp

## Overview

This is a simple auction application built with Django, a Python-based web framework. The app allows users to create auction listings, place bids, comment on listings, and manage a watchlist of items they're interested in.

## Features

- **User Authentication**: Users can register, log in, and log out to manage their account.
- **Auction Listings**: Authenticated users can create, view, and manage auction listings.
- **Bidding System**: Users can place bids on active auction listings.
- **Comments**: Users can leave comments on auction listings to engage in discussions.
- **Watchlist**: Users can add listings to their watchlist for easy tracking.
- **Categories**: Listings can be organized and filtered by categories for better navigation.

## Technologies Used

- **Python** (Programming Language)
- **Django** (Web Framework)
- **SQLite** (Database)
- **HTML5**
- **CSS3**
  
## Getting Started

### Prerequisites

To run this project locally, you need to have Python and Django installed. Ensure you also have an understanding of basic web development concepts and Python programming.

### Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/SokratisChaimanas/AuctionsApp
    cd AuctionsApp
    ```

2. **Create a virtual environment** (recommended):
    ```bash
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

4. **Run migrations**:
    ```bash
    python manage.py migrate
    ```

5. **Create a superuser** (for admin access):
    ```bash
    python manage.py createsuperuser
    ```

6. **Run the development server**:
    ```bash
    python manage.py runserver
    ```

7. **Access the application**:
   - Open your web browser and go to `http://127.0.0.1:8000` to use the app.
   - Access the admin panel at `http://127.0.0.1:8000/admin` to manage the application.

### Usage

- **User Registration and Login**: Register for a new account or log in with existing credentials.
- **Create Listings**: Add new auction listings with details like title, description, starting bid, and category.
- **Place Bids**: View active listings and place bids on items you are interested in.
- **Comment**: Engage in discussions by leaving comments on auction listings.
- **Manage Watchlist**: Add or remove items from your watchlist to keep track of auctions.

## Project Structure

```bash
auctionsapp/
│
├── auctions/            # Core app with models, views, templates, and static files
│
├── commerce/            # Django project configuration files
│   
├── db.sqlite3           # SQLite database file
├── manage.py            # Django management script
