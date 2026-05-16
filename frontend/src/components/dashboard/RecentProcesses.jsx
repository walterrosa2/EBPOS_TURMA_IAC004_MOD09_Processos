import React from 'react';
import { useNavigate } from 'react-router-dom';
import Card from '../common/Card';
import Badge from '../common/Badge';
import { formatDate } from '../../utils/formatters';

const RecentProcesses = ({ processos = [] }) => {
  const navigate = useNavigate();

  if (!processos || processos.length === 0) {
    return (
      <Card>
        <h3 style={{ fontSize: '1rem', marginBottom: '16px' }}>Processos Recentes</h3>
        <p style={{ color: 'var(--color-muted)', fontSize: '0.875rem' }}>Nenhum processo encontrado.</p>
      </Card>
    );
  }

  return (
    <Card>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
        <h3 style={{ fontSize: '1rem', margin: 0 }}>Processos Recentes</h3>
        <button 
          onClick={() => navigate('/processos')}
          style={{ background: 'none', border: 'none', color: 'var(--color-primary)', cursor: 'pointer', fontSize: '0.875rem' }}
        >
          Ver todos
        </button>
      </div>
      
      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th>Nome</th>
              <th>Área</th>
              <th>Status</th>
              <th>Atualizado em</th>
            </tr>
          </thead>
          <tbody>
            {processos.slice(0, 5).map(p => (
              <tr key={p.id} onClick={() => navigate(`/processos/${p.id}`)} style={{ cursor: 'pointer' }}>
                <td style={{ fontWeight: '500' }}>{p.nome}</td>
                <td>{p.area}</td>
                <td>
                  <Badge variant={p.status === 'Analisado' ? 'success' : p.status === 'Rascunho' ? 'default' : 'primary'}>
                    {p.status}
                  </Badge>
                </td>
                <td>{formatDate(p.atualizado_em || p.criado_em)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Card>
  );
};

export default RecentProcesses;
