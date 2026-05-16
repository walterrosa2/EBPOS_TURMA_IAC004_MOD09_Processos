import os

path = "g:/Meu Drive/Backup_HD_Walter/PROJETO_EBPOS_IAC004_MOD09/frontend/src/components/automacoes/"
os.makedirs(path, exist_ok=True)

files = {
"PrioridadeBadge.jsx": """import React from 'react';
import { getPrioridadeVariant } from '../../utils/analysisFormatters';

const PrioridadeBadge = ({ prioridade }) => {
  if (!prioridade) return null;
  return <span className={`badge badge-${getPrioridadeVariant(prioridade)}`}>{prioridade}</span>;
};
export default PrioridadeBadge;
""",

"TipoAutomacaoBadge.jsx": """import React from 'react';

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
""",

"AutomacaoStatusSelect.jsx": """import React, { useState } from 'react';

const AutomacaoStatusSelect = ({ id, currentStatus, onStatusChange }) => {
  const [loading, setLoading] = useState(false);
  
  const handleChange = async (e) => {
    const newStatus = e.target.value;
    setLoading(true);
    await onStatusChange(id, newStatus);
    setLoading(false);
  };

  const statuses = [
    'Sugerida', 'Em avaliação', 'Priorizada', 
    'Em implementação', 'Concluída', 'Descartada'
  ];

  return (
    <select 
      value={currentStatus} 
      onChange={handleChange}
      disabled={loading}
      style={{ padding: '6px', borderRadius: '4px', border: '1px solid var(--color-border)' }}
    >
      {statuses.map(s => (
        <option key={s} value={s}>{s}</option>
      ))}
    </select>
  );
};
export default AutomacaoStatusSelect;
""",

"AutomacaoFilters.jsx": """import React from 'react';

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
""",

"AutomacaoTable.jsx": """import React from 'react';
import AutomacaoStatusSelect from './AutomacaoStatusSelect';
import PrioridadeBadge from './PrioridadeBadge';
import TipoAutomacaoBadge from './TipoAutomacaoBadge';
import { formatDateTime } from '../../utils/analysisFormatters';

const AutomacaoTable = ({ diretrizes, onStatusChange }) => {
  if (!diretrizes || diretrizes.length === 0) return <p>Nenhuma diretriz encontrada com estes filtros.</p>;

  return (
    <div style={{ overflowX: 'auto' }}>
      <table className="data-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Título</th>
            <th>Tipo</th>
            <th>Prioridade</th>
            <th>Impacto</th>
            <th>Status</th>
            <th>Criado em</th>
          </tr>
        </thead>
        <tbody>
          {diretrizes.map(d => (
            <tr key={d.id}>
              <td>#{d.id}</td>
              <td style={{ maxWidth: '300px' }}>
                <div style={{ fontWeight: '600' }}>{d.titulo}</div>
                <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>{d.descricao}</div>
              </td>
              <td><TipoAutomacaoBadge tipo={d.tipo} /></td>
              <td><PrioridadeBadge prioridade={d.prioridade} /></td>
              <td>{d.impacto || '-'}</td>
              <td><AutomacaoStatusSelect id={d.id} currentStatus={d.status} onStatusChange={onStatusChange} /></td>
              <td>{formatDateTime(d.criado_em)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
export default AutomacaoTable;
""",

"AutomacaoBoard.jsx": """import React from 'react';
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
"""
}

for k, v in files.items():
    with open(path+k, "w", encoding="utf-8") as f:
        f.write(v)
