import React from 'react';
import Card from '../common/Card';
import { safeList, getImpactoVariant } from '../../utils/analysisFormatters';

const MelhoriasList = ({ melhorias }) => {
  const lista = safeList(melhorias);
  if (lista.length === 0) return null;

  return (
    <Card>
      <h3 style={{ fontSize: '1.25rem', marginBottom: '16px' }}>Sugestões de Melhoria</h3>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        {lista.map((item, i) => (
          <div key={i} style={{ padding: '16px', border: '1px solid var(--color-border)', borderRadius: '8px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
              <h4 style={{ fontWeight: '600' }}>{item.titulo || item}</h4>
              {item.impacto && (
                <span className={`badge badge-${getImpactoVariant(item.impacto)}`}>Impacto: {item.impacto}</span>
              )}
            </div>
            {item.descricao && <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>{item.descricao}</p>}
          </div>
        ))}
      </div>
    </Card>
  );
};
export default MelhoriasList;
