#!/usr/bin/env python3
"""
Test Suite for All Model Types
==============================

Tests each model type individually and then tests the unified framework.
"""

import sys
import traceback
from datetime import datetime, timedelta

def test_agent_based_model():
    """Test the agent-based model"""
    print("\n=== Testing Agent-Based Model ===")
    try:
        sys.path.append('./frameworks')
        from frameworks.hypergnn_core import Agent, AgentType, create_sample_framework
        
        # Test basic agent creation
        agent = Agent("test_001", AgentType.INDIVIDUAL, "Test Person")
        print(f"✓ Created agent: {agent.name} ({agent.agent_type.value})")
        
        # Test framework
        framework = create_sample_framework()
        print(f"✓ Created sample framework for case: {framework.case_id}")
        
        return True
    except Exception as e:
        print(f"✗ Agent-based model test failed: {e}")
        traceback.print_exc()
        return False

def test_discrete_event_model():
    """Test the discrete event model"""
    print("\n=== Testing Discrete Event Model ===")
    try:
        from src.models.discrete_event_model import DiscreteEventModel
        
        # Create model
        model = DiscreteEventModel("test_case_discrete")
        print(f"✓ Created discrete event model for case: {model.case_id}")
        
        # Test model functionality
        if hasattr(model, 'export_model'):
            export = model.export_model()
            print(f"✓ Model export successful")
        
        return True
    except Exception as e:
        print(f"✗ Discrete event model test failed: {e}")
        traceback.print_exc()
        return False

def test_system_dynamics_model():
    """Test the system dynamics model"""
    print("\n=== Testing System Dynamics Model ===")
    try:
        from frameworks.system_dynamics import SystemDynamicsModel, Stock, StockType
        
        # Create model with fixed constructor
        model = SystemDynamicsModel("test_case_dynamics")
        print(f"✓ Created system dynamics model for case: {model.case_id}")
        
        # Test adding a stock
        stock = Stock(
            stock_id="test_stock",
            stock_type=StockType.FINANCIAL,
            owner="test_owner",
            current_level=1000.0,
            unit="USD",
            description="Test Financial Stock",
            last_updated=datetime.now()
        )
        model.add_stock(stock)
        print(f"✓ Added stock: {stock.stock_id}")
        
        return True
    except Exception as e:
        print(f"✗ System dynamics model test failed: {e}")
        traceback.print_exc()
        return False

def test_hypergraph_model():
    """Test the hypergraph model"""
    print("\n=== Testing Hypergraph Model ===")
    try:
        from frameworks.hypergraph_model import (
            HypergraphModel, HypergraphNode, Hyperedge, HyperedgeType
        )
        
        # Create model
        model = HypergraphModel("test_case_hypergraph")
        print(f"✓ Created hypergraph model for case: {model.case_id}")
        
        # Add nodes
        node1 = HypergraphNode("node1", "agent", "Test Agent 1")
        node2 = HypergraphNode("node2", "agent", "Test Agent 2")
        model.add_node(node1)
        model.add_node(node2)
        print(f"✓ Added {len(model.nodes)} nodes")
        
        # Add hyperedge
        hyperedge = Hyperedge(
            "edge1",
            {"node1", "node2"},
            HyperedgeType.COMMUNICATION,
            datetime.now(),
            strength=0.8,
            description="Test communication"
        )
        model.add_hyperedge(hyperedge)
        print(f"✓ Added {len(model.hyperedges)} hyperedges")
        
        # Test analysis
        summary = model.get_summary()
        print(f"✓ Model summary: {summary['total_nodes']} nodes, {summary['total_hyperedges']} hyperedges")
        
        return True
    except Exception as e:
        print(f"✗ Hypergraph model test failed: {e}")
        traceback.print_exc()
        return False

def test_llm_transformer_model():
    """Test the LLM transformer model"""
    print("\n=== Testing LLM Transformer Model ===")
    try:
        sys.path.append('./frameworks')
        from frameworks.llm_transformer_schema import LLMTransformerSchema
        
        # Create model
        model = LLMTransformerSchema("test_case_llm")
        print(f"✓ Created LLM transformer model for case: {model.case_id}")
        print(f"✓ Model config: {model.embed_dim}D embeddings, {model.num_layers} layers")
        
        return True
    except Exception as e:
        print(f"✗ LLM transformer model test failed: {e}")
        traceback.print_exc()
        return False

def test_comprehensive_demo():
    """Test a comprehensive demonstration"""
    print("\n=== Testing Comprehensive Model Integration ===")
    try:
        # Test creating sample data for all models
        
        # 1. Create agents
        from frameworks.hypergnn_core import Agent, AgentType
        agents = [
            Agent("agent_001", AgentType.INDIVIDUAL, "Alice Johnson"),
            Agent("agent_002", AgentType.INDIVIDUAL, "Bob Smith"),
            Agent("agent_003", AgentType.ORGANIZATION, "ABC Corp")
        ]
        print(f"✓ Created {len(agents)} sample agents")
        
        # 2. Create discrete events
        class SimpleEvent:
            def __init__(self, event_id, timestamp, event_type, actors, description):
                self.event_id = event_id
                self.timestamp = timestamp
                self.event_type = event_type
                self.actors = actors
                self.description = description
        
        events = [
            SimpleEvent("event_001", datetime.now() - timedelta(days=10), "communication", 
                       ["agent_001", "agent_002"], "Initial contact"),
            SimpleEvent("event_002", datetime.now() - timedelta(days=5), "meeting", 
                       ["agent_001", "agent_002", "agent_003"], "Strategy meeting")
        ]
        print(f"✓ Created {len(events)} sample events")
        
        # 3. Test individual model integrations
        models_tested = []
        
        # Test System Dynamics
        from frameworks.system_dynamics import SystemDynamicsModel
        sd_model = SystemDynamicsModel("demo_case")
        models_tested.append("SystemDynamics")
        
        # Test Hypergraph
        from frameworks.hypergraph_model import HypergraphModel, HypergraphNode
        hg_model = HypergraphModel("demo_case")
        for agent in agents:
            node = HypergraphNode(agent.agent_id, "agent", agent.name)
            hg_model.add_node(node)
        models_tested.append("Hypergraph")
        
        # Test LLM Transformer
        from frameworks.llm_transformer_schema import LLMTransformerSchema
        llm_model = LLMTransformerSchema("demo_case")
        models_tested.append("LLMTransformer")
        
        print(f"✓ Successfully integrated models: {', '.join(models_tested)}")
        
        # 4. Generate analysis summary
        analysis_summary = {
            "case_id": "demo_case",
            "timestamp": datetime.now().isoformat(),
            "agents_analyzed": len(agents),
            "events_analyzed": len(events),
            "models_used": models_tested,
            "integration_status": "successful"
        }
        
        print(f"✓ Analysis complete - {analysis_summary['agents_analyzed']} agents, "
              f"{analysis_summary['events_analyzed']} events, "
              f"{len(analysis_summary['models_used'])} models")
        
        return True
        
    except Exception as e:
        print(f"✗ Comprehensive demo test failed: {e}")
        traceback.print_exc()
        return False

def run_all_tests():
    """Run all model tests"""
    print("="*60)
    print("COMPREHENSIVE MODEL TESTING SUITE")
    print("="*60)
    
    tests = [
        ("Agent-Based Model", test_agent_based_model),
        ("Discrete Event Model", test_discrete_event_model),
        ("System Dynamics Model", test_system_dynamics_model),
        ("Hypergraph Model", test_hypergraph_model),
        ("LLM Transformer Model", test_llm_transformer_model),
        ("Comprehensive Demo", test_comprehensive_demo)
    ]
    
    results = {}
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20}")
        print(f"Running: {test_name}")
        print(f"{'='*20}")
        
        try:
            result = test_func()
            results[test_name] = result
            if result:
                passed += 1
                print(f"\n✅ {test_name}: PASSED")
            else:
                print(f"\n❌ {test_name}: FAILED")
        except Exception as e:
            results[test_name] = False
            print(f"\n❌ {test_name}: ERROR - {e}")
    
    # Summary
    print(f"\n{'='*60}")
    print(f"TEST RESULTS SUMMARY")
    print(f"{'='*60}")
    print(f"Passed: {passed}/{total}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    print(f"\nDetailed Results:")
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} {test_name}")
    
    if passed == total:
        print(f"\n🎉 All tests passed! Model suite is fully functional.")
    else:
        print(f"\n⚠️ {total-passed} test(s) failed. Check individual test output for details.")
    
    return passed, total

if __name__ == "__main__":
    run_all_tests()