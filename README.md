# Multi-Agent Research Project

This project leverages multiple AI agents (Informational, Interpersonal, Decision Making) to study their impact on human-AI collaboration in a research setting.

## Core Agents

The project implements three distinct AI agent personas to facilitate different aspects of user interaction:

1.  **Informational Agent**: Focuses on providing factual data, statistics, and research-backed information to support user decision-making processes.
2.  **Interpersonal Agent**: Designed with a warm, supportive persona to motivate users, encourage creativity, and provide soft-skills-oriented feedback.
3.  **Decision Making Agent**: Evaluates user ideas based on clarity and feasibility, providing structured feedback and "idea scores" to help refine concepts.

## Project Structure

- `backend/`: FastAPI application handling agent logic and database interactions.
  - `app/agents/`: Specific logic for each agent type.
  - `app/database.py`: SQLAlchemy models and session management.
- `frontend/`: Streamlit application providing a unified user interface for research participants.
- `docker-compose.yml`: Orchestrates the containerized setup.

## Getting Started

1.  **Environment Setup**:
    - Copy `.env.example` to `.env`.
    - Fill in your `GROQ_API_KEY` and `TAVILY_API_KEY`.
2.  **Run with Docker**:
    ```bash
    docker-compose up --build
    ```
3.  **Access the App**:
    - Frontend: `http://localhost:8501`
    - Backend API Docs: `http://localhost:8000/docs`

## Features

- **Unified Interface**: Clean, modern design following research survey flow.
- **Agent Options**: Switch between Informational, Interpersonal, and Decision Making agents.
- **Data Persistence**: Automatically saves participant interactions to a remote RDS PostgreSQL database.
- **Survey Integration**: Generates unique codes for Qualtrics survey verification.

## Clean Code Principles

- **DRY**: Shared logic and schemas across agents.
- **SDLC**: Structured as a modular web application with clear separation of concerns.
- **Minimalist**: Removed unnecessary comments and docstrings.
