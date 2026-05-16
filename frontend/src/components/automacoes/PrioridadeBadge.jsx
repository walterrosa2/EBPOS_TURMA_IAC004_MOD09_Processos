import React from 'react';
import { getPrioridadeVariant } from '../../utils/analysisFormatters';

const PrioridadeBadge = ({ prioridade }) => {
  if (!prioridade) return null;
  return <span className={`badge badge-${getPrioridadeVariant(prioridade)}`}>{prioridade}</span>;
};
export default PrioridadeBadge;
