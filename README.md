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

## Legal Notice

This software includes code from [project name/link] licensed under the MIT License (see LICENSE.md for details).

All movie posters used in this project are for educational and personal purposes only. The posters are not owned by the project creator and are sourced from various websites. All copyrights belong to their respective owners.

