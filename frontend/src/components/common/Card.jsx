import React from 'react';

const Card = ({ children, className = '', style = {} }) => {
  return (
    <div
      className={className}
      style={{
        backgroundColor: 'var(--color-surface)',
        borderRadius: 'var(--radius-md)',
        boxShadow: 'var(--shadow-sm)',
        padding: '24px',
        border: '1px solid var(--color-border)',
        ...style
      }}
    >
      {children}
    </div>
  );
};

export default Card;
