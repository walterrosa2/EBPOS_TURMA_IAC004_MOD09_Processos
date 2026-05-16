import React from 'react';
import Card from '../common/Card';
import { safeList, getSeveridadeVariant } from '../../utils/analysisFormatters';

const RiscosList = ({ riscos }) => {
  const lista = safeList(riscos);
  if (lista.length === 0) return null;

  return (
    <Card>
      <h3 style={{ fontSize: '1.25rem', marginBottom: '16px' }}>Riscos Identificados</h3>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        {lista.map((item, i) => (
          <div key={i} style={{ padding: '16px', border: '1px solid var(--color-border)', borderRadius: '8px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
              <h4 style={{ fontWeight: '600' }}>{item.titulo || item}</h4>
              {item.severidade && (
                <span className={`badge badge-${getSeveridadeVariant(item.severidade)}`}>Severidade: {item.severidade}</span>
              )}
            </div>
            {item.descricao && <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginBottom: '8px' }}>{item.descricao}</p>}
            {item.tipo && <p style={{ fontSize: '0.85rem' }}>Tipo: <strong>{item.tipo}</strong></p>}
            {item.mitigacao && <p style={{ fontSize: '0.85rem', color: 'var(--color-success)', marginTop: '8px' }}>Mitigação: {item.mitigacao}</p>}
          </div>
        ))}
      </div>
    </Card>
  );
};
export default RiscosList;
