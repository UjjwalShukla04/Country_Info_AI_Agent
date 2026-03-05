# Country Information AI Agent

A full-stack AI agent that provides detailed information about countries using the REST Countries API. It features a React frontend with voice interaction and a FastAPI backend powered by LangGraph.

## Features

- **Country Data:** Fetch population, capital, currency, languages, and flags.
- **Comparison:** Compare multiple countries in a structured table.
- **Ranking:** List top countries by population or area (e.g., "Top 5 most populated countries").
- **Summaries:** Get bullet-point summaries of countries.
- **Voice Interaction:** Speech-to-Text (STT) for input and Text-to-Speech (TTS) for reading answers.
- **Modern UI:** Responsive React frontend with Markdown support.

## Tech Stack

- **Frontend:** React, Vite, Axios, React Markdown
- **Backend:** FastAPI, Python, LangChain, LangGraph, OpenAI GPT-3.5
- **Data Source:** [REST Countries API](https://restcountries.com/)

## Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js & npm
- OpenAI API Key

### Backend Setup

1. Clone the repository.
2. Navigate to the root directory.
3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Create a `.env` file in the root directory and add your OpenAI API key:
   ```
   OPENAI_API_KEY=sk-your-api-key-here
   ```
6. Start the backend server:
   ```bash
   python api.py
   ```
   The backend runs on `http://localhost:8000`.

### Frontend Setup

1. Navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```
   The frontend runs on `http://localhost:5173`.

## Deployment (Manual on Render)

Since Render Blueprints may require payment verification, you can deploy manually for free.

### 1. Deploy Backend (Web Service)

1.  Go to [Render Dashboard](https://dashboard.render.com/).
2.  Click **New +** -> **Web Service**.
3.  Connect this repository.
4.  **Settings**:
    - **Name**: `country-agent-backend`
    - **Runtime**: Python 3
    - **Build Command**: `pip install -r requirements.txt`
    - **Start Command**: `uvicorn api:app --host 0.0.0.0 --port $PORT`
5.  **Environment Variables**:
    - `OPENAI_API_KEY`: Your OpenAI API Key.
6.  Click **Create Web Service**.
7.  **Copy the Backend URL** once deployed (e.g., `https://country-agent-backend.onrender.com`).

### 2. Deploy Frontend (Static Site)

1.  Go to **Render Dashboard**.
2.  Click **New +** -> **Static Site**.
3.  Connect this repository.
4.  **Settings**:
    - **Name**: `country-agent-frontend`
    - **Root Directory**: `frontend` (Important!)
    - **Build Command**: `npm install && npm run build`
    - **Publish Directory**: `dist`
5.  **Environment Variables**:
    - `VITE_API_URL`: Paste your Backend URL here (e.g., `https://country-agent-backend.onrender.com`).
6.  Click **Create Static Site**.

Your app will be live at the frontend URL!

## Project Structure

- `api.py`: FastAPI application entry point.
- `main.py`: CLI version of the agent (optional).
- `nodes.py`: LangGraph nodes for intent extraction, tool invocation, and synthesis.
- `tool.py`: Interface for REST Countries API.
- `state.py`: State definition for LangGraph.
- `models.py`: Pydantic models for intent and data validation.
- `frontend/`: React application source code.
