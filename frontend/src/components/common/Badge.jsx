import React from 'react';

const Badge = ({ children, variant = 'default' }) => {
  const styles = {
    default: { bg: '#f3f4f6', color: '#374151' },
    primary: { bg: '#dbeafe', color: '#1e40af' },
    success: { bg: '#d1fae5', color: '#065f46' },
    warning: { bg: '#fef3c7', color: '#92400e' },
    danger: { bg: '#fee2e2', color: '#991b1b' },
  };

  const currentStyle = styles[variant] || styles.default;

  return (
    <span style={{
      display: 'inline-flex',
      alignItems: 'center',
      padding: '2px 8px',
      borderRadius: '9999px',
      fontSize: '0.75rem',
      fontWeight: '500',
      backgroundColor: currentStyle.bg,
      color: currentStyle.color,
      whiteSpace: 'nowrap'
    }}>
      {children}
    </span>
  );
};

export default Badge;
