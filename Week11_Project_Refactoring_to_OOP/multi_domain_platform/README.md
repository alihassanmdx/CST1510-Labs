# Multi-Domain Intelligence Platform

A Streamlit-based web application for managing cybersecurity incidents, IT operations, and data science workflows with AI-powered analysis capabilities.

## Project Overview

This platform integrates multiple operational domains into a unified dashboard, allowing organizations to monitor security threats, manage IT tickets, analyze datasets, and leverage AI assistance for intelligent decision-making.

## Architecture Overview

This project follows  **Object-Oriented Programming (OOP)** architecture 

### Folder Structure
```
multi_domain_platform/
├── models/                      # Domain entity classes
│   ├── user.py                 # User authentication entity
│   ├── security_incident.py    # Cybersecurity incident entity
│   ├── dataset.py              # Data science dataset entity
│   └── it_ticket.py            # IT support ticket entity
├── services/                    # Business logic layer
│   ├── database_manager.py     # Database operations service
│   ├── auth_manager.py         # Authentication service
│   └── ai_assistant.py         # AI integration service
├── database/                    # Database layer
│   ├── schema.py               # Database schema definitions
│   └── intelligence_platform.db # SQLite database file
├── pages/                       # Streamlit UI pages
│   ├── 1_Dashboard.py          # Main dashboard overview
│   ├── 2_Cyber_Incidents.py    # Cybersecurity incident management
│   ├── 3_DataScience.py        # Dataset analysis
│   ├── 4_ITOperations.py       # IT ticket management
│   └── 5_CyberSecurity.py      # Security metrics monitoring
├── .streamlit/                  # Streamlit configuration
│   └── secrets.toml            # API keys and secrets
├── Home.py                      # Application entry point (login/registration)
└── README.md                    # This file
```

### Architecture Layers

#### 1. **Models Layer** (Domain Entities)
Python classes representing main entities with encapsulation:

- User: Represents authenticated users with username, password hash, and role
- SecurityIncident: Tracks cybersecurity incidents with type, severity, status, and description
- Dataset: Manages data science datasets with metadata (size, rows, source)
- ITTicket: Handles IT support tickets with priority, status, and assignment tracking

All models follow OOP principles:
- Private attributes (double underscore prefix)
- Accessor (getter) methods for data access
- __str__ methods for readable output
#### 2. **Services Layer** 
Reusable service classes that handle core application functionality:

- DatabaseManager: Manages SQLite database connections, queries, and schema initialization
- AuthManager: Handles user registration and authentication with bcrypt password hashing
- AIAssistant: Integrates with OpenAI API for AI-powered analysis and insights

#### 3. **Database Layer**
- SQLite database for persistent storage
- Schema definition is in "schema.py"

#### 4. **Presentation Layer** (Streamlit Pages)
User interface pages built with Streamlit:

- **Dashboard**: Aggregated view of all domains (incidents, datasets, tickets)
- **Cyber Incidents**: Full CRUD operations for security incident management with AI analysis
- **Data Science**: Dataset visualization and AI-powered analysis
- **IT Operations**: IT ticket management with status tracking and AI troubleshooting
- **CyberSecurity**: Security metrics dashboard with threat monitoring

## Features

### Core Functionality
- **User Authentication**: Secure login/registration with bcrypt password hashing
-  **Multi-Domain Management**: Unified platform for security, IT, and data science operations
-  **CRUD Operations**: Create, Read, Update, Delete for all entity types
-  **AI Analysis**: OpenAI-powered insights for incidents, tickets, and datasets
-  **Real-time Metrics**: Live dashboards with security metrics and threat monitoring
-  **Data Visualization**: Charts and graphs for trend analysis

### Security Features
- Password hashing with bcrypt
- Session-based authentication
- Role-based access control
- API keys stored securely in secrets

## Prerequisites

- Python 3.10 or higher
- OpenAI API key (for AI features)
- Internet connection (for AI API calls)

The database will be automatically created and initialized when you first run the application.

## Running the Application

### Start the Application

streamlit run Home.py

### First-Time Setup
1. Navigate to the **Register** tab
2. Create a new user account
3. Login with your credentials
4. Explore the different domain pages from the sidebar

##  Guide

### 1. Authentication
- **Register**: Create a new account with username and password
- **Login**: Access the platform with your credentials
- **Logout**: Use the sidebar logout button to end your session

### 2. Dashboard
- View aggregated metrics across all domains
- Quick access to recent incidents, datasets, and tickets
- Summary statistics and counts

### 3. Cyber Incidents Management
- **View All**: Browse all security incidents with filtering
- **Add New**: Create new incident records with type, severity, and description
- **Update Status**: Modify incident status and severity levels
- **Delete**: Remove resolved or invalid incidents
- **AI Analysis**: Get AI-powered root cause analysis and mitigation recommendations

### 4. Data Science
- View dataset metadata and statistics
- Visualize data distributions and correlations
- Get AI-powered data quality assessments and preprocessing suggestions

### 5. IT Operations
- Manage IT support tickets with priority levels
- Track ticket status and assignments
- Get AI-powered troubleshooting guidance

### 6. CyberSecurity Dashboard
- Monitor real-time security metrics
- View threat distribution and trends
- Track security system status
- Analyze incidents by severity

## OOP Design Principles

The project follows key Object-Oriented Programming concepts:

### 1. **Encapsulation**
- All model attributes are private 
- Access controlled through getter methods
- Internal implementation hidden from external code

### 2. **Separation of Concerns**
- Models handle data representation
- Services handle business logic
- Pages handle user interface
- Database layer handles persistence

### 3. **Code Reusability**
- Service classes are reusable across pages
- Model classes can be extended for new features
- Clear interfaces make testing easier

