// API Service for HyperGNN Analysis Framework
// Handles all backend API communications

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api'

class ApiService {
  constructor() {
    this.baseURL = API_BASE_URL
    this.headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    }
  }

  // Generic request method
  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`
    const config = {
      headers: this.headers,
      ...options
    }

    try {
      const response = await fetch(url, config)
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const contentType = response.headers.get('content-type')
      if (contentType && contentType.includes('application/json')) {
        return await response.json()
      }
      
      return await response.text()
    } catch (error) {
      console.error(`API request failed for ${endpoint}:`, error)
      throw error
    }
  }

  // GET request
  async get(endpoint) {
    return this.request(endpoint, { method: 'GET' })
  }

  // POST request
  async post(endpoint, data) {
    return this.request(endpoint, {
      method: 'POST',
      body: JSON.stringify(data)
    })
  }

  // PUT request
  async put(endpoint, data) {
    return this.request(endpoint, {
      method: 'PUT',
      body: JSON.stringify(data)
    })
  }

  // DELETE request
  async delete(endpoint) {
    return this.request(endpoint, { method: 'DELETE' })
  }

  // Case Management APIs
  async getCases() {
    return this.get('/cases')
  }

  async getCase(caseId) {
    return this.get(`/cases/${caseId}`)
  }

  async createCase(caseData) {
    return this.post('/cases', caseData)
  }

  async updateCase(caseId, caseData) {
    return this.put(`/cases/${caseId}`, caseData)
  }

  async deleteCase(caseId) {
    return this.delete(`/cases/${caseId}`)
  }

  // Entity Management APIs
  async getEntities(caseId) {
    return this.get(`/cases/${caseId}/entities`)
  }

  async createEntity(caseId, entityData) {
    return this.post(`/cases/${caseId}/entities`, entityData)
  }

  async updateEntity(caseId, entityId, entityData) {
    return this.put(`/cases/${caseId}/entities/${entityId}`, entityData)
  }

  async deleteEntity(caseId, entityId) {
    return this.delete(`/cases/${caseId}/entities/${entityId}`)
  }

  // Evidence Management APIs
  async getEvidence(caseId) {
    return this.get(`/cases/${caseId}/evidence`)
  }

  async uploadEvidence(caseId, evidenceFile) {
    const formData = new FormData()
    formData.append('evidence', evidenceFile)
    
    return this.request(`/cases/${caseId}/evidence`, {
      method: 'POST',
      body: formData,
      headers: {} // Let browser set content-type for FormData
    })
  }

  async updateEvidence(caseId, evidenceId, evidenceData) {
    return this.put(`/cases/${caseId}/evidence/${evidenceId}`, evidenceData)
  }

  async deleteEvidence(caseId, evidenceId) {
    return this.delete(`/cases/${caseId}/evidence/${evidenceId}`)
  }

  // HyperGNN Analysis APIs
  async runHyperGNNAnalysis(caseId, analysisConfig) {
    return this.post(`/cases/${caseId}/analyze`, analysisConfig)
  }

  async getAnalysisResults(caseId, analysisId) {
    return this.get(`/cases/${caseId}/analysis/${analysisId}`)
  }

  async getNetworkData(caseId) {
    return this.get(`/cases/${caseId}/network`)
  }

  // Statistics and Reporting APIs
  async getDashboardStats() {
    return this.get('/dashboard/stats')
  }

  async getCaseTimeline(caseId) {
    return this.get(`/cases/${caseId}/timeline`)
  }

  async getEntityDistribution(caseId) {
    return this.get(`/cases/${caseId}/entity-distribution`)
  }

  async generateReport(caseId, reportType) {
    return this.get(`/cases/${caseId}/reports/${reportType}`)
  }

  // System Status APIs
  async getSystemStatus() {
    return this.get('/system/status')
  }

  async getProcessingQueue() {
    return this.get('/system/queue')
  }

  // Search and Filter APIs
  async searchEntities(query, filters = {}) {
    const params = new URLSearchParams({ query, ...filters })
    return this.get(`/search/entities?${params}`)
  }

  async searchEvidence(query, filters = {}) {
    const params = new URLSearchParams({ query, ...filters })
    return this.get(`/search/evidence?${params}`)
  }

  // Real-time Updates (WebSocket simulation with polling)
  async subscribeToUpdates(caseId, callback) {
    const pollInterval = 5000 // 5 seconds
    
    const poll = async () => {
      try {
        const updates = await this.get(`/cases/${caseId}/updates`)
        callback(updates)
      } catch (error) {
        console.error('Failed to fetch updates:', error)
      }
    }

    const intervalId = setInterval(poll, pollInterval)
    
    // Return unsubscribe function
    return () => clearInterval(intervalId)
  }

  // Batch Operations
  async batchUpdateEntities(caseId, updates) {
    return this.post(`/cases/${caseId}/entities/batch`, { updates })
  }

  async batchDeleteEntities(caseId, entityIds) {
    return this.post(`/cases/${caseId}/entities/batch-delete`, { entityIds })
  }

  // Export and Import APIs
  async exportCase(caseId, format = 'json') {
    return this.get(`/cases/${caseId}/export?format=${format}`)
  }

  async importCase(caseData) {
    return this.post('/cases/import', caseData)
  }

  // Configuration APIs
  async getConfiguration() {
    return this.get('/config')
  }

  async updateConfiguration(config) {
    return this.put('/config', config)
  }

  // HyperGraphQL APIs
  async getGraphQLSchema() {
    return this.get('/v1/hypergraphql/schema')
  }

  async executeGraphQLQuery(query, variables = {}) {
    return this.post('/v1/hypergraphql/query', { query, variables })
  }

  async getHGQLNodes(nodeType = null, orgLevel = null) {
    let endpoint = '/v1/hypergraphql/nodes'
    const params = []
    if (nodeType) params.push(`type=${nodeType}`)
    if (orgLevel) params.push(`orgLevel=${orgLevel}`)
    if (params.length > 0) endpoint += `?${params.join('&')}`
    return this.get(endpoint)
  }

  async getHGQLNode(nodeId) {
    return this.get(`/v1/hypergraphql/nodes/${nodeId}`)
  }

  async createHGQLNode(nodeData) {
    return this.post('/v1/hypergraphql/nodes', nodeData)
  }

  async getHGQLEdges(edgeType = null, orgLevel = null) {
    let endpoint = '/v1/hypergraphql/edges'
    const params = []
    if (edgeType) params.push(`type=${edgeType}`)
    if (orgLevel) params.push(`orgLevel=${orgLevel}`)
    if (params.length > 0) endpoint += `?${params.join('&')}`
    return this.get(endpoint)
  }

  async getHGQLEdge(edgeId) {
    return this.get(`/v1/hypergraphql/edges/${edgeId}`)
  }

  async createHGQLEdge(edgeData) {
    return this.post('/v1/hypergraphql/edges', edgeData)
  }

  // GitHub Integration APIs
  async initGitHubRepoStructure(repoPath) {
    return this.post('/v1/hypergraphql/github/repo/init', { repoPath })
  }

  async projectSchemaToRepo(repoPath) {
    return this.post('/v1/hypergraphql/github/repo/project', { repoPath })
  }

  async loadFromGitHubRepo(repoPath, orgName) {
    return this.post('/v1/hypergraphql/github/repo/load', { repoPath, orgName })
  }

  async registerGitHubOrg(orgName, orgLevel = 'ORG') {
    return this.post('/v1/hypergraphql/github/org/register', { orgName, orgLevel })
  }

  async registerRepoToOrg(orgName, repoName, repoPath) {
    return this.post(`/v1/hypergraphql/github/org/${orgName}/repos`, { repoName, repoPath })
  }

  async aggregateOrgSchemas(orgName) {
    return this.post(`/v1/hypergraphql/github/org/${orgName}/aggregate`)
  }

  async getOrgStats(orgName) {
    return this.get(`/v1/hypergraphql/github/org/${orgName}/stats`)
  }

  async compressRepo(orgName, repoName, outputPath) {
    return this.post('/v1/hypergraphql/github/repo/compress', { orgName, repoName, outputPath })
  }

  async exportHGQLSchema(orgLevel = null) {
    let endpoint = '/v1/hypergraphql/export'
    if (orgLevel) endpoint += `?orgLevel=${orgLevel}`
    return this.get(endpoint)
  }

  // HGNNQL Integration APIs
  async executeHGNNQL(query, caseId = 'default_case') {
    return this.post('/v1/hypergraphql/hgnnql/query', { query, case_id: caseId })
  }

  async getAtomSpaceAtoms(caseId) {
    return this.get(`/v1/hypergraphql/hgnnql/atomspace/${caseId}/atoms`)
  }

  async convertHyperGNNToHGNNQL(caseId, hypergnnData) {
    return this.post('/v1/hypergraphql/hgnnql/convert/hypergnn', { case_id: caseId, hypergnn_data: hypergnnData })
  }
}

// Create and export singleton instance
const apiService = new ApiService()
export default apiService

// Export individual methods for convenience
export const {
  getCases,
  getCase,
  createCase,
  updateCase,
  deleteCase,
  getEntities,
  createEntity,
  updateEntity,
  deleteEntity,
  getEvidence,
  uploadEvidence,
  updateEvidence,
  deleteEvidence,
  runHyperGNNAnalysis,
  getAnalysisResults,
  getNetworkData,
  getDashboardStats,
  getCaseTimeline,
  getEntityDistribution,
  generateReport,
  getSystemStatus,
  getProcessingQueue,
  searchEntities,
  searchEvidence,
  subscribeToUpdates,
  batchUpdateEntities,
  batchDeleteEntities,
  exportCase,
  importCase,
  getConfiguration,
  updateConfiguration,
  getGraphQLSchema,
  executeGraphQLQuery,
  getHGQLNodes,
  getHGQLNode,
  createHGQLNode,
  getHGQLEdges,
  getHGQLEdge,
  createHGQLEdge,
  initGitHubRepoStructure,
  projectSchemaToRepo,
  loadFromGitHubRepo,
  registerGitHubOrg,
  registerRepoToOrg,
  aggregateOrgSchemas,
  getOrgStats,
  compressRepo,
  exportHGQLSchema
} = apiService
