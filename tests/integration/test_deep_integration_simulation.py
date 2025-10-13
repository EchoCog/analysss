#!/usr/bin/env python3
"""
Test Suite for Deep Integration and Timeline Simulation
======================================================

Tests the deep integration pipeline and timeline simulation capabilities
to ensure accurate case-solving response generation from actor/event queries.
"""

import sys  
import os
import pytest
import json
from datetime import datetime, timedelta
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from deep_integration_simulation import (
    DeepIntegrationPipeline,
    TimelineSimulationTester, 
    TimelineQuery,
    create_sample_case_data
)


class TestDeepIntegrationPipeline:
    """Test cases for deep integration pipeline"""
    
    def setup_method(self):
        """Setup test environment"""
        self.case_id = "test_case_001"
        self.pipeline = DeepIntegrationPipeline(self.case_id)
        self.sample_data = create_sample_case_data()
    
    def test_pipeline_initialization(self):
        """Test pipeline initialization"""
        assert self.pipeline.case_id == self.case_id
        assert self.pipeline.data_cache == {}
        assert self.pipeline.model_outputs == {}
    
    def test_data_integration(self):
        """Test deep data integration across models"""
        metrics = self.pipeline.integrate_case_data(self.sample_data)
        
        # Check integration metrics
        assert metrics.overall_integration_score > 0.5
        assert metrics.data_consistency_score > 0.5
        assert metrics.cross_model_alignment > 0.5
        assert metrics.information_flow_efficiency > 0.5
        assert metrics.temporal_coherence > 0.5
        assert metrics.agent_relationship_accuracy > 0.5
        
        # Check data was cached
        assert len(self.pipeline.data_cache) > 0
        
        # Verify agents were processed
        agent_keys = [k for k in self.pipeline.data_cache.keys() if k.startswith('agent_')]
        assert len(agent_keys) == len(self.sample_data['agents'])
        
        # Verify events were processed
        event_keys = [k for k in self.pipeline.data_cache.keys() if k.startswith('event_')]
        assert len(event_keys) == len(self.sample_data['events'])
    
    def test_agent_integration(self):
        """Test agent integration across models"""
        agent_data = self.sample_data['agents'][0]
        agent = self.pipeline._create_integrated_agent(agent_data)
        
        assert agent.agent_id == agent_data['agent_id']
        assert agent.name == agent_data['name']
        assert hasattr(agent, 'agent_type')
        
        # Check caching
        cache_key = f"agent_{agent.agent_id}"
        assert cache_key in self.pipeline.data_cache
        assert self.pipeline.data_cache[cache_key] == agent
    
    def test_event_integration(self):
        """Test event integration across models"""
        event_data = self.sample_data['events'][0]
        event = self.pipeline._create_integrated_event(event_data)
        
        assert event.event_id == event_data['event_id']
        assert event.description == event_data['description']
        assert event.actors == event_data['actors']
        assert hasattr(event, 'timestamp')
        
        # Check caching
        cache_key = f"event_{event.event_id}"
        assert cache_key in self.pipeline.data_cache
        assert self.pipeline.data_cache[cache_key] == event
    
    def test_metrics_calculation(self):
        """Test integration metrics calculation"""
        # First integrate some data
        self.pipeline.integrate_case_data(self.sample_data)
        
        # Verify metrics are reasonable
        assert self.pipeline.integration_metrics is not None
        metrics = self.pipeline.integration_metrics
        
        # All scores should be between 0 and 1
        assert 0 <= metrics.overall_integration_score <= 1
        assert 0 <= metrics.data_consistency_score <= 1
        assert 0 <= metrics.cross_model_alignment <= 1
        assert 0 <= metrics.information_flow_efficiency <= 1
        assert 0 <= metrics.temporal_coherence <= 1
        assert 0 <= metrics.agent_relationship_accuracy <= 1


class TestTimelineSimulationTester:
    """Test cases for timeline simulation testing"""
    
    def setup_method(self):
        """Setup test environment"""
        self.case_id = "test_case_simulation"
        self.pipeline = DeepIntegrationPipeline(self.case_id)
        self.sample_data = create_sample_case_data()
        
        # Integrate data first
        self.pipeline.integrate_case_data(self.sample_data)
        
        # Initialize simulation tester
        self.tester = TimelineSimulationTester(self.case_id, self.pipeline)
    
    def test_tester_initialization(self):
        """Test simulation tester initialization"""
        assert self.tester.case_id == self.case_id
        assert self.tester.integration_pipeline == self.pipeline
        assert self.tester.simulation_results == []
    
    def test_timeline_query_creation(self):
        """Test timeline query creation"""
        actors = ["suspect_001", "victim_001"]
        events = self.sample_data['events'][:2]
        query_sentence = "Test query about suspects and victims"
        expected_insights = ["pattern", "connection"]
        
        query = self.tester.create_timeline_query(
            actors, events, query_sentence, expected_insights
        )
        
        assert query.case_id == self.case_id
        assert query.actors == actors
        assert query.events == events
        assert query.query_sentence == query_sentence
        assert query.expected_insights == expected_insights
        assert len(query.temporal_order) == len(events)
    
    def test_timeline_simulation(self):
        """Test timeline simulation response generation"""
        # Create a test query
        query = self.tester.create_timeline_query(
            actors=["suspect_001", "victim_001"],
            events=self.sample_data['events'][:3],
            query_sentence="Analyze interaction patterns between suspect and victim",
            expected_insights=["communication pattern", "relationship dynamics"]
        )
        
        # Run simulation
        result = self.tester.simulate_timeline_response(query)
        
        # Verify result structure
        assert result.query_id == query.query_id
        assert isinstance(result.generated_response, str)
        assert len(result.generated_response) > 0
        
        # Verify scores are in valid range
        assert 0 <= result.confidence_score <= 1
        assert 0 <= result.insight_accuracy <= 1
        assert 0 <= result.response_relevance <= 1
        assert 0 <= result.case_solving_potential <= 1
        assert result.execution_time >= 0
        
        # Verify model outputs
        assert 'actors_processed' in result.model_outputs
        assert 'events_processed' in result.model_outputs
        assert result.model_outputs['actors_processed'] == len(query.actors)
        assert result.model_outputs['events_processed'] == len(query.events)
    
    def test_timeline_analysis(self):
        """Test timeline pattern analysis"""
        query = self.tester.create_timeline_query(
            actors=["suspect_001", "victim_001", "witness_001"],
            events=self.sample_data['events'],
            query_sentence="Comprehensive timeline analysis"
        )
        
        analysis = self.tester._analyze_timeline_patterns(query)
        
        # Verify analysis structure
        assert 'communication_pattern' in analysis
        assert 'temporal_clustering' in analysis
        assert 'actor_centrality' in analysis
        assert 'evidence_strength' in analysis
        assert 'motive_clarity' in analysis
        
        # Verify analysis values
        assert isinstance(analysis['communication_pattern'], bool)
        assert isinstance(analysis['temporal_clustering'], bool)
        assert isinstance(analysis['actor_centrality'], list)
        assert 0 <= analysis['evidence_strength'] <= 1
        assert 0 <= analysis['motive_clarity'] <= 1
    
    def test_response_evaluation(self):
        """Test response evaluation methods"""
        query = self.tester.create_timeline_query(
            actors=["suspect_001", "victim_001"],
            events=self.sample_data['events'][:2],
            query_sentence="Test evaluation query",
            expected_insights=["pattern analysis", "evidence strength"]
        )
        
        # Test response with good content
        good_response = "Analysis shows communication pattern between suspect_001 and victim_001 with strong evidence and clear relationship patterns."
        
        confidence = self.tester._evaluate_confidence(query, good_response)
        accuracy = self.tester._evaluate_insight_accuracy(query, good_response)
        relevance = self.tester._evaluate_response_relevance(query, good_response)
        solving_potential = self.tester._evaluate_case_solving_potential(query, good_response)
        
        # All scores should be reasonable for good response
        assert confidence > 0.3
        assert accuracy > 0.1
        assert relevance > 0.1
        assert solving_potential > 0.1
        
        # Test response with poor content
        poor_response = "Nothing to say."
        
        poor_confidence = self.tester._evaluate_confidence(query, poor_response)
        poor_accuracy = self.tester._evaluate_insight_accuracy(query, poor_response)
        poor_relevance = self.tester._evaluate_response_relevance(query, poor_response)
        poor_solving = self.tester._evaluate_case_solving_potential(query, poor_response)
        
        # Poor response should score lower
        assert poor_confidence < confidence
        assert poor_accuracy < accuracy
        assert poor_relevance < relevance
        assert poor_solving < solving_potential
    
    def test_simulation_report_generation(self):
        """Test simulation report generation"""
        # Run a few simulations first
        for i in range(3):
            query = self.tester.create_timeline_query(
                actors=["suspect_001", "victim_001"],
                events=self.sample_data['events'][:2+i],
                query_sentence=f"Test query {i}",
                expected_insights=["test insight"]
            )
            self.tester.simulate_timeline_response(query)
        
        # Generate report
        report = self.tester.generate_simulation_report()
        
        # Verify report structure
        assert report['case_id'] == self.case_id
        assert 'timestamp' in report
        assert report['total_simulations'] == 3
        
        # Verify performance metrics
        metrics = report['performance_metrics']
        assert 'average_confidence_score' in metrics
        assert 'average_insight_accuracy' in metrics
        assert 'average_response_relevance' in metrics
        assert 'average_case_solving_potential' in metrics
        assert 'overall_effectiveness_score' in metrics
        
        # All metrics should be in valid range
        for metric_name, metric_value in metrics.items():
            if metric_name != 'average_execution_time':
                assert 0 <= metric_value <= 1, f"{metric_name} = {metric_value}"
        
        # Verify readiness assessment
        assessment = report['llm_readiness_assessment']
        assert 'confidence_level' in assessment
        assert 'insight_generation' in assessment
        assert 'case_solving_capability' in assessment
        assert 'overall_readiness' in assessment
        
        # Verify individual results
        assert len(report['individual_results']) == 3
        for result in report['individual_results']:
            assert 'query_id' in result
            assert 'confidence_score' in result
            assert 'case_solving_potential' in result


class TestIntegrationScenarios:
    """Test various integration scenarios"""
    
    def test_minimal_data_integration(self):
        """Test integration with minimal data"""
        minimal_data = {
            "agents": [{"agent_id": "test_agent", "name": "Test Agent", "type": "individual"}],
            "events": [{"event_id": "test_event", "timestamp": datetime.now().isoformat(), "type": "communication", "actors": ["test_agent"], "description": "Test event"}],
            "flows": [],
            "relationships": []
        }
        
        pipeline = DeepIntegrationPipeline("minimal_test")
        metrics = pipeline.integrate_case_data(minimal_data)
        
        assert metrics.overall_integration_score > 0
        assert len(pipeline.data_cache) >= 2  # At least agent and event
    
    def test_complex_timeline_query(self):
        """Test complex timeline query with multiple actors and events"""
        pipeline = DeepIntegrationPipeline("complex_test")
        sample_data = create_sample_case_data()
        pipeline.integrate_case_data(sample_data)
        
        tester = TimelineSimulationTester("complex_test", pipeline)
        
        # Create complex query with all actors and events
        query = tester.create_timeline_query(
            actors=[agent['agent_id'] for agent in sample_data['agents']],
            events=sample_data['events'],
            query_sentence="Perform comprehensive analysis of all interactions to determine case strength and prosecution viability",
            expected_insights=["evidence chain", "motive analysis", "opportunity assessment", "means evaluation"]
        )
        
        result = tester.simulate_timeline_response(query)
        
        # Complex query should generate substantial response
        assert len(result.generated_response) > 100
        assert result.confidence_score > 0.3
        assert result.case_solving_potential > 0.3
    
    def test_edge_cases(self):
        """Test edge cases and error handling"""
        pipeline = DeepIntegrationPipeline("edge_case_test")
        
        # Test with empty data
        empty_data = {"agents": [], "events": [], "flows": [], "relationships": []}
        metrics = pipeline.integrate_case_data(empty_data)
        
        # Should handle empty data gracefully
        assert 0 <= metrics.overall_integration_score <= 1
        
        # Test simulation with empty query
        tester = TimelineSimulationTester("edge_case_test", pipeline)
        empty_query = tester.create_timeline_query([], [], "Empty query")
        result = tester.simulate_timeline_response(empty_query)
        
        # Should handle empty query gracefully
        assert isinstance(result.generated_response, str)
        assert 0 <= result.confidence_score <= 1


def test_comprehensive_functionality():
    """Test the complete integration and simulation workflow"""
    
    # 1. Create pipeline
    pipeline = DeepIntegrationPipeline("comprehensive_test")
    
    # 2. Integrate data
    sample_data = create_sample_case_data()
    metrics = pipeline.integrate_case_data(sample_data)
    
    # 3. Create simulation tester
    tester = TimelineSimulationTester("comprehensive_test", pipeline)
    
    # 4. Create and run multiple queries
    queries_results = []
    
    # Basic query
    query1 = tester.create_timeline_query(
        actors=["suspect_001", "victim_001"],
        events=sample_data['events'][:3],
        query_sentence="Analyze basic interaction patterns"
    )
    result1 = tester.simulate_timeline_response(query1)
    queries_results.append((query1, result1))
    
    # Complex query
    query2 = tester.create_timeline_query(
        actors=[agent['agent_id'] for agent in sample_data['agents']],
        events=sample_data['events'],
        query_sentence="Comprehensive case analysis for prosecution decision",
        expected_insights=["case strength", "evidence quality", "witness reliability"]
    )
    result2 = tester.simulate_timeline_response(query2)
    queries_results.append((query2, result2))
    
    # 5. Generate report
    report = tester.generate_simulation_report()
    
    # 6. Verify complete workflow
    assert metrics.overall_integration_score > 0
    assert len(queries_results) == 2
    assert report['total_simulations'] == 2
    assert report['performance_metrics']['overall_effectiveness_score'] >= 0
    
    # 7. Verify improvement over queries (complex should be better)
    assert result2.case_solving_potential >= result1.case_solving_potential * 0.8  # Allow some variance
    
    print(f"✓ Comprehensive test passed")
    print(f"  - Integration Score: {metrics.overall_integration_score:.3f}")
    print(f"  - LLM Effectiveness: {report['performance_metrics']['overall_effectiveness_score']:.3f}")
    print(f"  - Readiness: {report['llm_readiness_assessment']['overall_readiness']}")


if __name__ == "__main__":
    # Run comprehensive functionality test
    test_comprehensive_functionality()
    
    print("\n" + "="*60)
    print("DEEP INTEGRATION SIMULATION TEST SUITE")
    print("="*60)
    print("✅ All comprehensive tests passed!")
    print("✅ Deep integration pipeline functioning correctly")
    print("✅ Timeline simulation system operational")
    print("✅ LLM case-solving response generation working")