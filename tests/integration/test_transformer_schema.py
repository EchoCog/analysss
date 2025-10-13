#!/usr/bin/env python3
"""
Test Cases for LLM/Transformer Schema Integration
================================================

Simple test cases to validate the transformer schema functionality
and integration with the HyperGNN framework.
"""

import os
import sys
from datetime import datetime, timedelta

import numpy as np

# Add frameworks to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), "frameworks"))

from hypergnn_core import Agent, AgentType, DiscreteEvent, EventType, HyperGNNFramework
from llm_transformer_schema import EventToken, LLMTransformerSchema, TokenType


def test_token_creation():
    """Test basic token creation and properties"""
    print("Testing token creation...")

    # Create a simple event token
    token = EventToken(
        token_id="test_token",
        token_type=TokenType.ACTION_COMMUNICATION,
        timestamp=datetime.now(),
        embedding=np.random.randn(256),
        semantic_role="Subject",
        agent_perspective="agent_001",
    )

    assert token.token_id == "test_token"
    assert token.token_type == TokenType.ACTION_COMMUNICATION
    assert token.semantic_role == "Subject"
    assert token.agent_perspective == "agent_001"
    assert token.embedding.shape == (256,)

    print("✓ Token creation test passed")


def test_attention_head_creation():
    """Test attention head creation for agent perspectives"""
    print("Testing attention head creation...")

    # Create transformer schema
    schema = LLMTransformerSchema("test_case", embed_dim=128, num_heads=4)

    # Create test agent
    agent = Agent("test_agent", AgentType.INDIVIDUAL, "Test Agent")

    # Create attention head
    head = schema.create_attention_head_for_agent(agent, "victim")

    assert head.agent_id == "test_agent"
    assert head.agent_perspective == "victim"
    assert head.query_weights.shape == (128, 32)  # embed_dim / num_heads
    assert head.key_weights.shape == (128, 32)
    assert head.value_weights.shape == (128, 32)

    # Check focus tokens are set for victim perspective
    assert TokenType.ACTION_TRANSACTION in head.focus_token_types
    assert TokenType.MODIFIER_INTENSITY in head.focus_token_types

    print("✓ Attention head creation test passed")


def test_timeline_tokenization():
    """Test tokenization of timeline events"""
    print("Testing timeline tokenization...")

    # Create test framework
    framework = HyperGNNFramework("test_case")

    # Create test agents
    agent1 = Agent("agent_001", AgentType.INDIVIDUAL, "Alice")
    agent2 = Agent("agent_002", AgentType.INDIVIDUAL, "Bob")
    framework.add_agent(agent1)
    framework.add_agent(agent2)

    # Create test event
    event = DiscreteEvent(
        "test_event",
        datetime.now(),
        EventType.COMMUNICATION,
        ["agent_001", "agent_002"],
        "Test communication event",
    )
    framework.add_event(event)

    # Create transformer schema and tokenize
    schema = LLMTransformerSchema("test_case", embed_dim=64)
    tokens = schema.tokenizer.tokenize_timeline_events([event], framework.agents)

    # Should have [CLS], event, agent1, agent2, [SEP] tokens
    assert len(tokens) == 5
    assert tokens[0].token_type == TokenType.SEQUENCE_START
    assert tokens[-1].token_type == TokenType.SEQUENCE_END
    assert any(token.token_type == TokenType.ACTION_COMMUNICATION for token in tokens)
    assert sum(1 for token in tokens if token.token_type == TokenType.ENTITY_AGENT) == 2

    print("✓ Timeline tokenization test passed")


def test_attention_computation():
    """Test attention computation functionality"""
    print("Testing attention computation...")

    # Create minimal setup
    schema = LLMTransformerSchema("test_case", embed_dim=64, num_heads=2)

    # Create test agent and attention head
    agent = Agent("test_agent", AgentType.INDIVIDUAL, "Test Agent")
    head = schema.create_attention_head_for_agent(agent)

    # Create test tokens
    tokens = [
        EventToken(
            "token1", TokenType.SEQUENCE_START, datetime.now(), np.random.randn(64)
        ),
        EventToken(
            "token2",
            TokenType.ACTION_COMMUNICATION,
            datetime.now(),
            np.random.randn(64),
        ),
        EventToken(
            "token3", TokenType.ENTITY_AGENT, datetime.now(), np.random.randn(64)
        ),
        EventToken(
            "token4", TokenType.SEQUENCE_END, datetime.now(), np.random.randn(64)
        ),
    ]

    schema.tokenized_timeline = tokens

    # Compute self-attention
    attention_matrix = schema._compute_self_attention(head)

    # Check attention matrix properties
    assert attention_matrix.shape == (4, 4)
    assert np.allclose(
        np.sum(attention_matrix, axis=1), 1.0, atol=1e-6
    )  # Rows should sum to 1
    assert np.all(attention_matrix >= 0)  # All attention weights should be non-negative

    print("✓ Attention computation test passed")


def test_cross_attention():
    """Test cross-attention between different agent perspectives"""
    print("Testing cross-attention...")

    schema = LLMTransformerSchema("test_case", embed_dim=64, num_heads=2)

    # Create two agents with different perspectives
    agent1 = Agent("victim", AgentType.INDIVIDUAL, "Victim")
    agent2 = Agent("perpetrator", AgentType.INDIVIDUAL, "Perpetrator")

    head1 = schema.create_attention_head_for_agent(agent1, "victim")
    head2 = schema.create_attention_head_for_agent(agent2, "perpetrator")

    # Create test tokens
    tokens = [
        EventToken(
            "start", TokenType.SEQUENCE_START, datetime.now(), np.random.randn(64)
        ),
        EventToken(
            "comm",
            TokenType.ACTION_COMMUNICATION,
            datetime.now(),
            np.random.randn(64),
            agent_perspective="victim",
        ),
        EventToken(
            "trans",
            TokenType.ACTION_TRANSACTION,
            datetime.now(),
            np.random.randn(64),
            agent_perspective="perpetrator",
        ),
        EventToken("end", TokenType.SEQUENCE_END, datetime.now(), np.random.randn(64)),
    ]

    schema.tokenized_timeline = tokens

    # Compute cross-attention
    cross_attention = schema._compute_cross_attention(head1, head2)

    # Check cross-attention properties
    assert cross_attention.shape == (4, 4)
    assert np.allclose(np.sum(cross_attention, axis=1), 1.0, atol=1e-6)
    assert np.all(cross_attention >= 0)

    print("✓ Cross-attention test passed")


def test_integrated_analysis():
    """Test the full integrated analysis pipeline"""
    print("Testing integrated analysis...")

    # Create simple framework
    framework = HyperGNNFramework("integration_test")

    # Add agents
    victim = Agent("victim_001", AgentType.INDIVIDUAL, "Victim")
    perpetrator = Agent("perp_001", AgentType.INDIVIDUAL, "Perpetrator")
    framework.add_agent(victim)
    framework.add_agent(perpetrator)

    # Add event
    event = DiscreteEvent(
        "crime_event",
        datetime.now(),
        EventType.TRANSACTION,
        ["victim_001", "perp_001"],
        "Criminal transaction event",
    )
    framework.add_event(event)

    # Create transformer schema
    schema = LLMTransformerSchema("integration_test", embed_dim=64, num_heads=2)

    # Run analysis
    analysis = schema.process_timeline_with_attention([event], framework.agents)

    # Validate analysis results
    assert "tokenized_sequence_length" in analysis
    assert "attention_heads" in analysis
    assert "self_attention_analysis" in analysis
    assert "cross_attention_analysis" in analysis
    assert "perspective_correlations" in analysis
    assert "timeline_insights" in analysis

    assert analysis["tokenized_sequence_length"] > 0
    assert analysis["attention_heads"] == 2

    print("✓ Integrated analysis test passed")


def test_mmo_relevance_calculation():
    """Test motive, means, opportunity relevance calculations"""
    print("Testing MMO relevance calculations...")

    schema = LLMTransformerSchema("mmo_test", embed_dim=64)

    # Create agents dict (empty for this test)
    agents = {}

    # Test different event types
    events = [
        DiscreteEvent(
            "comm", datetime.now(), EventType.COMMUNICATION, [], "Communication"
        ),
        DiscreteEvent(
            "trans", datetime.now(), EventType.TRANSACTION, [], "Transaction"
        ),
        DiscreteEvent("decision", datetime.now(), EventType.DECISION, [], "Decision"),
        DiscreteEvent("meeting", datetime.now(), EventType.MEETING, [], "Meeting"),
    ]

    for event in events:
        motive_rel = schema.tokenizer._calculate_motive_relevance(event, agents)
        means_rel = schema.tokenizer._calculate_means_relevance(event, agents)
        opportunity_rel = schema.tokenizer._calculate_opportunity_relevance(
            event, agents
        )

        # All relevance scores should be between 0 and 1
        assert 0 <= motive_rel <= 1
        assert 0 <= means_rel <= 1
        assert 0 <= opportunity_rel <= 1

        # Transaction events should have high motive relevance
        if event.event_type == EventType.TRANSACTION:
            assert motive_rel >= 0.7

        # Decision events should have high means relevance
        if event.event_type == EventType.DECISION:
            assert means_rel >= 0.7

        # Meeting events should have high opportunity relevance
        if event.event_type == EventType.MEETING:
            assert opportunity_rel >= 0.7

    print("✓ MMO relevance calculation test passed")


def run_all_tests():
    """Run all test cases"""
    print("=== Running LLM/Transformer Schema Tests ===\n")

    try:
        test_token_creation()
        test_attention_head_creation()
        test_timeline_tokenization()
        test_attention_computation()
        test_cross_attention()
        test_integrated_analysis()
        test_mmo_relevance_calculation()

        print("\n=== ALL TESTS PASSED ===")
        return True

    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
