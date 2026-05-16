import React from 'react';
import { Handle, Position } from 'reactflow';
import Badge from '../common/Badge';

const EtapaNode = ({ data }) => {
  const { etapa } = data;

  return (
    <div style={{
      background: 'white',
      border: '1px solid var(--color-border)',
      borderRadius: '8px',
      padding: '12px',
      minWidth: '200px',
      boxShadow: 'var(--shadow-sm)',
    }}>
      <Handle type="target" position={Position.Top} style={{ background: '#555' }} />
      
      <div style={{ fontWeight: '600', fontSize: '0.875rem', marginBottom: '8px' }}>
        {etapa.nome}
      </div>
      
      {(etapa.tipo_etapa || etapa.responsavel) && (
        <div style={{ fontSize: '0.75rem', color: 'var(--color-muted)', marginBottom: '8px' }}>
          {etapa.tipo_etapa && <div>Tipo: {etapa.tipo_etapa}</div>}
          {etapa.responsavel && <div>Resp: {etapa.responsavel}</div>}
        </div>
      )}

      <div style={{ display: 'flex', gap: '4px', flexWrap: 'wrap' }}>
        {etapa.gargalo && <Badge variant="warning">Gargalo</Badge>}
        {etapa.risco && <Badge variant="danger">Risco</Badge>}
      </div>

      <Handle type="source" position={Position.Bottom} style={{ background: '#555' }} />
    </div>
  );
};

export default EtapaNode;
