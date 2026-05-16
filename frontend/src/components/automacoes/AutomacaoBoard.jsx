import React from 'react';
import AutomacaoTable from './AutomacaoTable';
import AutomacaoFilters from './AutomacaoFilters';
import Card from '../common/Card';

const AutomacaoBoard = ({ diretrizes, onStatusChange, filters, setFilters }) => {
  // Aplicar filtros
  const filtered = diretrizes.filter(d => {
    if (filters.prioridade && d.prioridade !== filters.prioridade) return false;
    if (filters.status && d.status !== filters.status) return false;
    if (filters.text) {
      const matchText = filters.text.toLowerCase();
      if (!d.titulo.toLowerCase().includes(matchText) && 
          !(d.descricao && d.descricao.toLowerCase().includes(matchText))) {
        return false;
      }
    }
    return true;
  });

  return (
    <Card>
      <AutomacaoFilters filters={filters} setFilters={setFilters} />
      <AutomacaoTable diretrizes={filtered} onStatusChange={onStatusChange} />
    </Card>
  );
};
export default AutomacaoBoard;
