import React, { useState } from 'react';

const AutomacaoStatusSelect = ({ id, currentStatus, onStatusChange }) => {
  const [loading, setLoading] = useState(false);
  
  const handleChange = async (e) => {
    const newStatus = e.target.value;
    setLoading(true);
    await onStatusChange(id, newStatus);
    setLoading(false);
  };

  const statuses = [
    'Sugerida', 'Em avaliação', 'Priorizada', 
    'Em implementação', 'Concluída', 'Descartada'
  ];

  return (
    <select 
      value={currentStatus} 
      onChange={handleChange}
      disabled={loading}
      style={{ padding: '6px', borderRadius: '4px', border: '1px solid var(--color-border)' }}
    >
      {statuses.map(s => (
        <option key={s} value={s}>{s}</option>
      ))}
    </select>
  );
};
export default AutomacaoStatusSelect;
