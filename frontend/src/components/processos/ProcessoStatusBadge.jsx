import React from 'react';
import Badge from '../common/Badge';

const ProcessoStatusBadge = ({ status }) => {
  let variant = 'default';
  
  switch (status) {
    case 'Rascunho': variant = 'default'; break;
    case 'Mapeado': variant = 'primary'; break;
    case 'Em análise': variant = 'warning'; break;
    case 'Analisado': variant = 'success'; break;
    case 'Em melhoria': variant = 'danger'; break;
    default: variant = 'default';
  }

  return <Badge variant={variant}>{status}</Badge>;
};

export default ProcessoStatusBadge;
