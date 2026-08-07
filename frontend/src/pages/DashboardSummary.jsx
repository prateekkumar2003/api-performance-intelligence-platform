import { useEffect, useState } from 'react';
import MetricCard from '../components/MetricCard';
import { getSummary, getTopProblematicAPIs } from '../api';
import DataTable from '../components/DataTable';

const DashboardSummary = () => {
  const [summary, setSummary] = useState(null);
  const [topApis, setTopApis] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [summaryRes, topApisRes] = await Promise.all([
          getSummary(),
          getTopProblematicAPIs()
        ]);
        
        setSummary(summaryRes.data);
        setTopApis(topApisRes.data);
      } catch (error) {
        console.error('Error fetching dashboard summary data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const columns = [
    { header: 'Path', accessor: 'path' },
    { 
      header: 'Total Requests', 
      accessor: 'total_requests',
      render: (row) => <span style={{color: 'var(--text-secondary)'}}>{row.total_requests}</span>
    },
    { 
      header: 'Avg Response Time', 
      accessor: 'avg_response',
      render: (row) => {
        const val = row.avg_response;
        let color = 'var(--accent-cyan)';
        if (val > 1000) color = 'var(--accent-pink)';
        else if (val > 500) color = 'var(--accent-warning)';
        
        return <span style={{ color, fontWeight: 500 }}>{val ? val.toFixed(2) : 0} ms</span>;
      }
    },
  ];

  if (loading) return <div>Loading...</div>;

  return (
    <div className="animate-fade-in">
      <h1>Dashboard Summary</h1>
      
      <div className="dashboard-grid">
        <MetricCard 
          title="Total Requests" 
          value={summary?.total_requests || 0} 
        />
        <MetricCard 
          title="Total Issues" 
          value={summary?.total_issues || 0} 
        />
        <MetricCard 
          title="Avg Response Time" 
          value={`${summary?.average_response_time_ms ? summary.average_response_time_ms.toFixed(2) : 0} ms`} 
        />
      </div>

      <h2 style={{ marginTop: '40px' }}>Top Problematic APIs</h2>
      <DataTable 
        columns={columns} 
        data={topApis} 
        keyField="path"
      />
    </div>
  );
};

export default DashboardSummary;
