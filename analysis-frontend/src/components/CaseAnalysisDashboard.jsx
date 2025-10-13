import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Button } from '@/components/ui/button.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select.jsx'
import { Input } from '@/components/ui/input.jsx'
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  Area,
  AreaChart
} from 'recharts'
import { 
  FileText, 
  Users, 
  Clock, 
  TrendingUp, 
  AlertTriangle,
  CheckCircle,
  Search,
  Filter,
  Download,
  Eye,
  Calendar,
  MapPin,
  Shield
} from 'lucide-react'

const CaseAnalysisDashboard = () => {
  const [selectedCase, setSelectedCase] = useState('case_2025_137857')
  const [timeRange, setTimeRange] = useState('30d')
  const [searchTerm, setSearchTerm] = useState('')

  // Sample case data
  const caseData = {
    case_2025_137857: {
      title: 'Financial Fraud Investigation',
      status: 'In Progress',
      priority: 'High',
      created: '2025-01-15',
      entities: 47,
      evidence: 89,
      events: 156,
      completion: 73,
      timeline: [
        { date: '2025-01-15', events: 12, entities: 8 },
        { date: '2025-01-20', events: 23, entities: 15 },
        { date: '2025-01-25', events: 34, entities: 28 },
        { date: '2025-01-30', events: 45, entities: 35 },
        { date: '2025-02-05', events: 67, entities: 41 },
        { date: '2025-02-10', events: 89, entities: 47 }
      ],
      entityTypes: [
        { name: 'Persons', value: 18, color: '#3b82f6' },
        { name: 'Organizations', value: 12, color: '#10b981' },
        { name: 'Accounts', value: 8, color: '#f59e0b' },
        { name: 'Locations', value: 6, color: '#ef4444' },
        { name: 'Documents', value: 3, color: '#8b5cf6' }
      ],
      evidenceStatus: [
        { status: 'Verified', count: 45, color: '#10b981' },
        { status: 'Pending', count: 28, color: '#f59e0b' },
        { status: 'Disputed', count: 12, color: '#ef4444' },
        { status: 'Archived', count: 4, color: '#6b7280' }
      ]
    }
  }

  const currentCase = caseData[selectedCase]

  const recentActivity = [
    { 
      id: 1, 
      type: 'entity_added', 
      description: 'New person entity: John Smith', 
      timestamp: '2 hours ago',
      icon: Users,
      color: 'text-blue-600'
    },
    { 
      id: 2, 
      type: 'evidence_verified', 
      description: 'Bank statement #4521 verified', 
      timestamp: '4 hours ago',
      icon: CheckCircle,
      color: 'text-green-600'
    },
    { 
      id: 3, 
      type: 'connection_found', 
      description: 'New relationship: Smith → ABC Corp', 
      timestamp: '6 hours ago',
      icon: TrendingUp,
      color: 'text-purple-600'
    },
    { 
      id: 4, 
      type: 'alert', 
      description: 'Suspicious transaction pattern detected', 
      timestamp: '8 hours ago',
      icon: AlertTriangle,
      color: 'text-red-600'
    }
  ]

  const keyFindings = [
    {
      title: 'Transaction Pattern Anomaly',
      description: 'Unusual transaction patterns detected between accounts A-4521 and B-7832',
      severity: 'High',
      confidence: 87,
      entities: ['Account A-4521', 'Account B-7832', 'John Smith']
    },
    {
      title: 'Document Inconsistency',
      description: 'Conflicting information found in financial statements',
      severity: 'Medium',
      confidence: 72,
      entities: ['ABC Corporation', 'Financial Statement #3']
    },
    {
      title: 'Network Connection',
      description: 'Previously unknown connection between key entities discovered',
      severity: 'Medium',
      confidence: 94,
      entities: ['John Smith', 'ABC Corporation', 'XYZ Holdings']
    }
  ]

  return (
    <div className="space-y-6">
      {/* Header Controls */}
      <div className="flex flex-col sm:flex-row gap-4 items-start sm:items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold">Case Analysis Dashboard</h2>
          <p className="text-muted-foreground">Comprehensive case insights and analytics</p>
        </div>
        <div className="flex gap-2">
          <Select value={selectedCase} onValueChange={setSelectedCase}>
            <SelectTrigger className="w-[200px]">
              <SelectValue placeholder="Select case" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="case_2025_137857">Case 2025-137857</SelectItem>
              <SelectItem value="case_2025_138901">Case 2025-138901</SelectItem>
              <SelectItem value="case_2025_139245">Case 2025-139245</SelectItem>
            </SelectContent>
          </Select>
          <Select value={timeRange} onValueChange={setTimeRange}>
            <SelectTrigger className="w-[120px]">
              <SelectValue placeholder="Time range" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="7d">7 days</SelectItem>
              <SelectItem value="30d">30 days</SelectItem>
              <SelectItem value="90d">90 days</SelectItem>
              <SelectItem value="1y">1 year</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>

      {/* Case Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-muted-foreground">Entities</p>
                <p className="text-2xl font-bold">{currentCase.entities}</p>
              </div>
              <Users className="h-8 w-8 text-blue-600" />
            </div>
            <div className="mt-4">
              <Progress value={75} className="h-2" />
              <p className="text-xs text-muted-foreground mt-1">75% analyzed</p>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-muted-foreground">Evidence Items</p>
                <p className="text-2xl font-bold">{currentCase.evidence}</p>
              </div>
              <Shield className="h-8 w-8 text-green-600" />
            </div>
            <div className="mt-4">
              <Progress value={currentCase.completion} className="h-2" />
              <p className="text-xs text-muted-foreground mt-1">{currentCase.completion}% processed</p>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-muted-foreground">Timeline Events</p>
                <p className="text-2xl font-bold">{currentCase.events}</p>
              </div>
              <Clock className="h-8 w-8 text-purple-600" />
            </div>
            <div className="mt-4">
              <Badge variant={currentCase.status === 'In Progress' ? 'default' : 'secondary'}>
                {currentCase.status}
              </Badge>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-muted-foreground">Priority</p>
                <p className="text-2xl font-bold">{currentCase.priority}</p>
              </div>
              <AlertTriangle className={`h-8 w-8 ${currentCase.priority === 'High' ? 'text-red-600' : 'text-yellow-600'}`} />
            </div>
            <div className="mt-4">
              <p className="text-xs text-muted-foreground">Created: {currentCase.created}</p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Main Analytics */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Timeline Chart */}
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle>Case Timeline Analysis</CardTitle>
            <CardDescription>Entity and event discovery over time</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <AreaChart data={currentCase.timeline}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Area 
                  type="monotone" 
                  dataKey="events" 
                  stackId="1"
                  stroke="#3b82f6" 
                  fill="#3b82f6" 
                  fillOpacity={0.6}
                />
                <Area 
                  type="monotone" 
                  dataKey="entities" 
                  stackId="1"
                  stroke="#10b981" 
                  fill="#10b981" 
                  fillOpacity={0.6}
                />
              </AreaChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Entity Distribution */}
        <Card>
          <CardHeader>
            <CardTitle>Entity Distribution</CardTitle>
            <CardDescription>Breakdown by entity type</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={currentCase.entityTypes}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={100}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {currentCase.entityTypes.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
            <div className="mt-4 space-y-2">
              {currentCase.entityTypes.map((type, index) => (
                <div key={index} className="flex items-center justify-between text-sm">
                  <div className="flex items-center space-x-2">
                    <div 
                      className="w-3 h-3 rounded-full" 
                      style={{ backgroundColor: type.color }}
                    />
                    <span>{type.name}</span>
                  </div>
                  <span className="font-medium">{type.value}</span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Key Findings and Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Key Findings */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <TrendingUp className="h-5 w-5 mr-2" />
              Key Findings
            </CardTitle>
            <CardDescription>Important discoveries and insights</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {keyFindings.map((finding, index) => (
                <div key={index} className="border rounded-lg p-4 space-y-2">
                  <div className="flex items-center justify-between">
                    <h4 className="font-medium">{finding.title}</h4>
                    <Badge variant={finding.severity === 'High' ? 'destructive' : 'secondary'}>
                      {finding.severity}
                    </Badge>
                  </div>
                  <p className="text-sm text-muted-foreground">{finding.description}</p>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <span className="text-xs text-muted-foreground">Confidence:</span>
                      <Progress value={finding.confidence} className="w-20 h-2" />
                      <span className="text-xs font-medium">{finding.confidence}%</span>
                    </div>
                    <Button variant="ghost" size="sm">
                      <Eye className="h-4 w-4 mr-1" />
                      View
                    </Button>
                  </div>
                  <div className="flex flex-wrap gap-1 mt-2">
                    {finding.entities.map((entity, idx) => (
                      <Badge key={idx} variant="outline" className="text-xs">
                        {entity}
                      </Badge>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Recent Activity */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Clock className="h-5 w-5 mr-2" />
              Recent Activity
            </CardTitle>
            <CardDescription>Latest updates and changes</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {recentActivity.map((activity) => (
                <div key={activity.id} className="flex items-start space-x-3">
                  <div className={`p-2 rounded-full bg-muted ${activity.color}`}>
                    <activity.icon className="h-4 w-4" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium">{activity.description}</p>
                    <p className="text-xs text-muted-foreground">{activity.timestamp}</p>
                  </div>
                </div>
              ))}
            </div>
            <Button variant="outline" className="w-full mt-4">
              View All Activity
            </Button>
          </CardContent>
        </Card>
      </div>

      {/* Evidence Status */}
      <Card>
        <CardHeader>
          <CardTitle>Evidence Processing Status</CardTitle>
          <CardDescription>Current status of evidence items in the case</CardDescription>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={currentCase.evidenceStatus}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="status" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="count" fill="#3b82f6" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    </div>
  )
}

export default CaseAnalysisDashboard
