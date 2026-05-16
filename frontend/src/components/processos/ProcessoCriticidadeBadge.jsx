import React from 'react';
import Badge from '../common/Badge';

const ProcessoCriticidadeBadge = ({ criticidade }) => {
  let variant = 'default';
  
  switch (criticidade) {
    case 'Baixa': variant = 'success'; break;
    case 'Média': variant = 'warning'; break;
    case 'Alta': variant = 'danger'; break;
    default: variant = 'default';
  }

  return <Badge variant={variant}>{criticidade}</Badge>;
};

export default ProcessoCriticidadeBadge;
