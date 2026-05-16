import React from 'react';
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
