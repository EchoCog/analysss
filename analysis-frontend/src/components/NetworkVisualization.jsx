import { useEffect, useRef, useState } from 'react'
import * as d3 from 'd3'
import * as anime from 'animejs'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Button } from '@/components/ui/button.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Slider } from '@/components/ui/slider.jsx'
import { Play, Pause, RotateCcw, ZoomIn, ZoomOut } from 'lucide-react'

const NetworkVisualization = ({ data = null, width = 800, height = 600 }) => {
  const svgRef = useRef()
  const [isPlaying, setIsPlaying] = useState(false)
  const [selectedNode, setSelectedNode] = useState(null)
  const [zoomLevel, setZoomLevel] = useState(1)
  const [nodeCount, setNodeCount] = useState(50)

  // Generate sample hypergraph data if none provided
  const generateSampleData = (numNodes = 50) => {
    const nodes = []
    const links = []
    
    // Create entity nodes with different types
    const entityTypes = ['Person', 'Organization', 'Location', 'Event', 'Evidence']
    const colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6']
    
    for (let i = 0; i < numNodes; i++) {
      const type = entityTypes[Math.floor(Math.random() * entityTypes.length)]
      nodes.push({
        id: `entity_${i}`,
        name: `${type} ${i + 1}`,
        type: type,
        color: colors[entityTypes.indexOf(type)],
        size: Math.random() * 15 + 5,
        connections: Math.floor(Math.random() * 8) + 1
      })
    }
    
    // Create hyperedges (connections between multiple nodes)
    for (let i = 0; i < numNodes * 1.5; i++) {
      const source = Math.floor(Math.random() * numNodes)
      const target = Math.floor(Math.random() * numNodes)
      if (source !== target) {
        links.push({
          source: `entity_${source}`,
          target: `entity_${target}`,
          strength: Math.random(),
          type: 'relationship'
        })
      }
    }
    
    return { nodes, links }
  }

  useEffect(() => {
    if (!svgRef.current) return

    const sampleData = data || generateSampleData(nodeCount)
    const svg = d3.select(svgRef.current)
    
    // Clear previous content
    svg.selectAll("*").remove()
    
    // Set up SVG dimensions
    svg.attr("width", width).attr("height", height)
    
    // Create zoom behavior
    const zoom = d3.zoom()
      .scaleExtent([0.1, 4])
      .on("zoom", (event) => {
        g.attr("transform", event.transform)
        setZoomLevel(event.transform.k)
      })
    
    svg.call(zoom)
    
    // Create main group for zooming/panning
    const g = svg.append("g")
    
    // Create force simulation
    const simulation = d3.forceSimulation(sampleData.nodes)
      .force("link", d3.forceLink(sampleData.links).id(d => d.id).distance(80))
      .force("charge", d3.forceManyBody().strength(-300))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force("collision", d3.forceCollide().radius(d => d.size + 2))
    
    // Create gradient definitions for enhanced visuals
    const defs = svg.append("defs")
    
    // Create radial gradient for nodes
    const gradient = defs.append("radialGradient")
      .attr("id", "nodeGradient")
      .attr("cx", "30%")
      .attr("cy", "30%")
    
    gradient.append("stop")
      .attr("offset", "0%")
      .attr("stop-color", "#ffffff")
      .attr("stop-opacity", 0.8)
    
    gradient.append("stop")
      .attr("offset", "100%")
      .attr("stop-color", "#000000")
      .attr("stop-opacity", 0.1)
    
    // Create links
    const link = g.append("g")
      .selectAll("line")
      .data(sampleData.links)
      .enter().append("line")
      .attr("stroke", "#999")
      .attr("stroke-opacity", 0.6)
      .attr("stroke-width", d => Math.sqrt(d.strength * 5))
      .style("filter", "drop-shadow(0px 0px 2px rgba(0,0,0,0.1))")
    
    // Create nodes
    const node = g.append("g")
      .selectAll("circle")
      .data(sampleData.nodes)
      .enter().append("circle")
      .attr("r", d => d.size)
      .attr("fill", d => d.color)
      .attr("stroke", "#fff")
      .attr("stroke-width", 2)
      .style("filter", "drop-shadow(0px 2px 4px rgba(0,0,0,0.2))")
      .style("cursor", "pointer")
      .call(d3.drag()
        .on("start", dragstarted)
        .on("drag", dragged)
        .on("end", dragended))
    
    // Add hover effects
    node.on("mouseover", function(event, d) {
      d3.select(this)
        .transition()
        .duration(200)
        .attr("r", d.size * 1.2)
        .attr("stroke-width", 3)
      
      // Highlight connected links
      link.style("stroke-opacity", l => 
        l.source.id === d.id || l.target.id === d.id ? 1 : 0.1
      )
    })
    .on("mouseout", function(event, d) {
      d3.select(this)
        .transition()
        .duration(200)
        .attr("r", d.size)
        .attr("stroke-width", 2)
      
      // Reset link opacity
      link.style("stroke-opacity", 0.6)
    })
    .on("click", function(event, d) {
      setSelectedNode(d)
      
      // Animate selection
      anime.default({
        targets: this,
        scale: [1, 1.3, 1],
        duration: 600,
        easing: 'easeOutElastic(1, .8)'
      })
    })
    
    // Add labels
    const labels = g.append("g")
      .selectAll("text")
      .data(sampleData.nodes)
      .enter().append("text")
      .text(d => d.name)
      .attr("font-size", "10px")
      .attr("font-family", "Arial, sans-serif")
      .attr("fill", "#333")
      .attr("text-anchor", "middle")
      .attr("dy", ".35em")
      .style("pointer-events", "none")
      .style("opacity", 0.8)
    
    // Update positions on simulation tick
    simulation.on("tick", () => {
      link
        .attr("x1", d => d.source.x)
        .attr("y1", d => d.source.y)
        .attr("x2", d => d.target.x)
        .attr("y2", d => d.target.y)
      
      node
        .attr("cx", d => d.x)
        .attr("cy", d => d.y)
      
      labels
        .attr("x", d => d.x)
        .attr("y", d => d.y + d.size + 15)
    })
    
    // Drag functions
    function dragstarted(event, d) {
      if (!event.active) simulation.alphaTarget(0.3).restart()
      d.fx = d.x
      d.fy = d.y
    }
    
    function dragged(event, d) {
      d.fx = event.x
      d.fy = event.y
    }
    
    function dragended(event, d) {
      if (!event.active) simulation.alphaTarget(0)
      d.fx = null
      d.fy = null
    }
    
    // Animation controls
    const animateNetwork = () => {
      if (isPlaying) {
        // Animate node positions
        anime.default({
          targets: sampleData.nodes,
          duration: 2000,
          easing: 'easeInOutSine',
          loop: true,
          direction: 'alternate',
          update: () => {
            simulation.alpha(0.1).restart()
          }
        })
      }
    }
    
    if (isPlaying) {
      animateNetwork()
    }
    
  }, [data, width, height, isPlaying, nodeCount])

  const handleZoomIn = () => {
    const svg = d3.select(svgRef.current)
    svg.transition().call(
      d3.zoom().scaleBy, 1.5
    )
  }

  const handleZoomOut = () => {
    const svg = d3.select(svgRef.current)
    svg.transition().call(
      d3.zoom().scaleBy, 1 / 1.5
    )
  }

  const handleReset = () => {
    const svg = d3.select(svgRef.current)
    svg.transition().call(
      d3.zoom().transform,
      d3.zoomIdentity
    )
    setZoomLevel(1)
  }

  return (
    <div className="space-y-4">
      {/* Controls */}
      <div className="flex items-center justify-between flex-wrap gap-4">
        <div className="flex items-center space-x-2">
          <Button
            variant={isPlaying ? "default" : "outline"}
            size="sm"
            onClick={() => setIsPlaying(!isPlaying)}
          >
            {isPlaying ? <Pause className="h-4 w-4 mr-2" /> : <Play className="h-4 w-4 mr-2" />}
            {isPlaying ? 'Pause' : 'Animate'}
          </Button>
          <Button variant="outline" size="sm" onClick={handleReset}>
            <RotateCcw className="h-4 w-4 mr-2" />
            Reset
          </Button>
        </div>
        
        <div className="flex items-center space-x-2">
          <Button variant="outline" size="sm" onClick={handleZoomOut}>
            <ZoomOut className="h-4 w-4" />
          </Button>
          <Badge variant="secondary">
            {Math.round(zoomLevel * 100)}%
          </Badge>
          <Button variant="outline" size="sm" onClick={handleZoomIn}>
            <ZoomIn className="h-4 w-4" />
          </Button>
        </div>
      </div>

      {/* Node Count Slider */}
      <div className="flex items-center space-x-4">
        <span className="text-sm font-medium">Nodes:</span>
        <Slider
          value={[nodeCount]}
          onValueChange={(value) => setNodeCount(value[0])}
          max={200}
          min={10}
          step={10}
          className="flex-1 max-w-xs"
        />
        <Badge variant="outline">{nodeCount}</Badge>
      </div>

      {/* Main Visualization */}
      <Card>
        <CardContent className="p-0">
          <div className="relative bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-800 dark:to-slate-900 rounded-lg overflow-hidden">
            <svg
              ref={svgRef}
              className="w-full h-full"
              style={{ minHeight: `${height}px` }}
            />
          </div>
        </CardContent>
      </Card>

      {/* Selected Node Info */}
      {selectedNode && (
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Selected Entity</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className="text-sm font-medium">Name</p>
                <p className="text-lg">{selectedNode.name}</p>
              </div>
              <div>
                <p className="text-sm font-medium">Type</p>
                <Badge style={{ backgroundColor: selectedNode.color }}>
                  {selectedNode.type}
                </Badge>
              </div>
              <div>
                <p className="text-sm font-medium">Connections</p>
                <p className="text-lg">{selectedNode.connections}</p>
              </div>
              <div>
                <p className="text-sm font-medium">ID</p>
                <p className="text-sm text-muted-foreground font-mono">{selectedNode.id}</p>
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}

export default NetworkVisualization
