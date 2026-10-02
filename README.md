# Secure Auth API (Python / FastAPI)

## Overview
This project is a secure API that handles user authentication (Sign Up, Log In, and Log Out) and protects specific routes. It uses **Supabase Auth** as the Identity Provider (IdP) to manage user accounts and issue secure JSON Web Tokens (JWTs). The API is built using **Python** and **FastAPI**.

## Features
- **Sign Up / Log In**: Users can register and authenticate via Supabase.
- **JWT Authentication**: Secure access using JSON Web Tokens.
- **Public & Protected Routes**: Differentiates between open data and data requiring authentication.
- **Middleware Guard**: Reusable token verification for protected endpoints.
- **Swagger UI**: Interactive API documentation.

## Setup Instructions

### 1. Prerequisites
- Python 3.10+
- A [Supabase](https://supabase.com/) account and project.

### 2. Environment Variables
Create a `.env` file in the root directory and add your Supabase credentials. **Never commit this file to version control.**

```env
SUPABASE_URL=your_project_url
SUPABASE_KEY=your_anon_key
PORT=8000
```

### 3. Installation
Install the required dependencies:
```bash
pip install fastapi uvicorn supabase python-dotenv
```

### 4. Running the Server
Start the development server with:
```bash
uvicorn main:app --reload
```

## API Reference

| Endpoint | Method | Auth Required | Description |
| --- | --- | --- | --- |
| `/auth/signup` | POST | No | Create a new user account. |
| `/auth/login` | POST | No | Authenticate user & return JWT. |
| `/auth/logout` | POST | Yes | Terminate the user session. |
| `/public/info` | GET | No | Read public, unprotected data. |
| `/protected/profile` | GET | Yes | Read private user profile data. |

## AI vs Me (Stage 7)
*(To be completed in Stage 7)*
# Auth---Login-protect
