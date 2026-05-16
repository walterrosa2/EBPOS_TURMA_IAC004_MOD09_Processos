import React from 'react';
import EmptyState from '../common/EmptyState';

const FlowEmptyState = ({ onAddEtapa }) => {
  return (
    <div style={{ 
      position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', 
      background: 'rgba(255, 255, 255, 0.9)', padding: '24px', borderRadius: '12px', zIndex: 10,
      boxShadow: 'var(--shadow-md)'
    }}>
      <EmptyState 
        message="Nenhuma etapa foi criada para este fluxo ainda." 
        actionText="Criar primeira etapa" 
        onAction={onAddEtapa}
      />
    </div>
  );
};

export default FlowEmptyState;
