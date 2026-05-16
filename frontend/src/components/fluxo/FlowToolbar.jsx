import React from 'react';
import { useNavigate } from 'react-router-dom';
import Button from '../common/Button';

const FlowToolbar = ({ processoId, onAddEtapa, onSave, onReload, saving }) => {
  const navigate = useNavigate();

  return (
    <div style={{
      position: 'absolute',
      top: 16,
      left: 16,
      right: 16,
      display: 'flex',
      justifyContent: 'space-between',
      zIndex: 10
    }}>
      <div style={{ display: 'flex', gap: '12px' }}>
        <Button variant="secondary" onClick={() => navigate(`/processos/${processoId}`)}>
          &larr; Voltar para detalhe
        </Button>
        <Button onClick={onAddEtapa}>+ Nova etapa</Button>
      </div>
      <div style={{ display: 'flex', gap: '12px' }}>
        <Button variant="secondary" onClick={onReload} disabled={saving}>Recarregar</Button>
        <Button onClick={onSave} loading={saving}>Salvar fluxo</Button>
      </div>
    </div>
  );
};

export default FlowToolbar;
