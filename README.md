# 🛡️ Guardian MPIN Shield

Guardian MPIN Shield is a Streamlit web application designed to help users evaluate the strength of their Mobile Personal Identification Numbers (MPINs). It analyzes MPINs against common patterns, sequential numbers, repeating digits, keyboard patterns, and personal demographic dates to identify vulnerabilities and provide security recommendations.

## ✨ Features

* **MPIN Strength Evaluation:** Assesses MPINs as STRONG, MODERATE, or WEAK.
* **Vulnerability Detection:** Identifies MPINs that are common, repetitive, sequential, or based on personal dates (Date of Birth, Anniversary).
* **User-Friendly Interface:** Built with Streamlit for an intuitive and interactive experience.
* **Privacy-Focused:** All data is processed locally and **not stored**, ensuring user privacy.
* **Visual Feedback:** Uses Lottie animations and custom CSS for engaging user feedback.

---

## 🏗️ Architecture

The application follows a simple client-server architecture common to Streamlit applications, with a clear separation of concerns for the MPIN evaluation logic.



1.  **Frontend (Streamlit App - `streamlit_app.py`):**
    * Handles the user interface, including input fields for MPIN and personal dates.
    * Manages page navigation (Welcome vs. Main App).
    * Displays real-time feedback using Streamlit widgets, custom CSS (`style.css`), and Lottie animations (loaded from `assets/`).
    * Orchestrates the evaluation process by calling the `MPINEvaluator` class.
    * **No sensitive data is stored or transmitted.**

2.  **Backend (MPIN Evaluation Logic - `mpin_checker.py`):**
    * Contains the core business logic for MPIN strength evaluation within the `MPINEvaluator` class.
    * Performs various checks: common MPINs, sequential patterns, repeating digits, keyboard patterns, and date-related patterns.
    * Assigns a strength level (WEAK, MODERATE, STRONG) and generates specific reasons/suggestions.
    * This module is imported and used directly by `streamlit_app.py`, ensuring all processing happens within the local environment where the Streamlit app is running.

3.  **Static Assets (`assets/` folder):**
    * Stores images (`welcome_image.png`) and Lottie animation JSON files (`animation.json`, `success.json`, `warning.json`, `loading_cube.json`) used by the frontend for visual enhancements.

4.  **Styling (`style.css`):**
    * Provides custom CSS to enhance the visual appeal and branding of the Streamlit application.

---

## ⚙️ Installation

To set up and run the Guardian MPIN Shield application locally, follow these steps:

### 1. **Clone the Repository (or create files manually)**

If this were a Git repository, you would clone it. For now, ensure you have the following file structure in your project directory:
├── streamlit_app.py
├── mpin_checker.py
├── style.css
└── assets/
├── animation.json
├── welcome_image.png
├── success.json
├── warning.json
└── loading_cube.json

**Note:** Ensure `welcome_image.png` exists in the `assets` folder. If you have a different image name (e.g., `welcome_image.png`), update the `st.image` line in `streamlit_app.py` accordingly. Also, place your Lottie JSON files in the `assets` folder.

### 2. **Create a Python Virtual Environment (Recommended)**

It's good practice to use a virtual environment to manage project dependencies.

```bash
python -m venv venv

