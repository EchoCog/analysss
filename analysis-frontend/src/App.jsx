import { useState } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import NetworkVisualization from './components/NetworkVisualization.jsx'
import CaseAnalysisDashboard from './components/CaseAnalysisDashboard.jsx'
import { 
  Network, 
  Database, 
  FileText, 
  BarChart3, 
  Search, 
  Settings, 
  Brain,
  Shield,
  Clock,
  Users,
  TrendingUp,
  Activity
} from 'lucide-react'
import './App.css'

function App() {
  const [activeTab, setActiveTab] = useState('dashboard')

  const stats = [
    { title: 'Active Cases', value: '24', icon: FileText, trend: '+12%', color: 'text-blue-600' },
    { title: 'Entities Analyzed', value: '1,847', icon: Users, trend: '+8%', color: 'text-green-600' },
    { title: 'Evidence Items', value: '3,291', icon: Shield, trend: '+15%', color: 'text-purple-600' },
    { title: 'Processing Time', value: '2.3s', icon: Clock, trend: '-23%', color: 'text-orange-600' }
  ]

  const recentCases = [
    { id: 'case_2025_137857', title: 'Financial Fraud Investigation', status: 'In Progress', priority: 'High', entities: 47 },
    { id: 'case_2025_138901', title: 'Corporate Compliance Review', status: 'Completed', priority: 'Medium', entities: 23 },
    { id: 'case_2025_139245', title: 'Evidence Chain Analysis', status: 'Pending', priority: 'High', entities: 89 }
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800">
      {/* Header */}
      <header className="border-b bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <Brain className="h-8 w-8 text-blue-600" />
                <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                  HyperGNN Analysis
                </h1>
              </div>
              <Badge variant="secondary" className="text-xs">
                Framework v2.1
              </Badge>
            </div>
            <div className="flex items-center space-x-4">
              <Button variant="outline" size="sm">
                <Search className="h-4 w-4 mr-2" />
                Search
              </Button>
              <Button variant="outline" size="sm">
                <Settings className="h-4 w-4 mr-2" />
                Settings
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-6 py-8">
        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
          <TabsList className="grid w-full grid-cols-4 lg:w-[600px]">
            <TabsTrigger value="dashboard">Dashboard</TabsTrigger>
            <TabsTrigger value="analysis">Analysis</TabsTrigger>
            <TabsTrigger value="visualization">Visualization</TabsTrigger>
            <TabsTrigger value="reports">Reports</TabsTrigger>
          </TabsList>

          <TabsContent value="dashboard" className="space-y-6">
            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {stats.map((stat, index) => (
                <Card key={index} className="relative overflow-hidden">
                  <CardContent className="p-6">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm font-medium text-muted-foreground">{stat.title}</p>
                        <p className="text-3xl font-bold">{stat.value}</p>
                        <p className={`text-sm ${stat.color} flex items-center mt-1`}>
                          <TrendingUp className="h-3 w-3 mr-1" />
                          {stat.trend}
                        </p>
                      </div>
                      <div className={`p-3 rounded-full bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20`}>
                        <stat.icon className={`h-6 w-6 ${stat.color}`} />
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>

            {/* Main Dashboard Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Recent Cases */}
              <Card className="lg:col-span-2">
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <FileText className="h-5 w-5 mr-2" />
                    Recent Cases
                  </CardTitle>
                  <CardDescription>
                    Latest case analysis and processing status
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {recentCases.map((case_item, index) => (
                      <div key={index} className="flex items-center justify-between p-4 border rounded-lg hover:bg-muted/50 transition-colors">
                        <div className="space-y-1">
                          <p className="font-medium">{case_item.title}</p>
                          <p className="text-sm text-muted-foreground">{case_item.id}</p>
                          <div className="flex items-center space-x-2">
                            <Badge variant={case_item.status === 'Completed' ? 'default' : case_item.status === 'In Progress' ? 'secondary' : 'outline'}>
                              {case_item.status}
                            </Badge>
                            <Badge variant={case_item.priority === 'High' ? 'destructive' : 'secondary'}>
                              {case_item.priority}
                            </Badge>
                          </div>
                        </div>
                        <div className="text-right">
                          <p className="text-sm text-muted-foreground">{case_item.entities} entities</p>
                          <Button variant="ghost" size="sm" className="mt-1">
                            View Details
                          </Button>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              {/* System Status */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <Activity className="h-5 w-5 mr-2" />
                    System Status
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <div className="h-2 w-2 bg-green-500 rounded-full"></div>
                      <span className="text-sm">HyperGNN Core</span>
                    </div>
                    <Badge variant="secondary">Online</Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <div className="h-2 w-2 bg-green-500 rounded-full"></div>
                      <span className="text-sm">Database</span>
                    </div>
                    <Badge variant="secondary">Connected</Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <div className="h-2 w-2 bg-yellow-500 rounded-full"></div>
                      <span className="text-sm">Processing Queue</span>
                    </div>
                    <Badge variant="outline">3 pending</Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <div className="h-2 w-2 bg-green-500 rounded-full"></div>
                      <span className="text-sm">API Gateway</span>
                    </div>
                    <Badge variant="secondary">Healthy</Badge>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          <TabsContent value="analysis" className="space-y-6">
            <CaseAnalysisDashboard />
          </TabsContent>

          <TabsContent value="visualization" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <BarChart3 className="h-5 w-5 mr-2" />
                  Interactive Network Visualization
                </CardTitle>
                <CardDescription>
                  Hypergraph network analysis with D3.js and interactive controls
                </CardDescription>
              </CardHeader>
              <CardContent>
                <NetworkVisualization width={800} height={600} />
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="reports" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <FileText className="h-5 w-5 mr-2" />
                  Analysis Reports
                </CardTitle>
                <CardDescription>
                  Generate and export comprehensive analysis reports
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <Button variant="outline" className="h-24 flex-col">
                    <FileText className="h-8 w-8 mb-2" />
                    Case Summary Report
                  </Button>
                  <Button variant="outline" className="h-24 flex-col">
                    <Network className="h-8 w-8 mb-2" />
                    Network Analysis Report
                  </Button>
                  <Button variant="outline" className="h-24 flex-col">
                    <BarChart3 className="h-8 w-8 mb-2" />
                    Statistical Analysis
                  </Button>
                  <Button variant="outline" className="h-24 flex-col">
                    <Shield className="h-8 w-8 mb-2" />
                    Evidence Chain Report
                  </Button>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </main>
    </div>
  )
}

export default App
