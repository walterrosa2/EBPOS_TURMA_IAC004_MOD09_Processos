import React from 'react';
import { useLocation } from 'react-router-dom';

const Header = () => {
  const location = useLocation();
  
  let title = 'Dashboard';
  let subtitle = 'Visão geral da operação';

  if (location.pathname.startsWith('/processos')) {
    title = 'Processos';
    subtitle = 'Catálogo de processos contábeis';
    
    if (location.pathname === '/processos/novo') {
      title = 'Novo Processo';
      subtitle = 'Cadastrar um novo fluxo mapeado';
    } else if (location.pathname.endsWith('/editar')) {
      title = 'Editar Processo';
      subtitle = 'Atualizar informações do processo';
    } else if (location.pathname !== '/processos') {
      title = 'Detalhe do Processo';
      subtitle = 'Visualização de metadados';
    }
  }

  return (
    <header style={{
      height: 'var(--header-height)',
      backgroundColor: 'var(--color-surface)',
      borderBottom: '1px solid var(--color-border)',
      display: 'flex',
      alignItems: 'center',
      padding: '0 32px',
      position: 'sticky',
      top: 0,
      zIndex: 10
    }}>
      <div>
        <h1 style={{ fontSize: '1.25rem', fontWeight: '600', margin: 0 }}>{title}</h1>
        {subtitle && <p style={{ fontSize: '0.75rem', color: 'var(--color-muted)', margin: '2px 0 0 0' }}>{subtitle}</p>}
      </div>
    </header>
  );
};

export default Header;
