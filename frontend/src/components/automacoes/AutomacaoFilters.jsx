import React from 'react';

const AutomacaoFilters = ({ filters, setFilters }) => {
  return (
    <div style={{ display: 'flex', gap: '16px', marginBottom: '24px', flexWrap: 'wrap' }}>
      <input 
        type="text" 
        placeholder="Buscar..." 
        value={filters.text} 
        onChange={e => setFilters(f => ({ ...f, text: e.target.value }))}
        style={{ padding: '8px', border: '1px solid var(--color-border)', borderRadius: '4px' }}
      />
      <select 
        value={filters.prioridade} 
        onChange={e => setFilters(f => ({ ...f, prioridade: e.target.value }))}
        style={{ padding: '8px', border: '1px solid var(--color-border)', borderRadius: '4px' }}
      >
        <option value="">Todas Prioridades</option>
        <option value="Urgente">Urgente</option>
        <option value="Alta">Alta</option>
        <option value="Média">Média</option>
        <option value="Baixa">Baixa</option>
      </select>
      <select 
        value={filters.status} 
        onChange={e => setFilters(f => ({ ...f, status: e.target.value }))}
        style={{ padding: '8px', border: '1px solid var(--color-border)', borderRadius: '4px' }}
      >
        <option value="">Todos Status</option>
        <option value="Sugerida">Sugerida</option>
        <option value="Em avaliação">Em avaliação</option>
        <option value="Priorizada">Priorizada</option>
        <option value="Em implementação">Em implementação</option>
        <option value="Concluída">Concluída</option>
        <option value="Descartada">Descartada</option>
      </select>
    </div>
  );
};
export default AutomacaoFilters;
