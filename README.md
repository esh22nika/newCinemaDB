# Movie Theatre Ticket Booking System

This project is a web-based application for managing a movie theatre's ticket booking process. The system is built using Flask (Python), HTML, CSS, JavaScript, PostgreSQL, and psycopg2. It includes separate dashboards for customers, employees, and admins, each with their own unique features and functionalities.

## Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup and Installation](#setup-and-installation)
- [Database Schema](#database-schema)
- [How to Use](#how-to-use)
- [Future Improvements](#future-improvements)

## Features

### Customer Dashboard
- **Movie Booking**: Customers can browse available movies, select a movie, language, view type, showtime, and book tickets.
- **View Transactions**: Customers can view their transaction history and ticket bookings.

### Employee Dashboard
- **Add Movies**: Employees can add new movie listings with details such as movie name, language, view type, and available showtimes.
- **Sell Tickets**: Employees can manually sell tickets to walk-in customers and confirm the transaction.

### Admin Dashboard
- **Manage Employees**: Admins can create, update, and delete employee records.
- **View Revenue**: Admins can view total revenue from ticket sales, along with transaction and ticket data.
- **Movie Performance**: Admins can view statistics, including total ticket sales and the most popular movies.

### Authentication
- Separate login pages for customers, employees, and admins.
- Simple signup functionality for admins, employees, and customers.

## Technologies Used
- **Frontend**: HTML, CSS, JavaScript (for the interactive seat selection and form handling)
- **Backend**: Flask (Python)
- **Database**: PostgreSQL (pgAdmin used for managing the database)
- **Database Driver**: psycopg2 (for connecting Python to PostgreSQL)

## Setup and Installation

### Prerequisites
Ensure you have the following installed on your system:
- Python 3.x
- PostgreSQL
- Flask and dependencies (`pip install -r requirements.txt`)
- pgAdmin (optional, for database management)

## Database Schema

- **Customers**: Stores customer information such as name, email, and password.
- **Movies**: Stores movie details such as name, language, view type, and showtimes.
- **Bookings**: Stores booking information, including customer, movie, and ticket details.
- **Employees**: Stores employee information.
- **Admins**: Stores admin information.

## How to Use

- **Customer**: Browse and book tickets for movies.
- **Employee**: Add movies to the database and sell tickets.
- **Admin**: Manage employees, view revenue, and check movie performance.

## Future Improvements

- Add real-time seat availability tracking.
- Implement customer reviews and ratings for movies.
- Enhance UI/UX with a more interactive design.

## Legal Notice

This software includes code from [https://codepen.io/Gogh/pen/gOqVqBx] which inspired the login UI, it is licensed under the MIT License (see LICENSE.md for details).

All movie posters used in this project are for educational and personal purposes only. The posters are not owned by the project creator and are sourced from various websites. All copyrights belong to their respective owners.

