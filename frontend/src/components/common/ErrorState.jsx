import React from 'react';

const ErrorState = ({ message = 'Ocorreu um erro ao carregar os dados.', onRetry }) => {
  return (
    <div style={{ padding: '24px', backgroundColor: '#fef2f2', border: '1px solid #fca5a5', borderRadius: '8px', color: '#991b1b', margin: '16px 0' }}>
      <h3 style={{ marginBottom: '8px', fontSize: '1rem' }}>Erro</h3>
      <p style={{ marginBottom: onRetry ? '16px' : '0', fontSize: '0.875rem' }}>{message}</p>
      {onRetry && (
        <button
          onClick={onRetry}
          style={{ padding: '6px 12px', backgroundColor: '#dc2626', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', fontSize: '0.875rem' }}
        >
          Tentar Novamente
        </button>
      )}
    </div>
  );
};

export default ErrorState;
