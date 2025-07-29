# Quiz Master Frontend

A modern Vue.js frontend for the Quiz Master application, featuring a comprehensive quiz management system with separate interfaces for administrators and regular users.

## 🚀 Features

### Admin Features
- **Subject Management**: Create and manage subjects with chapters
- **Quiz Management**: Create quizzes, add questions with multiple choice options
- **Summary Dashboard**: View charts showing subject-wise scores and user attempts
- **User Management**: Overview of all users and their performance

### User Features
- **Quiz Dashboard**: View upcoming quizzes and start taking them
- **Quiz Taking Interface**: Interactive quiz interface with timer
- **Score Tracking**: View personal quiz scores and performance
- **Summary Charts**: Visual representation of quiz performance

## 🛠️ Tech Stack

- **Vue.js 3** - Progressive JavaScript framework
- **Vue Router** - Official router for Vue.js
- **Pinia** - State management for Vue.js
- **Vite** - Build tool and development server
- **ESLint** - Code linting
- **Prettier** - Code formatting

## 📦 Installation

1. **Navigate to the frontend directory:**
   ```bash
   cd frontend/quiz-master-frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```

4. **Open your browser and visit:**
   ```
   http://localhost:5173
   ```

## 🏗️ Project Structure

```
src/
├── views/                 # Page components
│   ├── LoginView.vue      # Login/Registration page
│   ├── AdminDashboard.vue # Admin subject management
│   ├── AdminQuiz.vue      # Admin quiz management
│   ├── AdminSummary.vue   # Admin summary charts
│   ├── UserDashboard.vue  # User quiz dashboard
│   ├── UserScores.vue     # User score tracking
│   ├── UserSummary.vue    # User summary charts
│   └── QuizTaking.vue     # Quiz taking interface
├── stores/                # Pinia stores
│   ├── auth.js           # Authentication state
│   └── quiz.js           # Quiz data management
├── router/                # Vue Router configuration
│   └── index.js
├── App.vue               # Root component
└── main.js              # Application entry point
```

## 🗂️ File Organization

### Views
- **LoginView.vue**: Handles user authentication and registration
- **AdminDashboard.vue**: Subject and chapter management interface
- **AdminQuiz.vue**: Quiz and question creation interface
- **AdminSummary.vue**: Analytics and reporting dashboard
- **UserDashboard.vue**: User's quiz overview and navigation
- **UserScores.vue**: Personal score tracking and history
- **UserSummary.vue**: Personal performance analytics
- **QuizTaking.vue**: Interactive quiz interface with timer

### Stores
- **auth.js**: Manages user authentication, login/logout, and user roles
- **quiz.js**: Handles all quiz-related data including subjects, chapters, questions, and scores

## 🚦 Available Scripts

```bash
# Development
npm run dev          # Start development server
npm run build        # Build for production
npm run preview      # Preview production build

# Code Quality
npm run lint         # Run ESLint
npm run format       # Format code with Prettier
```

## 🔐 Authentication

The application uses a mock authentication system for demonstration:

- **Admin Login**: Use any email containing "admin" (e.g., `admin@example.com`)
- **User Login**: Use any other email (e.g., `user@example.com`)
- **Registration**: Creates new user accounts (always as regular users)

## 🎯 Usage Guide

### For Administrators

1. **Login** with an admin email
2. **Navigate** to different sections:
   - **Home**: Manage subjects and chapters
   - **Quiz**: Create and manage quizzes
   - **Summary**: View analytics and reports

3. **Add Subjects**:
   - Click "+ New Subject" button
   - Fill in name and description
   - Save to create the subject

4. **Add Chapters**:
   - Click "+ Chapter" on any subject
   - Fill in chapter details
   - Save to add to the subject

5. **Create Quizzes**:
   - Go to Quiz section
   - Click "+ New Quiz"
   - Set chapter, date, and duration
   - Add questions with multiple choice options

### For Users

1. **Login** with a regular user email
2. **View Upcoming Quizzes** on the dashboard
3. **Start a Quiz**:
   - Click "Start" on any available quiz
   - Answer questions within the time limit
   - Submit when finished

4. **Track Progress**:
   - View scores in the Scores section
   - Check performance analytics in Summary

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory:

```env
VITE_API_BASE_URL=http://localhost:5000/api
VITE_APP_TITLE=Quiz Master
```

### Backend Integration
To connect with the backend:

1. Update API endpoints in the stores
2. Replace mock data with actual API calls
3. Configure CORS settings on the backend

## 📱 Responsive Design

The application is fully responsive and works on:
- Desktop computers
- Tablets
- Mobile phones

## 🎨 Styling

- **CSS Grid** and **Flexbox** for layouts
- **CSS Custom Properties** for theming
- **Responsive design** with mobile-first approach
- **Modern UI** with smooth transitions and hover effects

## 🔄 State Management

The application uses Pinia for state management:

- **Auth Store**: User authentication and session management
- **Quiz Store**: All quiz-related data and operations

## 🚀 Deployment

### Build for Production
```bash
npm run build
```

### Deploy to Static Hosting
The built files in `dist/` can be deployed to:
- Netlify
- Vercel
- GitHub Pages
- Any static file hosting service

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## 📄 License

This project is part of the Quiz Master application.

## 🆘 Support

For support and questions:
1. Check the documentation
2. Review the code comments
3. Open an issue on the repository

---

**Happy Quiz Taking! 🎓**
