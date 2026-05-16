import React from 'react';

const LoadingState = ({ message = 'Carregando...' }) => {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '48px 24px', color: 'var(--color-muted)' }}>
      <div style={{
        border: '3px solid #f3f3f3',
        borderTop: '3px solid var(--color-primary)',
        borderRadius: '50%',
        width: '24px',
        height: '24px',
        animation: 'spin 1s linear infinite',
        marginBottom: '16px'
      }} />
      <style>{`
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
      `}</style>
      <p style={{ fontSize: '0.875rem' }}>{message}</p>
    </div>
  );
};

export default LoadingState;
