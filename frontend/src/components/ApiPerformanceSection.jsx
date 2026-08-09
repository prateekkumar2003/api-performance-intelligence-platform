import { useEffect, useState } from 'react';
import { getAPIEndpoints, getAPIPerformance } from '../api';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const ApiPerformanceSection = () => {
  const [endpoints, setEndpoints] = useState([]);
  const [selectedApi, setSelectedApi] = useState('');
  const [chartData, setChartData] = useState([]);
  const [loading, setLoading] = useState(false);

  // Fetch unique endpoints on mount
  useEffect(() => {
    const fetchEndpoints = async () => {
      try {
        const res = await getAPIEndpoints();
        setEndpoints(res.data);
        if (res.data.length > 0) {
          // Auto-select first API
          const firstApi = `${res.data[0].method} ${res.data[0].path}`;
          setSelectedApi(firstApi);
        }
      } catch (err) {
        console.error('Error fetching API endpoints:', err);
      }
    };
    fetchEndpoints();
  }, []);

  // Fetch performance data when selected API changes
  useEffect(() => {
    const fetchPerformance = async () => {
      if (!selectedApi) return;
      setLoading(true);
      try {
        const [method, ...pathParts] = selectedApi.split(' ');
        const path = pathParts.join(' ');
        const res = await getAPIPerformance(path, method);
        setChartData(res.data.data);
      } catch (err) {
        console.error('Error fetching API performance data:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchPerformance();
  }, [selectedApi]);

  return (
    <div style={{ marginTop: '48px' }}>
      <div style={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center', 
        marginBottom: '24px' 
      }}>
        <h2>API Performance</h2>
        
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <label style={{ fontWeight: 600, color: 'var(--text-secondary)' }}>Select API:</label>
          <select 
            value={selectedApi}
            onChange={(e) => setSelectedApi(e.target.value)}
            style={{
              padding: '8px 12px',
              borderRadius: '8px',
              border: '1px solid var(--border-color)',
              background: 'var(--bg-secondary)',
              color: 'var(--text-primary)',
              minWidth: '250px',
              cursor: 'pointer'
            }}
          >
            {endpoints.map((ep, idx) => (
              <option key={idx} value={`${ep.method} ${ep.path}`}>
                {ep.method} {ep.path}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div style={{ 
        background: 'var(--bg-secondary)', 
        padding: '24px', 
        borderRadius: '12px',
        border: '1px solid var(--border-color)',
        minHeight: '350px'
      }}>
        {loading ? (
          <div style={{ textAlign: 'center', color: 'var(--text-secondary)', marginTop: '100px' }}>
            Loading chart data...
          </div>
        ) : chartData.length === 0 ? (
          <div style={{ textAlign: 'center', color: 'var(--text-secondary)', marginTop: '100px' }}>
            No performance data available for this API.
          </div>
        ) : (
          <div style={{ width: '100%', height: '350px' }}>
            <ResponsiveContainer>
              <LineChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#333" vertical={false} />
                <XAxis 
                  dataKey="time" 
                  stroke="var(--text-secondary)" 
                  tick={{ fill: 'var(--text-secondary)', fontSize: 12 }} 
                  dy={10}
                />
                <YAxis 
                  stroke="var(--text-secondary)"
                  tick={{ fill: 'var(--text-secondary)', fontSize: 12 }} 
                  dx={-10}
                  label={{ value: 'Response Time (ms)', angle: -90, position: 'insideLeft', fill: 'var(--text-secondary)' }}
                />
                <Tooltip 
                  contentStyle={{ 
                    background: 'var(--bg-primary)', 
                    border: '1px solid var(--border-color)',
                    borderRadius: '8px',
                    color: 'var(--text-primary)'
                  }} 
                  itemStyle={{ color: 'var(--accent-cyan)' }}
                />
                <Line 
                  type="monotone" 
                  dataKey="avg_response_time" 
                  name="Avg Response Time" 
                  stroke="var(--accent-cyan)" 
                  strokeWidth={3}
                  dot={{ r: 4, fill: 'var(--bg-primary)', strokeWidth: 2 }}
                  activeDot={{ r: 6, fill: 'var(--accent-cyan)' }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>
    </div>
  );
};

export default ApiPerformanceSection;
