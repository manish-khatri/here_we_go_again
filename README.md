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

#### Terminal 3 - Start Flask Backend:
```bash
# Windows
venv\Scripts\activate
python app.py

# Linux/macOS
source venv/bin/activate
python app.py
```

#### Terminal 4 - Start Vue.js Frontend:
```bash
cd frontend
npm run dev
```

### Option 2: Using the Start Script (Coming Soon)
We'll add a startup script to automate this process.

## 🌐 Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:5000

## 👤 Default Login Credentials

After the first run, the application creates default users:

### Admin User:
- **Email**: admin@email.com
- **Password**: password

### Regular User:
- **Email**: student@email.com  
- **Password**: password

## 📁 Project Structure

```
here_we_go_again/
├── app.py                 # Flask application entry point
├── req.txt               # Python dependencies
├── backend/              # Backend Flask application
│   ├── config.py        # Application configuration
│   ├── models.py        # Database models
│   ├── routes.py        # API routes
│   ├── celery_app.py    # Celery configuration
│   ├── tasks.py         # Background tasks
│   └── create_init_data.py # Initial data setup
├── frontend/            # Vue.js frontend application
│   ├── package.json     # Node.js dependencies
│   ├── src/
│   │   ├── views/       # Vue components/pages
│   │   ├── stores/      # Pinia stores
│   │   └── router/      # Vue Router configuration
│   └── vite.config.js   # Vite configuration
└── instance/            # Database files (auto-generated)
```

## 🔧 Configuration

### Backend Configuration
The backend configuration is located in `backend/config.py`. Key settings:

- **Database**: SQLite (development)
- **Redis**: localhost:6379
- **CORS**: Enabled for frontend at localhost:5173

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
