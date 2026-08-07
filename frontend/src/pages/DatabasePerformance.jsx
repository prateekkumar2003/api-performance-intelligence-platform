import { useEffect, useState } from 'react';
import DataTable from '../components/DataTable';
import { getSlowQueries } from '../api';

const DatabasePerformance = () => {
  const [queries, setQueries] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await getSlowQueries();
        setQueries(res.data);
      } catch (error) {
        console.error('Error fetching slow queries:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const columns = [
    { 
      header: 'Query', 
      accessor: 'query',
      render: (row) => (
        <code style={{ 
          background: 'rgba(255,255,255,0.05)', 
          padding: '4px 8px', 
          borderRadius: '4px',
          color: 'var(--accent-cyan)'
        }}>
          {row.query}
        </code>
      )
    },
    { 
      header: 'Execution Time', 
      accessor: 'execution_time_ms',
      render: (row) => (
        <span style={{ color: 'var(--accent-warning)', fontWeight: 600 }}>
          {row.execution_time_ms} ms
        </span>
      )
    },
    { 
      header: 'Detected At', 
      accessor: 'created_at',
      render: (row) => new Date(row.created_at).toLocaleString()
    },
  ];

  if (loading) return <div>Loading...</div>;

  return (
    <div className="animate-fade-in">
      <h1>Slow Queries</h1>
      <p style={{ marginBottom: '24px' }}>
        List of database queries experiencing performance degradation.
      </p>
      
      <DataTable 
        columns={columns} 
        data={queries} 
      />
    </div>
  );
};

export default DatabasePerformance;
