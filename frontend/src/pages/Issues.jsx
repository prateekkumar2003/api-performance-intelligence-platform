import { useEffect, useState } from 'react';
import DataTable from '../components/DataTable';
import { getPerformanceIssues } from '../api';
import AlertBadge from '../components/AlertBadge';

const Issues = () => {
  const [issues, setIssues] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await getPerformanceIssues();
        setIssues(res.data);
      } catch (error) {
        console.error('Error fetching performance issues:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const columns = [
    { 
      header: 'Severity', 
      accessor: 'severity',
      render: (row) => <AlertBadge type={row.severity} text={row.severity} />
    },
    { 
      header: 'Issue Type', 
      accessor: 'issue_type',
      render: (row) => <span style={{ fontWeight: 600 }}>{row.issue_type}</span>
    },
    { 
      header: 'Message', 
      accessor: 'message',
      render: (row) => <span style={{ color: 'var(--text-secondary)' }}>{row.message}</span>
    },
    { header: 'Path', accessor: 'path' },
    { 
      header: 'Detected At', 
      accessor: 'created_at',
      render: (row) => new Date(row.created_at).toLocaleString()
    },
  ];

  if (loading) return <div>Loading...</div>;

  return (
    <div className="animate-fade-in">
      <h1>Performance Issues</h1>
      <p style={{ marginBottom: '24px' }}>
        Identified performance anomalies and critical bottlenecks.
      </p>
      
      <DataTable 
        columns={columns} 
        data={issues} 
      />
    </div>
  );
};

export default Issues;
