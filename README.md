# Simple IP Address Management (IPAM) Tool

This project is a basic IPAM web tool created using Python and Flask. It allows users to add, view, and delete IP addresses from a simple SQLite database.

## Features

- Add IP addresses to the database.
- View a list of all added IP addresses.
- Delete IP addresses from the database.

## Installation

To set up and run this IPAM tool, follow these steps:

1) **Clone the Repository**

```bash
git clone [repository-url]
cd [repository-name]
```
Create virtual Environment

```
python -m venv venv
```

And activate it with:

On Windows: 

```
venv\Scripts\activate
```

On MacOS/Linux: source 

```
venv/bin/activate
```

2) **Install Dependencies**

Ensure you have Python installed on your system. Then, install the required Python packages using pip:

```bash
pip install Flask Flask-SQLAlchemy
```

3) **Run the Application**
   
Start the Flask application with the following command:

```bash
python app.py
```

## Usage

Once the application is running, navigate to http://localhost:5000 in your web browser. You will see a simple interface to add and view IP addresses. To add an IP address, type it into the input box and click "Add IP". To delete an IP address, click the "Delete" link next to the corresponding IP address.

## Contributing

Contributions to this project are welcome. Please follow these steps to contribute:

Fork the repository.
Create a new branch for your feature (git checkout -b feature/AmazingFeature).
Commit your changes (git commit -m 'Add some AmazingFeature').
Push to the branch (git push origin feature/AmazingFeature).
Open a pull request.
