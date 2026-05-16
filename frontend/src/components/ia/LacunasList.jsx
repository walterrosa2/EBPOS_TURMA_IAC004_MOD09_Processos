import React from 'react';
import Card from '../common/Card';
import { safeList } from '../../utils/analysisFormatters';

const LacunasList = ({ lacunas }) => {
  const lista = safeList(lacunas);
  if (lista.length === 0) return null;

  return (
    <Card>
      <h3 style={{ fontSize: '1.25rem', marginBottom: '16px' }}>Lacunas no Mapeamento</h3>
      <ul style={{ paddingLeft: '20px', display: 'flex', flexDirection: 'column', gap: '8px', color: 'var(--text-secondary)' }}>
        {lista.map((item, i) => (
          <li key={i}>{typeof item === 'string' ? item : item.descricao || item.titulo}</li>
        ))}
      </ul>
    </Card>
  );
};
export default LacunasList;
