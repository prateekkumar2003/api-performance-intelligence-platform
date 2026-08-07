const AlertBadge = ({ type, text }) => {
  const getBadgeClass = (type) => {
    switch(type?.toLowerCase()) {
      case 'critical': return 'critical';
      case 'warning': return 'warning';
      case 'info': return 'info';
      default: return 'info';
    }
  };

  return (
    <span className={`badge ${getBadgeClass(type)}`}>
      {text || type}
    </span>
  );
};

export default AlertBadge;
