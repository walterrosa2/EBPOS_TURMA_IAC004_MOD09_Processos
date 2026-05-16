import React from 'react';
import { AREAS_CONTABEIS, CRITICIDADES, STATUS_PROCESSO } from '../../utils/constants';

const ProcessoFilters = ({ filters, onFilterChange }) => {
  const handleChange = (e) => {
    const { name, value } = e.target;
    onFilterChange({ ...filters, [name]: value });
  };

  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: '16px', marginBottom: '24px' }}>
      <div>
        <input
          type="text"
          name="q"
          placeholder="Buscar por nome..."
          value={filters.q || ''}
          onChange={handleChange}
        />
      </div>
      <div>
        <select name="area" value={filters.area || ''} onChange={handleChange}>
          <option value="">Todas as áreas</option>
          {AREAS_CONTABEIS.map(area => <option key={area} value={area}>{area}</option>)}
        </select>
      </div>
      <div>
        <select name="criticidade" value={filters.criticidade || ''} onChange={handleChange}>
          <option value="">Todas criticidades</option>
          {CRITICIDADES.map(c => <option key={c} value={c}>{c}</option>)}
        </select>
      </div>
      <div>
        <select name="status" value={filters.status || ''} onChange={handleChange}>
          <option value="">Todos os status</option>
          {STATUS_PROCESSO.map(s => <option key={s} value={s}>{s}</option>)}
        </select>
      </div>
    </div>
  );
};

export default ProcessoFilters;
