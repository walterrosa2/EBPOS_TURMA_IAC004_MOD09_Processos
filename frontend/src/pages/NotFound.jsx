import React from 'react';
import { useNavigate } from 'react-router-dom';
import EmptyState from '../components/common/EmptyState';

const NotFound = () => {
  const navigate = useNavigate();

  return (
    <div style={{ display: 'flex', height: '100%', alignItems: 'center', justifyContent: 'center' }}>
      <EmptyState 
        message="Ops! A página que você está procurando não existe."
        actionText="Voltar para o Dashboard"
        onAction={() => navigate('/')}
      />
    </div>
  );
};

export default NotFound;
