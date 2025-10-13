---

# HyperGNN Analysis Framework - Frontend

This is the frontend interface for the **HyperGNN Analysis Framework**, a modern, interactive web application built with React, D3.js, and other cutting-edge web technologies. It provides a comprehensive suite of tools for case analysis, data visualization, and reporting, all powered by the HyperGNN framework.

## ✨ Features

- **Interactive Dashboard**: A real-time overview of active cases, analyzed entities, evidence items, and system performance.
- **Advanced Case Analysis**: A dedicated dashboard for in-depth case analysis, including timeline analysis, entity distribution, and key findings.
- **Dynamic Network Visualization**: An interactive hypergraph network visualization powered by D3.js, with smooth animations, zoom/pan controls, and node selection.
- **Comprehensive Reporting**: Generate and export detailed reports, including case summaries, network analysis, and statistical breakdowns.
- **Modern UI/UX**: A professional, responsive design with a clean, intuitive user interface, built with shadcn/ui and Tailwind CSS.
- **Backend API Integration**: Seamlessly connects to the Flask-based backend API for data retrieval, analysis, and management.

## 🚀 Getting Started

To get the frontend up and running, follow these simple steps:

### Prerequisites

- Node.js (v18 or higher)
- pnpm (or npm/yarn)

### Installation

1.  **Clone the repository**:

    ```bash
    git clone https://github.com/rzonedevops/analysis.git
    cd analysis/analysis-frontend
    ```

2.  **Install dependencies**:

    ```bash
    pnpm install
    ```

### Running the Development Server

1.  **Start the frontend development server**:

    ```bash
    pnpm run dev
    ```

2.  **Start the backend API server** (in a separate terminal):

    ```bash
    cd ../
    pip install -r requirements.txt
    python3 backend_api.py
    ```

3.  Open your browser and navigate to `http://localhost:5173`.

## 🛠️ Tech Stack

- **Framework**: React
- **Styling**: Tailwind CSS, shadcn/ui
- **Data Visualization**: D3.js, Recharts
- **Animations**: anime.js
- **Build Tool**: Vite
- **Language**: JavaScript (ES6+)

## 📁 Project Structure

```
analysis-frontend/
├── public/             # Static assets
├── src/
│   ├── components/     # Reusable UI components
│   │   ├── ui/         # shadcn/ui components
│   │   ├── CaseAnalysisDashboard.jsx
│   │   └── NetworkVisualization.jsx
│   ├── services/       # API service for backend communication
│   │   └── apiService.js
│   ├── App.jsx         # Main application component
│   ├── App.css         # Global styles
│   └── main.jsx        # Application entry point
├── .env.local          # Environment variables
├── package.json        # Project dependencies and scripts
└── README.md           # This file
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue to discuss any changes.

---

