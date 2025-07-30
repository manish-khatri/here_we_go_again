# Quiz Master Application

A full-stack quiz management application with user authentication, role-based access control, and background task processing.

## 🚀 Features

### Admin Features
- **Subject Management**: Create and manage subjects with chapters
- **Quiz Management**: Create quizzes, add questions with multiple choice options
- **Summary Dashboard**: View charts showing subject-wise scores and user attempts
- **User Management**: Overview of all users and their performance
- **Export Functionality**: Export quiz data and results

### User Features
- **Quiz Dashboard**: View available quizzes and start taking them
- **Interactive Quiz Interface**: Take quizzes with timer and immediate feedback
- **Score Tracking**: View personal quiz scores and performance history
- **Summary Charts**: Visual representation of quiz performance

## 🛠️ Tech Stack

### Backend
- **Flask** - Python web framework
- **SQLAlchemy** - Database ORM
- **Flask-Security** - Authentication and authorization
- **Celery** - Background task processing
- **Redis** - Message broker for Celery

### Frontend
- **Vue.js 3** - Progressive JavaScript framework
- **Vue Router** - Official router for Vue.js
- **Pinia** - State management for Vue.js
- **Vite** - Build tool and development server

## 📋 Prerequisites

Before running the application, make sure you have the following installed:

- **Python 3.8+**
- **Node.js 16+**
- **Redis Server**

### Installing Redis

#### Windows:
1. Download Redis from: https://github.com/microsoftarchive/redis/releases
2. Extract and run `redis-server.exe`

#### Linux/macOS:
```bash
# Ubuntu/Debian
sudo apt-get install redis-server

# macOS with Homebrew
brew install redis
```

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/manish-khatri/here_we_go_again.git
cd here_we_go_again
```

### 2. Backend Setup

#### Create and activate virtual environment:
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

#### Install Python dependencies:
```bash
pip install -r req.txt
```

### 3. Frontend Setup

#### Navigate to frontend directory and install dependencies:
```bash
cd frontend
npm install
cd ..
```

### 4. Start Redis Server

#### Windows:
```bash
redis-server.exe
```

#### Linux/macOS:
```bash
redis-server
```

## 🏃‍♂️ Running the Application

### Option 1: Run All Services Manually

#### Terminal 1 - Start Redis (if not running as service):
```bash
redis-server
```

#### Terminal 2 - Start Celery Worker:
```bash
# Windows
venv\Scripts\activate
celery -A backend.celery_app worker --loglevel=info --pool=solo

# Linux/macOS
source venv/bin/activate
celery -A backend.celery_app worker --loglevel=info
```

#### Terminal 3 - Start Celery Beat (for scheduled tasks):
```bash
# Windows
start_celery_beat.bat

# Linux/macOS
./start_celery_beat.sh
```

#### Terminal 4 - Start Flask Backend:
```bash
# Windows
venv\Scripts\activate
python app.py

# Linux/macOS
source venv/bin/activate
python app.py
```

#### Terminal 5 - Start Vue.js Frontend:
```bash
cd frontend
npm run dev
```

### Option 2: Using the Start Script (Coming Soon)
We'll add a startup script to automate this process.

## ✨ New Features Implemented

### 🎯 Backend Jobs & Scheduling
- **Daily Reminders**: Automated daily reminders for inactive users
- **Monthly Reports**: Comprehensive monthly activity reports with HTML formatting
- **CSV Export**: User and admin CSV export functionality with download links
- **Email Integration**: SMTP email support for notifications and reports

### 🚀 Performance & Caching
- **Redis Caching**: Intelligent caching for subjects, dashboard data, and API responses
- **Cache Invalidation**: Automatic cache clearing when data is updated
- **API Performance**: Optimized database queries and response times

### � Enhanced Analytics
- **Real Charts**: Chart.js integration for dynamic data visualization
- **Subject-wise Analytics**: Performance tracking by subject and chapter
- **User Performance Trends**: Time-based performance analysis
- **Export Dashboard**: One-click data export with status tracking

### 🎨 Bootstrap Integration
- **Responsive Design**: Full Bootstrap 5 implementation
- **Form Validation**: HTML5 and JavaScript validation on all forms
- **Modern UI Components**: Bootstrap cards, modals, alerts, and buttons
- **Mobile-First Design**: Optimized for all device sizes

### 🔐 Enhanced Security & Validation
- **Email Validation**: Real-time email format and uniqueness checking
- **Password Strength**: Enforced password complexity requirements
- **Input Sanitization**: Comprehensive input validation on frontend and backend
- **File Access Control**: Secure file download with user access validation

### 📱 User Experience Improvements
- **Loading States**: Visual feedback for all async operations
- **Error Handling**: Comprehensive error messages and user feedback
- **Toast Notifications**: Real-time status updates for background jobs
- **Form Auto-validation**: Real-time validation as users type

## 🔧 Configuration

### Email Configuration
Update the email settings in `backend/tasks.py`:
```python
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'email': 'your-email@gmail.com',
    'password': 'your-app-password',  # Use app-specific password for Gmail
}
```

### Google Chat Webhook (Optional)
To enable Google Chat notifications, update the webhook URL in `backend/tasks.py`:
```python
webhook_url = "YOUR_GOOGLE_CHAT_WEBHOOK_URL"
```

### Backend Configuration
The backend configuration is located in `backend/config.py`. Key settings:

- **Database**: SQLite (development)
- **Redis**: localhost:6379 (DB 0 for Celery, DB 1 for Cache)
- **CORS**: Enabled for frontend at localhost:5173
- **Cache**: 5-minute default timeout for API responses

### Frontend Configuration
The frontend configuration is in `frontend/vite.config.js` and is set up to proxy API requests to the Flask backend.

## 🧪 Testing

### Backend Tests:
```bash
python -m pytest test_users.py
```

### Frontend Tests:
```bash
cd frontend
npm run test
```

## 🚀 Deployment

For production deployment, consider:

1. **Database**: Use PostgreSQL or MySQL instead of SQLite
2. **Redis**: Use Redis Cloud or managed Redis service
3. **Frontend**: Build and serve static files
4. **Backend**: Use Gunicorn or similar WSGI server
5. **Process Management**: Use PM2, systemd, or Docker

## 🛠️ Troubleshooting

### Common Issues:

1. **Redis Connection Error**:
   - Make sure Redis server is running
   - Check Redis connection settings in `backend/config.py`

2. **Database Issues**:
   - Delete `instance/database.sqlite3` and restart the app to recreate

3. **Frontend Not Loading**:
   - Check if backend is running on port 5000
   - Verify CORS settings in `app.py`

4. **Celery Worker Not Starting**:
   - On Windows, use `--pool=solo` flag
   - Make sure Redis is accessible

## 📝 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📞 Support

For issues and questions, please create an issue in the GitHub repository.
