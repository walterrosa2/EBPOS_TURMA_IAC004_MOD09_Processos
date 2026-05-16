import React from 'react';
import Button from '../common/Button';
import { formatDateTime } from '../../utils/analysisFormatters';

const AnaliseHeader = ({ processoNome, createdAt, onBack, onGoToAutomacoes }) => {
  return (
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '24px' }}>
      <div>
        <div style={{ display: 'flex', gap: '12px', alignItems: 'center', marginBottom: '8px' }}>
          <Button variant="secondary" onClick={onBack}>&larr; Voltar</Button>
          <h2 style={{ fontSize: '1.5rem', margin: 0 }}>Análise IA: {processoNome}</h2>
        </div>
        <p style={{ color: 'var(--text-secondary)', marginLeft: '80px' }}>
          Gerada em {formatDateTime(createdAt)}
        </p>
      </div>
      <div>
        <Button variant="primary" onClick={onGoToAutomacoes}>Ver Diretrizes de Automação</Button>
      </div>
    </div>
  );
};

export default AnaliseHeader;
