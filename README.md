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

## Deployment

### Backend

- Deploy to platforms like Render, Railway, or Heroku.
- Set `OPENAI_API_KEY` as an environment variable in your hosting dashboard.
- Ensure the build command installs dependencies from `requirements.txt`.
- Start command: `uvicorn api:app --host 0.0.0.0 --port $PORT`.

### Frontend

- Deploy to Vercel, Netlify, or Render Static Sites.
- Update the API URL in `App.jsx` to point to your deployed backend URL instead of `localhost`.

## Project Structure

- `api.py`: FastAPI application entry point.
- `main.py`: CLI version of the agent (optional).
- `nodes.py`: LangGraph nodes for intent extraction, tool invocation, and synthesis.
- `tool.py`: Interface for REST Countries API.
- `state.py`: State definition for LangGraph.
- `models.py`: Pydantic models for intent and data validation.
- `frontend/`: React application source code.
