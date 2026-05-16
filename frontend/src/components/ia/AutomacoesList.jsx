import React from 'react';
import Card from '../common/Card';
import { safeList, getPrioridadeVariant, getImpactoVariant } from '../../utils/analysisFormatters';

const AutomacoesList = ({ automacoes }) => {
  const lista = safeList(automacoes);
  if (lista.length === 0) return null;

  return (
    <Card>
      <h3 style={{ fontSize: '1.25rem', marginBottom: '16px' }}>Sugestões de Automação</h3>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        {lista.map((item, i) => (
          <div key={i} style={{ padding: '16px', border: '1px solid var(--color-border)', borderRadius: '8px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
              <h4 style={{ fontWeight: '600', color: 'var(--color-primary)' }}>{item.titulo || item}</h4>
              <div style={{ display: 'flex', gap: '8px' }}>
                {item.prioridade && <span className={`badge badge-${getPrioridadeVariant(item.prioridade)}`}>{item.prioridade}</span>}
                {item.impacto && <span className={`badge badge-${getImpactoVariant(item.impacto)}`}>Impacto {item.impacto}</span>}
              </div>
            </div>
            {item.descricao && <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginBottom: '8px' }}>{item.descricao}</p>}
            {item.esforco && <p style={{ fontSize: '0.85rem' }}>Esforço: <strong>{item.esforco}</strong></p>}
            {item.pre_requisitos && item.pre_requisitos.length > 0 && (
              <div style={{ marginTop: '8px', fontSize: '0.85rem', padding: '8px', backgroundColor: 'var(--bg-secondary)', borderRadius: '4px' }}>
                <strong>Pré-requisitos:</strong> {item.pre_requisitos.join(', ')}
              </div>
            )}
          </div>
        ))}
      </div>
    </Card>
  );
};
export default AutomacoesList;
