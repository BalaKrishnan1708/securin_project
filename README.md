# 🎓 CPE Search & Explorer - Interview Project

## 🔍 Project Overview
This application is a professional **CPE (Common Platform Enumeration)** dictionary explorer. It provides a full-stack solution to:
1.  **Ingest** large XML feeds from NVD (National Vulnerability Database).
2.  **Store** data in a structured SQL database for efficient querying.
3.  **Expose** the data via a RESTful API with advanced filtering.
4.  **Visualize** the data in a high-performance React dashboard.

---

## 🏗️ Architecture Stack
- **Backend**: Python 3.10+ & FastAPI
- **Database**: SQLite (SQLAlchemy ORM)
- **Frontend**: React 18+ & Vite
- **Styling**: Modern CSS (Glassmorphism & Radial Gradients)
- **Icons**: Lucide React

---

## 🛠️ How to Run in VS Code

### Step 1: Open VS Code
Open the root directory `securin` in VS Code.

### Step 2: Setup Backend (In one VS Code Terminal)
1.  Open a new terminal (**Ctrl+Shift+`**).
2.  Navigate to backend: `cd backend`
3.  Run the setup script (I have already created `venv` for you):
    ```powershell
    .\venv\Scripts\activate
    pip install -r requirements.txt
    ```
4.  **Populate Database** (Required once):
    ```powershell
    python parser.py
    ```
5.  **Start API**:
    ```powershell
    python main.py
    ```
    *Wait for "Uvicorn running on http://0.0.0.0:8000"*

### Step 3: Setup Frontend (In a SECOND VS Code Terminal)
1.  Open a new terminal (**Click the + in the terminal bar**).
2.  Navigate to frontend: `cd frontend`
3.  Install dependencies:
    ```bash
    npm install
    ```
4.  Launch Dashboard:
    ```bash
    npm run dev
    ```
5.  Open [http://localhost:5173](http://localhost:5173) in your browser.

---

## 💡 Key Design Decisions (For the Examiner)

### 1. **Optimized XML Parsing**
The source XML is over 600MB. Loading this into memory would crash most systems.
*   **Solution**: We used `ET.iterparse()`, which processes the file in **chunks**. This keeps memory usage flat (constant O(1)) regardless of file size.
*   **Database Performance**: We used `db.bulk_save_objects()` to commit records in batches of 1,000, reducing database I/O overhead.

### 2. **Professional REST API**
*   **Endpoints**: Separate endpoints for simple retrieval (`/api/cpes`) and complex searching (`/api/cpes/search`).
*   **Search Engine**: Implemented `ilike` (case-insensitive search) for flexible filtering by product title and URI.
*   **CORS**: Configured FastAPI middleware to securely allow the React frontend to communicate with the API.

### 3. **Enterprise UI Experience**
*   **Layout**: A "Glassmorphism" search bar that stays legible while being visually appealing.
*   **UX Features**:
    *   **Debounced Search**: Added a 400ms delay to inputs to prevent hitting the API on every single keystroke.
    *   **Popovers**: Solved the "too many links" problem by showing the top 2 links and hiding the rest behind an interactive popover.
    *   **Badges**: URIs are color-coded in badges (Blue for 2.2, Purple for 2.3) for instant visual differentiation.
    *   **Truncation**: Tables stay clean on small screens by truncating long titles with tooltips for the full text.
