# Test Data Automation Tool

Welcome to the **Test Data Automation Tool**!

---

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Setup & Run Steps](#setup--run-steps)
- [Environment Variables](#environment-variables)
- [Troubleshooting](#troubleshooting)
- [Contact](#contact)

---

## Overview

This tool consists of three main components:

- **Backend (Node.js/Express):** Handles API and server logic.
- **Frontend (React):** UI for user interactions.
- **Python Automation (Playwright):** Robust test data handling via browser automation.

---

## Project Structure

```plaintext
/
├── backend/
├── frontend/
├── python_playwright_phase_2/
├── package.json
└── ...
```

---

## Prerequisites

- [Node.js & npm](https://nodejs.org/)
- [Python 3.12+](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/)
- Playwright requirements (handled by pip)
- OS: Windows/macOS/Linux

---

## Setup & Run Steps

> **Follow these steps in your terminal to set up and run the application:**

1. **Setup Node.js dependencies for backend:**

   ```bash
   cd backend && npm install
   ```

2. **Setup Node.js dependencies for frontend:**

   ```bash
   cd ../frontend && npm install
   ```

3. **Install root Node.js dependencies:**

   ```bash
   cd .. && npm install
   ```

4. **Setup Python virtual environment for automation:**

   ```bash
   python -m venv venv
   ```
4a. activate the venv script 

5. **Install Python package dependencies:**

   ```bash
   pip install -r ./python_playwright_phase_2/requirements.txt
   ```

6. **Fill in Environment Variables:**

   - Fill the `.env` files in the main **backend** and **python_playwright_phase_2** folder as needed.

7. **Run the Application:**
   ```bash
   npm run dev
   ```
   This starts both backend, frontend and trigger Python service.

---

## Environment Variables

- Copy `.env.example`.
- Fill in necessary API keys, DB credentials, etc. in:
  - `/backend/.env`
  - `/python_playwright_phase_2/.env`

---

## Troubleshooting

- **Missing dependencies?**  
  Double-check `npm install` and `pip install -r requirements.txt`.

- **Env not loading?**  
  Ensure your `.env` files are present and correctly filled.

---
