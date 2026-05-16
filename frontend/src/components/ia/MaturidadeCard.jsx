import React from 'react';
import Card from '../common/Card';

const MaturidadeCard = ({ maturidade }) => {
  if (!maturidade) return null;

  return (
    <Card>
      <h3 style={{ fontSize: '1.25rem', marginBottom: '16px', color: 'var(--text-primary)' }}>Nível de Maturidade</h3>
      <div style={{ display: 'flex', alignItems: 'center', gap: '16px', marginBottom: '16px' }}>
        <div style={{ 
          backgroundColor: 'var(--color-primary, #4f46e5)', 
          color: 'white', 
          padding: '8px 16px', 
          borderRadius: '8px',
          fontWeight: 'bold',
          fontSize: '1.1rem'
        }}>
          {maturidade.nivel || maturidade}
        </div>
      </div>
      {maturidade.justificativa && (
        <p style={{ color: 'var(--text-secondary)', lineHeight: '1.5' }}>
          {maturidade.justificativa}
        </p>
      )}
    </Card>
  );
};

export default MaturidadeCard;
