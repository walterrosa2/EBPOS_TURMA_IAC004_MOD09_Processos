import React from 'react';

const EmptyState = ({ message = 'Nenhum dado encontrado.', actionText, onAction }) => {
  return (
    <div style={{ textAlign: 'center', padding: '48px 24px', color: 'var(--color-muted)' }}>
      <div style={{ fontSize: '3rem', marginBottom: '16px' }}>📄</div>
      <p style={{ marginBottom: actionText ? '16px' : '0' }}>{message}</p>
      {actionText && onAction && (
        <button
          onClick={onAction}
          style={{
            padding: '8px 16px',
            backgroundColor: 'var(--color-primary)',
            color: 'white',
            border: 'none',
            borderRadius: '8px',
            cursor: 'pointer'
          }}
        >
          {actionText}
        </button>
      )}
    </div>
  );
};

export default EmptyState;
