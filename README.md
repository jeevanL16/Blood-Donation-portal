# Blood Portal

A Flask-based Blood Donation Portal where users can register as donors or request blood, and an admin can manage the operations.

## Features

- **Donor Registration:** Users can register themselves as blood donors.
- **Blood Request:** Users can request blood for emergencies.
- **Admin Dashboard:** Admin can approve/reject donors, manage requests, and export data.
- **Feedback & Contact:** Users can send feedback and contact the administrators.

## Screenshots

### Home Page

![Home Page](screenshots/home_page.png)

### Testimonials

![Testimonials](screenshots/testimonials.png)

### Admin Dashboard - Donors

![Admin Dashboard Donors](screenshots/admin_dashboard_donors.png)

### Admin Dashboard - Feedback

![Admin Dashboard Feedback](screenshots/admin_dashboard_feedback.png)

## Technologies Used

- Backend: Python, Flask, Flask-SQLAlchemy, Flask-WTF
- Database: MySQL
- Frontend: HTML, CSS (Jinja2 templates)
- Excel Export: Pandas, Openpyxl

## Setup Instructions

1. **Clone the repository**

   ```bash
   git clone <your-repository-url>
   cd bloodportal
   ```

2. **Create a virtual environment and activate it**

   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```

3. **Install the dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Database Configuration**
   - Install MySQL and create a database named `blood_portal`.
   - Ensure you configure your database credentials properly in `config.py` and `app.py`. *(Note: For production, use environment variables instead of hardcoded credentials).*

5. **Run the Application**

   ```bash
   python app.py
   ```

   The application will be accessible at `http://localhost:5000`.

## Admin Access

To log into the admin dashboard, visit `/admin/login` and use the admin credentials defined in the application.

## License

MIT License
