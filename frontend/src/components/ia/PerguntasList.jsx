import React from 'react';
import Card from '../common/Card';
import { safeList } from '../../utils/analysisFormatters';

const PerguntasList = ({ perguntas }) => {
  const lista = safeList(perguntas);
  if (lista.length === 0) return null;

  return (
    <Card>
      <h3 style={{ fontSize: '1.25rem', marginBottom: '16px' }}>Perguntas para Aprofundamento</h3>
      <ul style={{ paddingLeft: '20px', display: 'flex', flexDirection: 'column', gap: '12px', color: 'var(--text-primary)' }}>
        {lista.map((item, i) => (
          <li key={i}>{item}</li>
        ))}
      </ul>
    </Card>
  );
};
export default PerguntasList;
