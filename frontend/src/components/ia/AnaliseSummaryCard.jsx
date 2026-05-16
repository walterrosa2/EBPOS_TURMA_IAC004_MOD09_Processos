import React from 'react';
import Card from '../common/Card';

const AnaliseSummaryCard = ({ resumoExecutivo, diagnosticoOperacional }) => {
  return (
    <Card>
      <h3 style={{ fontSize: '1.25rem', marginBottom: '16px', color: 'var(--text-primary)' }}>Resumo Executivo</h3>
      <p style={{ marginBottom: '24px', lineHeight: '1.6', color: 'var(--text-secondary)' }}>{resumoExecutivo}</p>
      
      <h3 style={{ fontSize: '1.25rem', marginBottom: '16px', color: 'var(--text-primary)' }}>Diagnóstico Operacional</h3>
      <p style={{ lineHeight: '1.6', color: 'var(--text-secondary)' }}>{diagnosticoOperacional}</p>
    </Card>
  );
};

export default AnaliseSummaryCard;
