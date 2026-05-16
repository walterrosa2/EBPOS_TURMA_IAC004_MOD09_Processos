import React from 'react';

const Button = ({ children, onClick, type = 'button', variant = 'primary', disabled = false, loading = false, className = '', ...props }) => {
  const baseStyle = {
    padding: '8px 16px',
    borderRadius: '8px',
    fontWeight: '500',
    fontSize: '0.875rem',
    cursor: disabled || loading ? 'not-allowed' : 'pointer',
    border: 'none',
    display: 'inline-flex',
    alignItems: 'center',
    justifyContent: 'center',
    transition: 'background-color 0.2s',
    opacity: disabled ? 0.6 : 1,
  };

  const variants = {
    primary: {
      backgroundColor: 'var(--color-primary)',
      color: 'white',
    },
    secondary: {
      backgroundColor: 'var(--color-surface)',
      color: 'var(--color-text)',
      border: '1px solid var(--color-border)',
    },
    danger: {
      backgroundColor: 'var(--color-danger)',
      color: 'white',
    }
  };

  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled || loading}
      style={{ ...baseStyle, ...variants[variant] }}
      className={className}
      {...props}
    >
      {loading ? 'Carregando...' : children}
    </button>
  );
};

export default Button;
