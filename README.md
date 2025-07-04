# Construction Material Tracker

This project contains a simple Flask web application to track the quote, purchase order and delivery files for construction materials. When creating a new order you can record the order date along with the order name.

## Running the app

1. Install dependencies:
   ```bash
   pip install -r webapp/requirements.txt
   ```
2. Run the application:
   ```bash
   python webapp/app.py
   ```
3. Visit `http://localhost:5000` in your browser.

Files uploaded through the interface are stored in `webapp/uploads/` and order information is saved in `webapp/orders.db`.
