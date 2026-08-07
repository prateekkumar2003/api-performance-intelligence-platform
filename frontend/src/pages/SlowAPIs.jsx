import { useEffect, useState } from 'react';
import DataTable from '../components/DataTable';
import { getSlowAPIs } from '../api';
import AlertBadge from '../components/AlertBadge';

const SlowAPIs = () => {
  const [slowApis, setSlowApis] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await getSlowAPIs();
        setSlowApis(res.data);
      } catch (error) {
        console.error('Error fetching slow APIs:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const columns = [
    { header: 'Path', accessor: 'path' },
    { 
      header: 'Method', 
      accessor: 'method',
      render: (row) => <AlertBadge type="info" text={row.method} />
    },
    { 
      header: 'Response Time', 
      accessor: 'response_time_ms',
      render: (row) => (
        <span style={{ color: 'var(--accent-pink)', fontWeight: 600 }}>
          {row.response_time_ms} ms
        </span>
      )
    },
    { 
      header: 'Status Code', 
      accessor: 'status_code',
      render: (row) => (
        <span style={{ color: row.status_code >= 400 ? 'var(--accent-pink)' : 'var(--accent-success)' }}>
          {row.status_code}
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
      <h1>Slow APIs</h1>
      <p style={{ marginBottom: '24px' }}>
        List of APIs taking longer than 1000ms to respond.
      </p>
      
      <DataTable 
        columns={columns} 
        data={slowApis} 
      />
    </div>
  );
};

export default SlowAPIs;
