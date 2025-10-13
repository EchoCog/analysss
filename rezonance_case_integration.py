#!/usr/bin/env python3
"""
ReZonance Case Integration Module

This module integrates the ReZonance case data with the existing HyperGNN framework
and provides analysis capabilities for the complex financial and legal relationships.
"""

import json
import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from decimal import Decimal


@dataclass
class ReZonanceEntity:
    """Represents an entity in the ReZonance case."""
    name: str
    entity_type: str  # 'Company', 'Person', 'Service Provider'
    description: str
    contact_info: Dict[str, Any]
    financial_data: Dict[str, Any]
    legal_status: str
    created_at: Optional[datetime.datetime] = None


@dataclass
class ReZonanceTimelineEvent:
    """Represents a timeline event in the ReZonance case."""
    event_date: datetime.date
    event_type: str
    description: str
    entity_involved: str
    financial_amount: Optional[Decimal]
    document_reference: str
    significance_level: int  # 1-5, where 5 is most significant


class ReZonanceCaseAnalyzer:
    """Main analyzer for the ReZonance case."""
    
    def __init__(self):
        self.entities = []
        self.timeline_events = []
        self.financial_summary = {}
        
    def load_entities(self) -> List[ReZonanceEntity]:
        """Load key entities from the ReZonance case."""
        entities_data = [
            {
                "name": "ReZonance (Pty) Ltd",
                "entity_type": "Company",
                "description": "Main subject company providing IT services",
                "contact_info": {"email": "dan@regima.com"},
                "financial_data": {"outstanding_debt": 1035361.34, "currency": "ZAR"},
                "legal_status": "Active"
            },
            {
                "name": "RegimA Skin Treatments CC",
                "entity_type": "Company", 
                "description": "Client company with outstanding debt to ReZonance",
                "contact_info": {"address": "50 Van Buuren, Bedfordview"},
                "financial_data": {"debt_to_rezonance": 1035361.34, "currency": "ZAR"},
                "legal_status": "Active"
            },
            {
                "name": "Daniel Faucitt",
                "entity_type": "Person",
                "description": "Director of ReZonance",
                "contact_info": {"email": "dan@regima.com"},
                "financial_data": {"role": "Director"},
                "legal_status": "Active"
            },
            {
                "name": "Kayla Pretorius",
                "entity_type": "Person",
                "description": "Deceased director/shareholder with estate complications",
                "contact_info": {"email": "kayla@regima.zone"},
                "financial_data": {"status": "Estate"},
                "legal_status": "Deceased"
            },
            {
                "name": "Rynette Farrar",
                "entity_type": "Person",
                "description": "Accounts Manager AICB (SA) - unauthorized representation",
                "contact_info": {"email": "rynette@regimaskin.co.za", "phone": "011 615 2869"},
                "financial_data": {"role": "Accounts Manager"},
                "legal_status": "Active"
            },
            {
                "name": "Unicorn Dynamics",
                "entity_type": "Company",
                "description": "Related company requiring annual returns",
                "contact_info": {"registration": "K2016307425"},
                "financial_data": {"status": "Compliance Risk"},
                "legal_status": "At Risk"
            }
        ]
        
        self.entities = [ReZonanceEntity(**data) for data in entities_data]
        return self.entities
    
    def load_timeline_events(self) -> List[ReZonanceTimelineEvent]:
        """Load key timeline events from the ReZonance case."""
        events_data = [
            {
                "event_date": datetime.date(2017, 6, 30),
                "event_type": "Service Start",
                "description": "First invoice to RegimA Skin Treatments for Google GSuite services",
                "entity_involved": "RegimA Skin Treatments",
                "financial_amount": Decimal("250.80"),
                "document_reference": "Invoice 1025",
                "significance_level": 3
            },
            {
                "event_date": datetime.date(2017, 9, 30),
                "event_type": "Peak Billing",
                "description": "Major service expansion with multiple enterprise services",
                "entity_involved": "RegimA Skin Treatments",
                "financial_amount": Decimal("100000.00"),
                "document_reference": "Invoices 1005, 1014",
                "significance_level": 5
            },
            {
                "event_date": datetime.date(2022, 3, 1),
                "event_type": "Debt Period Start",
                "description": "Opening balance showing substantial accumulated debt",
                "entity_involved": "RegimA Skin Treatments",
                "financial_amount": Decimal("971587.93"),
                "document_reference": "Financial Records",
                "significance_level": 4
            },
            {
                "event_date": datetime.date(2022, 7, 11),
                "event_type": "Payment Start",
                "description": "First structured payments begin",
                "entity_involved": "RegimA Skin Treatments",
                "financial_amount": Decimal("40000.00"),
                "document_reference": "Bank Records",
                "significance_level": 3
            },
            {
                "event_date": datetime.date(2023, 2, 28),
                "event_type": "Debt Closure",
                "description": "Final balance showing persistent debt despite payments",
                "entity_involved": "RegimA Skin Treatments",
                "financial_amount": Decimal("1035361.34"),
                "document_reference": "RezonanceFebr2023.PDF",
                "significance_level": 5
            },
            {
                "event_date": datetime.date(2025, 7, 2),
                "event_type": "CIPC Warning",
                "description": "Annual return reminder for Unicorn Dynamics",
                "entity_involved": "Unicorn Dynamics",
                "financial_amount": None,
                "document_reference": "CIPC Email",
                "significance_level": 3
            },
            {
                "event_date": datetime.date(2025, 7, 7),
                "event_type": "Dispute Response",
                "description": "Daniel Faucitt clarifies company status and payment disputes",
                "entity_involved": "Daniel Faucitt",
                "financial_amount": None,
                "document_reference": "Email Response",
                "significance_level": 4
            }
        ]
        
        self.timeline_events = [ReZonanceTimelineEvent(**data) for data in events_data]
        return self.timeline_events
    
    def analyze_financial_patterns(self) -> Dict[str, Any]:
        """Analyze financial patterns in the ReZonance case."""
        total_payments = Decimal("470000.00")  # Total payments made 2022-2023
        final_debt = Decimal("1035361.34")
        opening_debt = Decimal("971587.93")
        
        debt_increase = final_debt - opening_debt
        payment_effectiveness = (total_payments / debt_increase) * 100 if debt_increase > 0 else 0
        
        analysis = {
            "total_payments_made": float(total_payments),
            "opening_debt": float(opening_debt),
            "final_debt": float(final_debt),
            "debt_increase": float(debt_increase),
            "payment_effectiveness_percent": float(payment_effectiveness),
            "analysis_summary": {
                "pattern": "Debt increased despite substantial payments",
                "concern": "Additional charges or interest exceeded payment amounts",
                "recommendation": "Investigate payment allocation and additional charges"
            }
        }
        
        self.financial_summary = analysis
        return analysis
    
    def generate_hypergraph_nodes(self) -> List[Dict[str, Any]]:
        """Generate hypergraph nodes for the ReZonance case."""
        nodes = []
        
        # Entity nodes
        for entity in self.entities:
            nodes.append({
                "id": f"entity_{entity.name.replace(' ', '_').lower()}",
                "type": "entity",
                "label": entity.name,
                "entity_type": entity.entity_type,
                "legal_status": entity.legal_status,
                "metadata": {
                    "description": entity.description,
                    "contact_info": entity.contact_info,
                    "financial_data": entity.financial_data
                }
            })
        
        # Event nodes
        for event in self.timeline_events:
            nodes.append({
                "id": f"event_{event.event_date.isoformat()}_{event.event_type.replace(' ', '_').lower()}",
                "type": "event",
                "label": f"{event.event_date}: {event.event_type}",
                "event_type": event.event_type,
                "significance": event.significance_level,
                "metadata": {
                    "description": event.description,
                    "financial_amount": float(event.financial_amount) if event.financial_amount else None,
                    "document_reference": event.document_reference
                }
            })
        
        return nodes
    
    def generate_hypergraph_edges(self) -> List[Dict[str, Any]]:
        """Generate hypergraph edges for the ReZonance case."""
        edges = []
        
        # Financial relationship edges
        edges.append({
            "id": "debt_relationship",
            "type": "financial",
            "source": "entity_regima_skin_treatments_cc",
            "target": "entity_rezonance_(pty)_ltd",
            "relationship": "owes_money",
            "amount": 1035361.34,
            "currency": "ZAR",
            "status": "outstanding"
        })
        
        # Directorship edges
        edges.append({
            "id": "directorship_daniel",
            "type": "governance",
            "source": "entity_daniel_faucitt",
            "target": "entity_rezonance_(pty)_ltd",
            "relationship": "director_of",
            "status": "active"
        })
        
        # Estate complication edges
        edges.append({
            "id": "estate_complication",
            "type": "legal",
            "source": "entity_kayla_pretorius",
            "target": "entity_unicorn_dynamics",
            "relationship": "deceased_director",
            "status": "estate_unresolved"
        })
        
        return edges
    
    def export_to_json(self, filename: str = "rezonance_case_data.json") -> str:
        """Export the complete case data to JSON format."""
        case_data = {
            "case_id": "rezonance_2017_2025",
            "case_name": "ReZonance IT Services Debt Dispute",
            "analysis_date": datetime.datetime.now().isoformat(),
            "entities": [asdict(entity) for entity in self.entities],
            "timeline_events": [
                {
                    **asdict(event),
                    "event_date": event.event_date.isoformat(),
                    "financial_amount": float(event.financial_amount) if event.financial_amount else None
                }
                for event in self.timeline_events
            ],
            "financial_analysis": self.financial_summary,
            "hypergraph_nodes": self.generate_hypergraph_nodes(),
            "hypergraph_edges": self.generate_hypergraph_edges()
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(case_data, f, indent=2, ensure_ascii=False)
        
        return filename


def main():
    """Main function to run the ReZonance case analysis."""
    analyzer = ReZonanceCaseAnalyzer()
    
    print("Loading ReZonance case entities...")
    entities = analyzer.load_entities()
    print(f"Loaded {len(entities)} entities")
    
    print("Loading timeline events...")
    events = analyzer.load_timeline_events()
    print(f"Loaded {len(events)} timeline events")
    
    print("Analyzing financial patterns...")
    financial_analysis = analyzer.analyze_financial_patterns()
    print(f"Payment effectiveness: {financial_analysis['payment_effectiveness_percent']:.2f}%")
    
    print("Exporting case data...")
    filename = analyzer.export_to_json()
    print(f"Case data exported to: {filename}")
    
    return analyzer


if __name__ == "__main__":
    analyzer = main()
