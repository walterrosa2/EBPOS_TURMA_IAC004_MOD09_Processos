import React from 'react';
import Card from '../common/Card';

const MetricCard = ({ title, value, description, color = 'var(--color-primary)' }) => {
  return (
    <Card style={{ borderTop: `4px solid ${color}` }}>
      <h3 style={{ fontSize: '0.875rem', color: 'var(--color-muted)', marginBottom: '8px', fontWeight: '500' }}>{title}</h3>
      <div style={{ fontSize: '2.5rem', fontWeight: '700', color: 'var(--color-text)', marginBottom: '4px' }}>{value}</div>
      {description && <p style={{ fontSize: '0.75rem', color: 'var(--color-muted)' }}>{description}</p>}
    </Card>
  );
};

export default MetricCard;
