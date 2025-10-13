"""
HyperGNN Analysis Framework - Backend API Server
Provides REST API endpoints for the frontend interface
"""

import logging
import os
import sqlite3
import sys
import uuid
from datetime import datetime, timedelta

from flask import Flask, jsonify, request
from flask_cors import CORS

# Add the current directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Try to import the HyperGNN framework
try:
    from frameworks.hypergnn_core import HyperGNNFramework

    HYPERGNN_AVAILABLE = True
except ImportError:
    HYPERGNN_AVAILABLE = False
    print("Warning: HyperGNN framework not available. Using mock data.")

# Try to import HyperGraphQL API
try:
    from src.api.hypergraphql_api import hypergraphql_bp
    HYPERGRAPHQL_AVAILABLE = True
except ImportError:
    HYPERGRAPHQL_AVAILABLE = False
    print("Warning: HyperGraphQL API not available.")

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Register HyperGraphQL blueprint if available
if HYPERGRAPHQL_AVAILABLE:
    app.register_blueprint(hypergraphql_bp)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database setup
DB_PATH = "analysis_framework.db"


def init_database():
    """Initialize the SQLite database with required tables"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Cases table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS cases (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'active',
            priority TEXT DEFAULT 'medium',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            entity_count INTEGER DEFAULT 0,
            evidence_count INTEGER DEFAULT 0,
            event_count INTEGER DEFAULT 0
        )
    """
    )

    # Entities table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS entities (
            id TEXT PRIMARY KEY,
            case_id TEXT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            properties TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (case_id) REFERENCES cases (id)
        )
    """
    )

    # Evidence table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS evidence (
            id TEXT PRIMARY KEY,
            case_id TEXT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            file_path TEXT,
            status TEXT DEFAULT 'pending',
            metadata TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (case_id) REFERENCES cases (id)
        )
    """
    )

    # Analysis results table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS analysis_results (
            id TEXT PRIMARY KEY,
            case_id TEXT,
            analysis_type TEXT NOT NULL,
            results TEXT,
            status TEXT DEFAULT 'running',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,
            FOREIGN KEY (case_id) REFERENCES cases (id)
        )
    """
    )

    conn.commit()
    conn.close()


def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# Mock data for demonstration
MOCK_DASHBOARD_STATS = {
    "active_cases": 24,
    "entities_analyzed": 1847,
    "evidence_items": 3291,
    "processing_time": "2.3s",
    "trends": {
        "cases": "+12%",
        "entities": "+8%",
        "evidence": "+15%",
        "processing": "-23%",
    },
}

MOCK_SYSTEM_STATUS = {
    "hypergnn_core": {"status": "online", "uptime": "99.8%"},
    "database": {"status": "connected", "connections": 12},
    "processing_queue": {"status": "healthy", "pending": 3},
    "api_gateway": {"status": "healthy", "response_time": "45ms"},
}

MOCK_CASES = [
    {
        "id": "case_2025_137857",
        "title": "Financial Fraud Investigation",
        "description": "Complex financial fraud case involving multiple entities",
        "status": "in_progress",
        "priority": "high",
        "created_at": "2025-01-15T10:30:00Z",
        "entity_count": 47,
        "evidence_count": 89,
        "event_count": 156,
    },
    {
        "id": "case_2025_138901",
        "title": "Corporate Compliance Review",
        "description": "Compliance audit and review process",
        "status": "completed",
        "priority": "medium",
        "created_at": "2025-01-10T14:20:00Z",
        "entity_count": 23,
        "evidence_count": 45,
        "event_count": 78,
    },
    {
        "id": "case_2025_139245",
        "title": "Evidence Chain Analysis",
        "description": "Analysis of evidence chain and relationships",
        "status": "pending",
        "priority": "high",
        "created_at": "2025-01-20T09:15:00Z",
        "entity_count": 89,
        "evidence_count": 156,
        "event_count": 234,
    },
]

# API Routes


@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify(
        {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "hypergnn_available": HYPERGNN_AVAILABLE,
        }
    )


@app.route("/api/dashboard/stats", methods=["GET"])
def get_dashboard_stats():
    """Get dashboard statistics"""
    try:
        # In a real implementation, this would query the database
        return jsonify(MOCK_DASHBOARD_STATS)
    except Exception as e:
        logger.error(f"Error getting dashboard stats: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/system/status", methods=["GET"])
def get_system_status():
    """Get system status information"""
    try:
        return jsonify(MOCK_SYSTEM_STATUS)
    except Exception as e:
        logger.error(f"Error getting system status: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/cases", methods=["GET"])
def get_cases():
    """Get all cases"""
    try:
        conn = get_db_connection()
        cases = conn.execute("SELECT * FROM cases ORDER BY created_at DESC").fetchall()
        conn.close()

        if not cases:
            # Return mock data if database is empty
            return jsonify(MOCK_CASES)

        return jsonify([dict(case) for case in cases])
    except Exception as e:
        logger.error(f"Error getting cases: {e}")
        return jsonify(MOCK_CASES)


@app.route("/api/cases/<case_id>", methods=["GET"])
def get_case(case_id):
    """Get specific case details"""
    try:
        conn = get_db_connection()
        case = conn.execute("SELECT * FROM cases WHERE id = ?", (case_id,)).fetchone()
        conn.close()

        if case:
            return jsonify(dict(case))
        else:
            # Return mock data for known case IDs
            mock_case = next((c for c in MOCK_CASES if c["id"] == case_id), None)
            if mock_case:
                return jsonify(mock_case)
            return jsonify({"error": "Case not found"}), 404
    except Exception as e:
        logger.error(f"Error getting case {case_id}: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/cases", methods=["POST"])
def create_case():
    """Create a new case"""
    try:
        data = request.get_json()
        case_id = str(uuid.uuid4())

        conn = get_db_connection()
        conn.execute(
            """
            INSERT INTO cases (id, title, description, status, priority)
            VALUES (?, ?, ?, ?, ?)
        """,
            (
                case_id,
                data.get("title"),
                data.get("description"),
                data.get("status", "active"),
                data.get("priority", "medium"),
            ),
        )
        conn.commit()
        conn.close()

        return jsonify({"id": case_id, "message": "Case created successfully"}), 201
    except Exception as e:
        logger.error(f"Error creating case: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/cases/<case_id>/entities", methods=["GET"])
def get_entities(case_id):
    """Get entities for a specific case"""
    try:
        conn = get_db_connection()
        entities = conn.execute(
            "SELECT * FROM entities WHERE case_id = ?", (case_id,)
        ).fetchall()
        conn.close()

        return jsonify([dict(entity) for entity in entities])
    except Exception as e:
        logger.error(f"Error getting entities for case {case_id}: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/cases/<case_id>/network", methods=["GET"])
def get_network_data(case_id):
    """Get network visualization data for a case"""
    try:
        # Generate mock network data
        import random

        nodes = []
        links = []

        # Generate sample nodes
        entity_types = ["Person", "Organization", "Location", "Event", "Evidence"]
        colors = ["#3b82f6", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6"]

        num_nodes = random.randint(20, 50)
        for i in range(num_nodes):
            entity_type = random.choice(entity_types)
            nodes.append(
                {
                    "id": f"entity_{i}",
                    "name": f"{entity_type} {i + 1}",
                    "type": entity_type,
                    "color": colors[entity_types.index(entity_type)],
                    "size": random.randint(5, 20),
                    "connections": random.randint(1, 8),
                }
            )

        # Generate sample links
        for i in range(num_nodes * 2):
            source = random.randint(0, num_nodes - 1)
            target = random.randint(0, num_nodes - 1)
            if source != target:
                links.append(
                    {
                        "source": f"entity_{source}",
                        "target": f"entity_{target}",
                        "strength": random.random(),
                        "type": "relationship",
                    }
                )

        return jsonify({"nodes": nodes, "links": links})
    except Exception as e:
        logger.error(f"Error getting network data for case {case_id}: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/cases/<case_id>/timeline", methods=["GET"])
def get_case_timeline(case_id):
    """Get timeline data for a case"""
    try:
        # Generate mock timeline data
        timeline = []
        start_date = datetime.now() - timedelta(days=30)

        for i in range(6):
            date = start_date + timedelta(days=i * 5)
            timeline.append(
                {
                    "date": date.strftime("%Y-%m-%d"),
                    "events": 12 + i * 11,
                    "entities": 8 + i * 7,
                }
            )

        return jsonify(timeline)
    except Exception as e:
        logger.error(f"Error getting timeline for case {case_id}: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/cases/<case_id>/entity-distribution", methods=["GET"])
def get_entity_distribution(case_id):
    """Get entity distribution data for a case"""
    try:
        distribution = [
            {"name": "Persons", "value": 18, "color": "#3b82f6"},
            {"name": "Organizations", "value": 12, "color": "#10b981"},
            {"name": "Accounts", "value": 8, "color": "#f59e0b"},
            {"name": "Locations", "value": 6, "color": "#ef4444"},
            {"name": "Documents", "value": 3, "color": "#8b5cf6"},
        ]
        return jsonify(distribution)
    except Exception as e:
        logger.error(f"Error getting entity distribution for case {case_id}: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/cases/<case_id>/analyze", methods=["POST"])
def run_analysis(case_id):
    """Run HyperGNN analysis on a case"""
    try:
        data = request.get_json()
        analysis_id = str(uuid.uuid4())

        if HYPERGNN_AVAILABLE:
            # Run actual analysis
            # framework = HyperGNNFramework()
            # Implementation would go here
            pass

        # Store analysis request
        conn = get_db_connection()
        conn.execute(
            """
            INSERT INTO analysis_results (id, case_id, analysis_type, status)
            VALUES (?, ?, ?, ?)
        """,
            (analysis_id, case_id, data.get("type", "hypergnn"), "running"),
        )
        conn.commit()
        conn.close()

        return jsonify(
            {
                "analysis_id": analysis_id,
                "status": "started",
                "message": "Analysis started successfully",
            }
        )
    except Exception as e:
        logger.error(f"Error running analysis for case {case_id}: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/cases/<case_id>/reports/<report_type>", methods=["GET"])
def generate_report(case_id, report_type):
    """Generate a report for a case"""
    try:
        report_data = {
            "case_id": case_id,
            "report_type": report_type,
            "generated_at": datetime.now().isoformat(),
            "summary": f"Generated {report_type} report for case {case_id}",
            "data": {
                "entities": 47,
                "evidence": 89,
                "connections": 156,
                "key_findings": [
                    "Transaction pattern anomaly detected",
                    "Document inconsistency found",
                    "Network connection discovered",
                ],
            },
        }
        return jsonify(report_data)
    except Exception as e:
        logger.error(
            f"Error generating report {report_type} for case {case_id}: {e}"
        )
        return jsonify({"error": str(e)}), 500


@app.route("/api/search/entities", methods=["GET"])
def search_entities():
    """Search entities across all cases"""
    try:
        # query = request.args.get("query", "")
        # Mock search results
        results = [
            {
                "id": "entity_1",
                "name": "John Smith",
                "type": "Person",
                "case_id": "case_2025_137857",
            },
            {
                "id": "entity_2",
                "name": "ABC Corporation",
                "type": "Organization",
                "case_id": "case_2025_137857",
            },
        ]
        return jsonify(results)
    except Exception as e:
        logger.error(f"Error searching entities: {e}")
        return jsonify({"error": str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    # Initialize database
    init_database()

    # Insert some mock data if database is empty
    conn = get_db_connection()
    existing_cases = conn.execute("SELECT COUNT(*) FROM cases").fetchone()[0]
    if existing_cases == 0:
        for case in MOCK_CASES:
            conn.execute(
                """INSERT INTO cases (id, title, description, status, priority, created_at, entity_count, evidence_count, event_count) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    case["id"],
                    case["title"],
                    case["description"],
                    case["status"],
                    case["priority"],
                    case["created_at"],
                    case["entity_count"],
                    case["evidence_count"],
                    case["event_count"],
                ),
            )
    conn.commit()
    conn.close()

    app.run(debug=True, port=5001)

