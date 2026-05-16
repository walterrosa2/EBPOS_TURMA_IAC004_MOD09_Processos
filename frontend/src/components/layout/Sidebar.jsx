import React from 'react';
import { NavLink } from 'react-router-dom';

const Sidebar = () => {
  const linkStyle = ({ isActive }) => ({
    display: 'block',
    padding: '12px 16px',
    borderRadius: '8px',
    marginBottom: '8px',
    color: isActive ? 'var(--color-primary)' : 'var(--color-text)',
    backgroundColor: isActive ? '#eff6ff' : 'transparent',
    fontWeight: isActive ? '500' : '400',
    transition: 'background-color 0.2s, color 0.2s',
  });

  const disabledLinkStyle = {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '12px 16px',
    borderRadius: '8px',
    marginBottom: '8px',
    color: 'var(--color-muted)',
    cursor: 'not-allowed',
    opacity: 0.7
  };

  return (
    <aside style={{
      width: 'var(--sidebar-width)',
      height: '100vh',
      position: 'fixed',
      left: 0,
      top: 0,
      backgroundColor: 'var(--color-surface)',
      borderRight: '1px solid var(--color-border)',
      display: 'flex',
      flexDirection: 'column'
    }}>
      <div style={{ padding: '24px 20px', borderBottom: '1px solid var(--color-border)' }}>
        <h2 style={{ fontSize: '1.25rem', color: 'var(--color-primary)' }}>QDT Processos</h2>
        <p style={{ fontSize: '0.75rem', color: 'var(--color-muted)', marginTop: '4px' }}>Gestão Contábil</p>
      </div>

      <nav style={{ flex: 1, padding: '20px 16px', overflowY: 'auto' }}>
        <NavLink to="/" style={linkStyle} end>Dashboard</NavLink>
        <NavLink to="/processos" style={linkStyle}>Processos</NavLink>
        
        <div style={disabledLinkStyle}>
          Fluxos
          <span style={{ fontSize: '0.65rem', backgroundColor: '#f1f5f9', padding: '2px 6px', borderRadius: '4px' }}>Em breve</span>
        </div>
        <div style={disabledLinkStyle}>
          IA Insights
          <span style={{ fontSize: '0.65rem', backgroundColor: '#f1f5f9', padding: '2px 6px', borderRadius: '4px' }}>Em breve</span>
        </div>
        <div style={disabledLinkStyle}>
          Automações
          <span style={{ fontSize: '0.65rem', backgroundColor: '#f1f5f9', padding: '2px 6px', borderRadius: '4px' }}>Em breve</span>
        </div>
      </nav>

      <div style={{ padding: '20px 16px', borderTop: '1px solid var(--color-border)' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div style={{ width: '32px', height: '32px', borderRadius: '50%', backgroundColor: 'var(--color-primary)', color: 'white', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 'bold' }}>U</div>
          <div>
            <p style={{ fontSize: '0.875rem', fontWeight: '500' }}>Usuário</p>
            <p style={{ fontSize: '0.75rem', color: 'var(--color-muted)' }}>SaaS MVP</p>
          </div>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;
