import React from 'react';

const TipoAutomacaoBadge = ({ tipo }) => {
  if (!tipo) return null;
  const map = {
    'ia': 'primary',
    'rpa': 'secondary',
    'integracao': 'success',
    'script': 'warning',
    'macro': 'default'
  };
  return <span className={`badge badge-${map[tipo.toLowerCase()] || 'default'}`}>{tipo}</span>;
};
export default TipoAutomacaoBadge;
