import React from 'react';
import { useNavigate } from 'react-router-dom';
import ProcessoStatusBadge from './ProcessoStatusBadge';
import ProcessoCriticidadeBadge from './ProcessoCriticidadeBadge';
import Button from '../common/Button';
import { formatDate } from '../../utils/formatters';

const ProcessoTable = ({ processos, onDelete }) => {
  const navigate = useNavigate();

  return (
    <div className="table-container">
      <table>
        <thead>
          <tr>
            <th>Nome</th>
            <th>Área</th>
            <th>Responsável</th>
            <th>Periodicidade</th>
            <th>Criticidade</th>
            <th>Status</th>
            <th>Atualizado em</th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          {processos.map(p => (
            <tr key={p.id}>
              <td style={{ fontWeight: '500' }}>{p.nome}</td>
              <td>{p.area}</td>
              <td>{p.responsavel || '-'}</td>
              <td>{p.periodicidade || '-'}</td>
              <td><ProcessoCriticidadeBadge criticidade={p.criticidade} /></td>
              <td><ProcessoStatusBadge status={p.status} /></td>
              <td>{formatDate(p.atualizado_em || p.criado_em)}</td>
              <td>
                <div style={{ display: 'flex', gap: '8px' }}>
                  <Button variant="secondary" onClick={() => navigate(`/processos/${p.id}`)}>Ver</Button>
                  <Button variant="secondary" onClick={() => navigate(`/processos/${p.id}/editar`)}>Editar</Button>
                  <Button variant="danger" onClick={() => onDelete(p.id)}>Excluir</Button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ProcessoTable;
