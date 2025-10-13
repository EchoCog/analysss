#!/usr/bin/env python3
"""
HyperGNN Visualization Generator
Creates interactive D3.js visualization of the updated RegimA Group network
"""

import json
import os
from datetime import datetime
import hashlib
import math

def load_analysis_data():
    """Load all analysis data for visualization"""
    
    # Load hypergraph data
    with open('/home/ubuntu/analysis/super_sleuth_hypergraph.json', 'r') as f:
        hypergraph_data = json.load(f)
    
    # Load relationship analysis
    with open('/home/ubuntu/analysis/hyper_holmes_analysis.json', 'r') as f:
        holmes_data = json.load(f)
    
    # Load entity analysis
    with open('/home/ubuntu/analysis/super_sleuth_analysis.json', 'r') as f:
        sleuth_data = json.load(f)
    
    return hypergraph_data, holmes_data, sleuth_data

def generate_enhanced_nodes(hypergraph_data, holmes_data, sleuth_data):
    """Generate enhanced node data with new connection highlights"""
    
    nodes = []
    entity_relationships = holmes_data.get('entity_relationships', {})
    fraud_detection = holmes_data.get('fraud_detection', {})
    
    # Process entity nodes
    for node in hypergraph_data['nodes']:
        if node['type'] == 'entity':
            enhanced_node = {
                'id': node['id'],
                'label': node['label'],
                'type': node['type'],
                'category': node['category'],
                'size': 10,  # Base size
                'color': get_category_color(node['category']),
                'new_connection': True,  # All are new from this analysis
                'fraud_indicator': False,
                'relationship_strength': 0,
                'tooltip_data': {
                    'name': node['label'],
                    'type': node['category'],
                    'connections': 0,
                    'fraud_risk': 'Low'
                }
            }
            
            # Add relationship data if available
            if 'relationship_count' in node:
                enhanced_node['relationship_strength'] = node.get('total_relationship_strength', 0)
                enhanced_node['size'] = min(30, 10 + node['relationship_count'] * 2)
                enhanced_node['tooltip_data']['connections'] = node['relationship_count']
            
            # Check for fraud indicators
            fraud_entities = []
            for fraud_type, details in fraud_detection.items():
                if details.get('detected', False):
                    fraud_entities.extend(details.get('entities_involved', []))
            
            if any(entity.lower() in node['label'].lower() for entity in fraud_entities):
                enhanced_node['fraud_indicator'] = True
                enhanced_node['color'] = '#ff4444'  # Red for fraud
                enhanced_node['tooltip_data']['fraud_risk'] = 'High'
            
            nodes.append(enhanced_node)
        
        elif node['type'] == 'event':
            # Timeline event nodes
            event_node = {
                'id': node['id'],
                'label': node['label'],
                'type': 'event',
                'category': 'timeline',
                'size': 15,
                'color': '#ff6b6b',
                'new_connection': True,
                'fraud_indicator': False,
                'shape': 'square',
                'tooltip_data': {
                    'name': node['label'],
                    'type': 'Timeline Event',
                    'date': node.get('date', 'Unknown'),
                    'significance': 'High'
                }
            }
            nodes.append(event_node)
    
    return nodes

def generate_enhanced_edges(hypergraph_data, holmes_data):
    """Generate enhanced edge data with relationship strengths"""
    
    edges = []
    entity_relationships = holmes_data.get('entity_relationships', {})
    
    # Process existing edges from hypergraph
    for edge in hypergraph_data['edges']:
        enhanced_edge = {
            'id': edge['id'],
            'source': edge['source'],
            'target': edge['target'],
            'type': edge['type'],
            'weight': edge.get('weight', 1.0),
            'strength': 1,
            'color': '#999999',
            'width': 1,
            'new_connection': True,
            'animated': False
        }
        edges.append(enhanced_edge)
    
    # Add relationship edges from Holmes analysis
    for source_entity, relationships in entity_relationships.items():
        source_id = hashlib.md5(source_entity.encode()).hexdigest()[:8]
        
        for rel in relationships:
            target_id = hashlib.md5(rel['target'].encode()).hexdigest()[:8]
            
            # Create enhanced relationship edge
            rel_edge = {
                'id': f"rel_{source_id}_{target_id}",
                'source': source_id,
                'target': target_id,
                'type': 'financial_relationship',
                'weight': rel['strength'],
                'strength': rel['strength'],
                'color': get_relationship_color(rel['strength']),
                'width': min(8, 1 + rel['strength'] * 0.5),
                'new_connection': True,
                'animated': rel['strength'] > 5,  # Animate strong relationships
                'tooltip_data': {
                    'strength': rel['strength'],
                    'files': rel['file_count'],
                    'type': 'Financial Association'
                }
            }
            edges.append(rel_edge)
    
    return edges

def get_category_color(category):
    """Get color for entity category"""
    colors = {
        'companies': '#4a90e2',
        'financial_institutions': '#7ed321',
        'people': '#f5a623',
        'regulatory': '#d0021b',
        'timeline': '#ff6b6b'
    }
    return colors.get(category, '#999999')

def get_relationship_color(strength):
    """Get color based on relationship strength"""
    if strength >= 7:
        return '#d0021b'  # Red for very strong
    elif strength >= 4:
        return '#f5a623'  # Orange for strong
    elif strength >= 2:
        return '#7ed321'  # Green for moderate
    else:
        return '#4a90e2'  # Blue for weak

def calculate_layout_positions(nodes, edges):
    """Calculate force-directed layout positions"""
    
    # Simple force-directed layout calculation
    positions = {}
    center_x, center_y = 400, 300
    
    # Place nodes in categories
    category_positions = {
        'companies': (center_x, center_y),
        'financial_institutions': (center_x + 200, center_y - 100),
        'people': (center_x - 200, center_y - 100),
        'regulatory': (center_x, center_y + 150),
        'timeline': (center_x, center_y - 200)
    }
    
    category_counts = {}
    
    for node in nodes:
        category = node['category']
        if category not in category_counts:
            category_counts[category] = 0
        
        base_x, base_y = category_positions.get(category, (center_x, center_y))
        
        # Arrange nodes in a circle around category center
        angle = (category_counts[category] * 2 * math.pi) / max(1, len([n for n in nodes if n['category'] == category]))
        radius = 80 + (node['size'] * 2)
        
        x = base_x + radius * math.cos(angle)
        y = base_y + radius * math.sin(angle)
        
        positions[node['id']] = {'x': x, 'y': y}
        category_counts[category] += 1
    
    # Add positions to nodes
    for node in nodes:
        if node['id'] in positions:
            node.update(positions[node['id']])
    
    return nodes

def generate_d3_visualization():
    """Generate complete D3.js visualization"""
    
    # Load data
    hypergraph_data, holmes_data, sleuth_data = load_analysis_data()
    
    # Generate enhanced nodes and edges
    nodes = generate_enhanced_nodes(hypergraph_data, holmes_data, sleuth_data)
    edges = generate_enhanced_edges(hypergraph_data, holmes_data)
    
    # Calculate layout
    nodes = calculate_layout_positions(nodes, edges)
    
    # Create visualization data
    viz_data = {
        'nodes': nodes,
        'edges': edges,
        'metadata': {
            'title': 'RegimA Group HyperGNN Network',
            'subtitle': 'Updated Analysis with New Connections Highlighted',
            'generated_at': datetime.now().isoformat(),
            'total_nodes': len(nodes),
            'total_edges': len(edges),
            'fraud_indicators': len([n for n in nodes if n.get('fraud_indicator', False)]),
            'new_connections': len([e for e in edges if e.get('new_connection', False)])
        },
        'legend': {
            'node_categories': {
                'companies': {'color': '#4a90e2', 'description': 'RegimA Group Companies'},
                'financial_institutions': {'color': '#7ed321', 'description': 'Banks & Financial Services'},
                'people': {'color': '#f5a623', 'description': 'Key Individuals'},
                'regulatory': {'color': '#d0021b', 'description': 'Regulatory Bodies'},
                'timeline': {'color': '#ff6b6b', 'description': 'Timeline Events'}
            },
            'edge_types': {
                'financial_relationship': {'description': 'Financial Association'},
                'relationship': {'description': 'General Relationship'},
                'fraud_indicator': {'description': 'Fraud Risk Connection'}
            }
        }
    }
    
    return viz_data

def create_html_visualization(viz_data):
    """Create complete HTML visualization with D3.js"""
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RegimA Group HyperGNN Visualization</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/animejs/3.2.1/anime.min.js"></script>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 20px;
            backdrop-filter: blur(10px);
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 30px;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        .header p {{
            font-size: 1.2em;
            opacity: 0.9;
            margin: 10px 0;
        }}
        
        .stats {{
            display: flex;
            justify-content: space-around;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }}
        
        .stat-item {{
            background: rgba(255, 255, 255, 0.2);
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            margin: 5px;
            min-width: 120px;
        }}
        
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            display: block;
        }}
        
        .visualization-container {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            position: relative;
        }}
        
        #network-viz {{
            width: 100%;
            height: 600px;
            border: 2px solid #ddd;
            border-radius: 10px;
            background: #fafafa;
        }}
        
        .legend {{
            display: flex;
            justify-content: space-around;
            margin-top: 20px;
            flex-wrap: wrap;
        }}
        
        .legend-section {{
            background: rgba(255, 255, 255, 0.2);
            padding: 15px;
            border-radius: 10px;
            margin: 5px;
            flex: 1;
            min-width: 200px;
        }}
        
        .legend-item {{
            display: flex;
            align-items: center;
            margin: 5px 0;
        }}
        
        .legend-color {{
            width: 20px;
            height: 20px;
            border-radius: 50%;
            margin-right: 10px;
        }}
        
        .controls {{
            margin: 20px 0;
            text-align: center;
        }}
        
        .control-button {{
            background: rgba(255, 255, 255, 0.2);
            border: none;
            color: white;
            padding: 10px 20px;
            margin: 5px;
            border-radius: 25px;
            cursor: pointer;
            transition: all 0.3s ease;
        }}
        
        .control-button:hover {{
            background: rgba(255, 255, 255, 0.3);
            transform: translateY(-2px);
        }}
        
        .tooltip {{
            position: absolute;
            background: rgba(0, 0, 0, 0.9);
            color: white;
            padding: 10px;
            border-radius: 5px;
            pointer-events: none;
            font-size: 12px;
            z-index: 1000;
            opacity: 0;
            transition: opacity 0.3s;
        }}
        
        .node {{
            cursor: pointer;
            transition: all 0.3s ease;
        }}
        
        .node:hover {{
            stroke: #333;
            stroke-width: 3px;
        }}
        
        .edge {{
            transition: all 0.3s ease;
        }}
        
        .edge.highlighted {{
            stroke-width: 4px !important;
            opacity: 1 !important;
        }}
        
        .fraud-indicator {{
            animation: pulse 2s infinite;
        }}
        
        @keyframes pulse {{
            0% {{ opacity: 1; }}
            50% {{ opacity: 0.5; }}
            100% {{ opacity: 1; }}
        }}
        
        .new-connection {{
            animation: glow 3s ease-in-out infinite alternate;
        }}
        
        @keyframes glow {{
            from {{ filter: drop-shadow(0 0 5px currentColor); }}
            to {{ filter: drop-shadow(0 0 15px currentColor); }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🕸️ RegimA Group HyperGNN Network</h1>
            <p>Interactive Visualization with New Connections Highlighted</p>
            <p><em>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</em></p>
        </div>
        
        <div class="stats">
            <div class="stat-item">
                <span class="stat-number">{viz_data['metadata']['total_nodes']}</span>
                <span>Total Nodes</span>
            </div>
            <div class="stat-item">
                <span class="stat-number">{viz_data['metadata']['total_edges']}</span>
                <span>Total Edges</span>
            </div>
            <div class="stat-item">
                <span class="stat-number">{viz_data['metadata']['fraud_indicators']}</span>
                <span>Fraud Indicators</span>
            </div>
            <div class="stat-item">
                <span class="stat-number">{viz_data['metadata']['new_connections']}</span>
                <span>New Connections</span>
            </div>
        </div>
        
        <div class="controls">
            <button class="control-button" onclick="highlightFraudNodes()">🚨 Highlight Fraud Risk</button>
            <button class="control-button" onclick="highlightNewConnections()">✨ Show New Connections</button>
            <button class="control-button" onclick="animateNetwork()">🎬 Animate Network</button>
            <button class="control-button" onclick="resetView()">🔄 Reset View</button>
        </div>
        
        <div class="visualization-container">
            <svg id="network-viz"></svg>
            <div class="tooltip" id="tooltip"></div>
        </div>
        
        <div class="legend">
            <div class="legend-section">
                <h3>Node Categories</h3>
                <div class="legend-item">
                    <div class="legend-color" style="background-color: #4a90e2;"></div>
                    <span>Companies</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background-color: #7ed321;"></div>
                    <span>Financial Institutions</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background-color: #f5a623;"></div>
                    <span>Key Individuals</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background-color: #d0021b;"></div>
                    <span>Regulatory Bodies</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background-color: #ff6b6b;"></div>
                    <span>Timeline Events</span>
                </div>
            </div>
            
            <div class="legend-section">
                <h3>Connection Strength</h3>
                <div class="legend-item">
                    <div style="width: 20px; height: 3px; background-color: #d0021b; margin-right: 10px;"></div>
                    <span>Very Strong (7+)</span>
                </div>
                <div class="legend-item">
                    <div style="width: 20px; height: 2px; background-color: #f5a623; margin-right: 10px;"></div>
                    <span>Strong (4-6)</span>
                </div>
                <div class="legend-item">
                    <div style="width: 20px; height: 1px; background-color: #7ed321; margin-right: 10px;"></div>
                    <span>Moderate (2-3)</span>
                </div>
                <div class="legend-item">
                    <div style="width: 20px; height: 1px; background-color: #4a90e2; margin-right: 10px;"></div>
                    <span>Weak (1)</span>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Visualization data
        const data = {json.dumps(viz_data, indent=2)};
        
        // Set up SVG
        const svg = d3.select("#network-viz");
        const width = 1200;
        const height = 600;
        svg.attr("width", width).attr("height", height);
        
        // Create groups for different elements
        const edgeGroup = svg.append("g").attr("class", "edges");
        const nodeGroup = svg.append("g").attr("class", "nodes");
        
        // Set up force simulation
        const simulation = d3.forceSimulation(data.nodes)
            .force("link", d3.forceLink(data.edges).id(d => d.id).distance(100))
            .force("charge", d3.forceManyBody().strength(-300))
            .force("center", d3.forceCenter(width / 2, height / 2))
            .force("collision", d3.forceCollide().radius(d => d.size + 5));
        
        // Create edges
        const edges = edgeGroup.selectAll("line")
            .data(data.edges)
            .enter().append("line")
            .attr("class", d => `edge ${{d.new_connection ? 'new-connection' : ''}}`)
            .attr("stroke", d => d.color)
            .attr("stroke-width", d => d.width)
            .attr("opacity", 0.6);
        
        // Create nodes
        const nodes = nodeGroup.selectAll("circle")
            .data(data.nodes)
            .enter().append("circle")
            .attr("class", d => `node ${{d.fraud_indicator ? 'fraud-indicator' : ''}} ${{d.new_connection ? 'new-connection' : ''}}`)
            .attr("r", d => d.size)
            .attr("fill", d => d.color)
            .attr("stroke", "#fff")
            .attr("stroke-width", 2)
            .call(d3.drag()
                .on("start", dragstarted)
                .on("drag", dragged)
                .on("end", dragended))
            .on("mouseover", showTooltip)
            .on("mouseout", hideTooltip)
            .on("click", nodeClicked);
        
        // Add labels
        const labels = nodeGroup.selectAll("text")
            .data(data.nodes)
            .enter().append("text")
            .text(d => d.label)
            .attr("font-size", "10px")
            .attr("fill", "#333")
            .attr("text-anchor", "middle")
            .attr("dy", d => d.size + 15)
            .style("pointer-events", "none");
        
        // Update positions on simulation tick
        simulation.on("tick", () => {{
            edges
                .attr("x1", d => d.source.x)
                .attr("y1", d => d.source.y)
                .attr("x2", d => d.target.x)
                .attr("y2", d => d.target.y);
            
            nodes
                .attr("cx", d => d.x)
                .attr("cy", d => d.y);
            
            labels
                .attr("x", d => d.x)
                .attr("y", d => d.y);
        }});
        
        // Drag functions
        function dragstarted(event, d) {{
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
        }}
        
        function dragged(event, d) {{
            d.fx = event.x;
            d.fy = event.y;
        }}
        
        function dragended(event, d) {{
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
        }}
        
        // Tooltip functions
        function showTooltip(event, d) {{
            const tooltip = d3.select("#tooltip");
            const tooltipData = d.tooltip_data || {{}};
            
            let content = `<strong>${{d.label}}</strong><br/>`;
            content += `Type: ${{tooltipData.type || d.category}}<br/>`;
            if (tooltipData.connections) content += `Connections: ${{tooltipData.connections}}<br/>`;
            if (tooltipData.fraud_risk) content += `Fraud Risk: ${{tooltipData.fraud_risk}}<br/>`;
            if (d.fraud_indicator) content += `<span style="color: #ff4444;">⚠️ Fraud Indicator</span><br/>`;
            if (d.new_connection) content += `<span style="color: #7ed321;">✨ New Connection</span>`;
            
            tooltip.html(content)
                .style("left", (event.pageX + 10) + "px")
                .style("top", (event.pageY - 10) + "px")
                .style("opacity", 1);
        }}
        
        function hideTooltip() {{
            d3.select("#tooltip").style("opacity", 0);
        }}
        
        function nodeClicked(event, d) {{
            // Highlight connected nodes and edges
            const connectedEdges = data.edges.filter(e => e.source.id === d.id || e.target.id === d.id);
            const connectedNodeIds = new Set();
            connectedEdges.forEach(e => {{
                connectedNodeIds.add(e.source.id);
                connectedNodeIds.add(e.target.id);
            }});
            
            // Reset all elements
            nodes.attr("opacity", 0.3);
            edges.attr("opacity", 0.1);
            labels.attr("opacity", 0.3);
            
            // Highlight connected elements
            nodes.filter(n => connectedNodeIds.has(n.id)).attr("opacity", 1);
            edges.filter(e => connectedEdges.includes(e)).attr("opacity", 1).classed("highlighted", true);
            labels.filter(n => connectedNodeIds.has(n.id)).attr("opacity", 1);
        }}
        
        // Control functions
        function highlightFraudNodes() {{
            nodes.attr("opacity", d => d.fraud_indicator ? 1 : 0.3);
            edges.attr("opacity", 0.2);
            labels.attr("opacity", d => d.fraud_indicator ? 1 : 0.3);
        }}
        
        function highlightNewConnections() {{
            nodes.attr("opacity", d => d.new_connection ? 1 : 0.3);
            edges.attr("opacity", d => d.new_connection ? 0.8 : 0.1);
            labels.attr("opacity", d => d.new_connection ? 1 : 0.3);
        }}
        
        function animateNetwork() {{
            // Animate nodes with anime.js
            anime({{
                targets: '.node',
                scale: [1, 1.2, 1],
                duration: 2000,
                delay: anime.stagger(100),
                easing: 'easeInOutQuad'
            }});
            
            // Animate edges
            anime({{
                targets: '.edge',
                strokeDasharray: ['0 100', '100 0'],
                duration: 3000,
                delay: anime.stagger(50),
                easing: 'easeInOutQuad'
            }});
        }}
        
        function resetView() {{
            nodes.attr("opacity", 1);
            edges.attr("opacity", 0.6).classed("highlighted", false);
            labels.attr("opacity", 1);
            
            // Reset animation
            anime.remove('.node');
            anime.remove('.edge');
        }}
        
        // Initial animation
        setTimeout(() => {{
            animateNetwork();
        }}, 1000);
    </script>
</body>
</html>"""
    
    return html_content

def main():
    """Generate the complete HyperGNN visualization"""
    
    print("🎨 Generating HyperGNN Visualization...")
    print("=" * 60)
    
    # Generate visualization data
    viz_data = generate_d3_visualization()
    
    # Create HTML visualization
    html_content = create_html_visualization(viz_data)
    
    # Save files
    viz_file = '/home/ubuntu/analysis/hypergnn_visualization.html'
    data_file = '/home/ubuntu/analysis/hypergnn_viz_data.json'
    
    with open(viz_file, 'w') as f:
        f.write(html_content)
    
    with open(data_file, 'w') as f:
        json.dump(viz_data, f, indent=2)
    
    print(f"✅ Visualization generated!")
    print(f"🌐 HTML file: {viz_file}")
    print(f"📊 Data file: {data_file}")
    print(f"📈 Nodes: {viz_data['metadata']['total_nodes']}")
    print(f"🔗 Edges: {viz_data['metadata']['total_edges']}")
    print(f"🚨 Fraud indicators: {viz_data['metadata']['fraud_indicators']}")
    print(f"✨ New connections: {viz_data['metadata']['new_connections']}")
    
    return viz_data

if __name__ == "__main__":
    main()
