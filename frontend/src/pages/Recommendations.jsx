import { useEffect, useState } from 'react';
import DataTable from '../components/DataTable';
import { getRecommendations } from '../api';
import AlertBadge from '../components/AlertBadge';

const Recommendations = () => {
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await getRecommendations();
        setRecommendations(res.data);
      } catch (error) {
        console.error('Error fetching recommendations:', error);
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
      header: 'Title', 
      accessor: 'title',
      render: (row) => <span style={{ fontWeight: 600 }}>{row.title}</span>
    },
    { 
      header: 'Description', 
      accessor: 'description',
      render: (row) => <span style={{ color: 'var(--text-secondary)' }}>{row.description}</span>
    },
    { header: 'Path', accessor: 'path' },
    { 
      header: 'Generated At', 
      accessor: 'created_at',
      render: (row) => new Date(row.created_at).toLocaleString()
    },
  ];

  if (loading) return <div>Loading...</div>;

  return (
    <div className="animate-fade-in">
      <h1>Optimization Recommendations</h1>
      <p style={{ marginBottom: '24px' }}>
        AI-driven suggestions to improve API and query performance.
      </p>
      
      <DataTable 
        columns={columns} 
        data={recommendations} 
      />
    </div>
  );
};

export default Recommendations;
