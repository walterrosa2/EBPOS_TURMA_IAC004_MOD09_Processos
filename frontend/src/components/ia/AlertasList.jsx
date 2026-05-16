import React from 'react';
import { safeList } from '../../utils/analysisFormatters';

const AlertasList = ({ alertas }) => {
  const lista = safeList(alertas);
  if (lista.length === 0) return null;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', marginBottom: '24px' }}>
      {lista.map((item, i) => (
        <div key={i} style={{ padding: '16px', backgroundColor: '#fef2f2', borderLeft: '4px solid #ef4444', borderRadius: '4px', color: '#991b1b' }}>
          <strong>Aviso Importante:</strong> {item}
        </div>
      ))}
    </div>
  );
};
export default AlertasList;
