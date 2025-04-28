import React, { useState } from 'react';
import styled from 'styled-components';
import api from '../utils/api';

const DebugContainer = styled.div`
  margin-top: 20px;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: var(--border-radius);
  border: 1px solid #e5e7eb;
`;

const DebugButton = styled.button`
  background: #6c757d;
  color: white;
  margin-right: 10px;
  
  &:hover {
    background: #5a6268;
  }
`;

const DebugResult = styled.pre`
  margin-top: 15px;
  padding: 10px;
  background: #343a40;
  color: #f8f9fa;
  border-radius: var(--border-radius);
  overflow: auto;
  max-height: 200px;
  font-size: 12px;
`;

function ApiDebug() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const testConnection = async () => {
    setLoading(true);
    setError(null);
    
    try {
      // Check the API URL being used
      const apiUrl = process.env.REACT_APP_API_URL || 'Using relative URL (development)';
      
      // Make a simple API request
      const response = await api.get('/');
      setResult({
        apiUrl,
        status: response.status,
        data: response.data
      });
    } catch (err) {
      setError({
        message: err.message,
        apiUrl: process.env.REACT_APP_API_URL || 'Using relative URL (development)',
        response: err.response?.data
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <DebugContainer>
      <h4>API Connection Debugger</h4>
      <DebugButton onClick={testConnection} disabled={loading}>
        {loading ? 'Testing...' : 'Test API Connection'}
      </DebugButton>
      
      {error && (
        <DebugResult>
          ERROR: {JSON.stringify(error, null, 2)}
        </DebugResult>
      )}
      
      {result && !error && (
        <DebugResult>
          {JSON.stringify(result, null, 2)}
        </DebugResult>
      )}
    </DebugContainer>
  );
}

export default ApiDebug;
