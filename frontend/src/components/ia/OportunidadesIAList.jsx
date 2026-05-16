import React from 'react';
import Card from '../common/Card';
import { safeList } from '../../utils/analysisFormatters';

const OportunidadesIAList = ({ oportunidades }) => {
  const lista = safeList(oportunidades);
  if (lista.length === 0) return null;

  return (
    <Card>
      <h3 style={{ fontSize: '1.25rem', marginBottom: '16px', color: '#6366f1' }}>✨ Oportunidades de Inteligência Artificial</h3>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        {lista.map((item, i) => (
          <div key={i} style={{ padding: '16px', border: '1px solid #c7d2fe', backgroundColor: '#f5f7ff', borderRadius: '8px' }}>
            <h4 style={{ fontWeight: '600', marginBottom: '8px' }}>{item.titulo || item}</h4>
            {item.descricao && <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>{item.descricao}</p>}
            {item.beneficio_esperado && <p style={{ fontSize: '0.85rem', color: '#4338ca', marginTop: '8px' }}>Benefício: {item.beneficio_esperado}</p>}
          </div>
        ))}
      </div>
    </Card>
  );
};
export default OportunidadesIAList;
