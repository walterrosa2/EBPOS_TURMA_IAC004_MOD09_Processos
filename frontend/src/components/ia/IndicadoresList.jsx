import React from 'react';
import Card from '../common/Card';
import { safeList } from '../../utils/analysisFormatters';

const IndicadoresList = ({ indicadores }) => {
  const lista = safeList(indicadores);
  if (lista.length === 0) return null;

  return (
    <Card>
      <h3 style={{ fontSize: '1.25rem', marginBottom: '16px' }}>Indicadores Recomendados (KPIs)</h3>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(250px, 1fr))', gap: '16px' }}>
        {lista.map((item, i) => (
          <div key={i} style={{ padding: '12px', border: '1px solid var(--color-border)', borderRadius: '8px', backgroundColor: 'var(--bg-secondary)' }}>
            <h4 style={{ fontWeight: '600', fontSize: '0.95rem', marginBottom: '4px' }}>{item.nome || item}</h4>
            {item.descricao && <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>{item.descricao}</p>}
            {item.formula && <code style={{ display: 'block', marginTop: '8px', fontSize: '0.75rem', padding: '4px', backgroundColor: '#e2e8f0', borderRadius: '4px' }}>{item.formula}</code>}
          </div>
        ))}
      </div>
    </Card>
  );
};
export default IndicadoresList;
