const MetricCard = ({ title, value }) => {
  return (
    <div className="glass-panel metric-card animate-fade-in">
      <div className="title">{title}</div>
      <div className="value">{value}</div>
    </div>
  );
};

export default MetricCard;
