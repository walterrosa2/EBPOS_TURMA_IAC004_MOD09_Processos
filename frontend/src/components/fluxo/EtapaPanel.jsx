import React, { useState, useEffect } from 'react';
import Button from '../common/Button';
import ErrorState from '../common/ErrorState';

const TIPOS_ETAPA = [
  'Entrada de informação',
  'Conferência',
  'Processamento',
  'Aprovação',
  'Envio',
  'Controle',
  'Arquivamento',
  'Decisão',
  'Comunicação',
  'Outro'
];

const EtapaPanel = ({ mode, initialData, onSave, onCancel, onDelete, saving, error }) => {
  const [formData, setFormData] = useState({
    nome: '',
    descricao: '',
    responsavel: '',
    entrada: '',
    saida: '',
    sistema_utilizado: '',
    tempo_estimado: '',
    tipo_etapa: '',
    risco: '',
    gargalo: '',
    oportunidade_automacao: ''
  });
  const [validationError, setValidationError] = useState('');

  useEffect(() => {
    if (mode === 'edit' && initialData) {
      setFormData({
        nome: initialData.nome || '',
        descricao: initialData.descricao || '',
        responsavel: initialData.responsavel || '',
        entrada: initialData.entrada || '',
        saida: initialData.saida || '',
        sistema_utilizado: initialData.sistema_utilizado || '',
        tempo_estimado: initialData.tempo_estimado || '',
        tipo_etapa: initialData.tipo_etapa || '',
        risco: initialData.risco || '',
        gargalo: initialData.gargalo || '',
        oportunidade_automacao: initialData.oportunidade_automacao || ''
      });
    } else {
      setFormData({
        nome: '', descricao: '', responsavel: '', entrada: '', saida: '',
        sistema_utilizado: '', tempo_estimado: '', tipo_etapa: '',
        risco: '', gargalo: '', oportunidade_automacao: ''
      });
    }
  }, [mode, initialData]);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!formData.nome.trim()) {
      setValidationError('O nome da etapa é obrigatório.');
      return;
    }
    setValidationError('');
    onSave(formData);
  };

  return (
    <div style={{
      width: '320px',
      height: '100%',
      backgroundColor: 'var(--color-surface)',
      borderLeft: '1px solid var(--color-border)',
      display: 'flex',
      flexDirection: 'column',
      zIndex: 10,
      boxShadow: 'var(--shadow-md)',
      position: 'relative'
    }}>
      <div style={{ padding: '16px', borderBottom: '1px solid var(--color-border)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h3 style={{ margin: 0 }}>{mode === 'create' ? 'Nova Etapa' : 'Editar Etapa'}</h3>
        <button onClick={onCancel} style={{ background: 'none', border: 'none', fontSize: '1.2rem', cursor: 'pointer' }}>&times;</button>
      </div>

      <div style={{ flex: 1, overflowY: 'auto', padding: '16px' }}>
        {error && <ErrorState message={error} />}
        {validationError && <ErrorState message={validationError} />}

        <form id="etapa-form" onSubmit={handleSubmit} style={{ display: 'grid', gap: '12px' }}>
          <div>
            <label style={{ display: 'block', marginBottom: '4px', fontSize: '0.875rem', fontWeight: '500' }}>Nome *</label>
            <input type="text" name="nome" value={formData.nome} onChange={handleChange} required />
          </div>
          <div>
            <label style={{ display: 'block', marginBottom: '4px', fontSize: '0.875rem', fontWeight: '500' }}>Tipo de Etapa</label>
            <select name="tipo_etapa" value={formData.tipo_etapa} onChange={handleChange}>
              <option value="">Selecione...</option>
              {TIPOS_ETAPA.map(t => <option key={t} value={t}>{t}</option>)}
            </select>
          </div>
          <div>
            <label style={{ display: 'block', marginBottom: '4px', fontSize: '0.875rem', fontWeight: '500' }}>Descrição</label>
            <textarea name="descricao" value={formData.descricao} onChange={handleChange} rows={2} />
          </div>
          <div>
            <label style={{ display: 'block', marginBottom: '4px', fontSize: '0.875rem', fontWeight: '500' }}>Responsável</label>
            <input type="text" name="responsavel" value={formData.responsavel} onChange={handleChange} />
          </div>
          <div>
            <label style={{ display: 'block', marginBottom: '4px', fontSize: '0.875rem', fontWeight: '500' }}>Entrada</label>
            <input type="text" name="entrada" value={formData.entrada} onChange={handleChange} />
          </div>
          <div>
            <label style={{ display: 'block', marginBottom: '4px', fontSize: '0.875rem', fontWeight: '500' }}>Saída</label>
            <input type="text" name="saida" value={formData.saida} onChange={handleChange} />
          </div>
          <div>
            <label style={{ display: 'block', marginBottom: '4px', fontSize: '0.875rem', fontWeight: '500' }}>Sistema Utilizado</label>
            <input type="text" name="sistema_utilizado" value={formData.sistema_utilizado} onChange={handleChange} />
          </div>
          <div>
            <label style={{ display: 'block', marginBottom: '4px', fontSize: '0.875rem', fontWeight: '500' }}>Tempo Estimado</label>
            <input type="text" name="tempo_estimado" value={formData.tempo_estimado} onChange={handleChange} />
          </div>
          <div>
            <label style={{ display: 'block', marginBottom: '4px', fontSize: '0.875rem', fontWeight: '500' }}>Risco</label>
            <input type="text" name="risco" value={formData.risco} onChange={handleChange} />
          </div>
          <div>
            <label style={{ display: 'block', marginBottom: '4px', fontSize: '0.875rem', fontWeight: '500' }}>Gargalo</label>
            <input type="text" name="gargalo" value={formData.gargalo} onChange={handleChange} />
          </div>
          <div>
            <label style={{ display: 'block', marginBottom: '4px', fontSize: '0.875rem', fontWeight: '500' }}>Oportunidade Automação</label>
            <textarea name="oportunidade_automacao" value={formData.oportunidade_automacao} onChange={handleChange} rows={2} />
          </div>
        </form>
      </div>

      <div style={{ padding: '16px', borderTop: '1px solid var(--color-border)', display: 'grid', gap: '8px' }}>
        <Button type="submit" form="etapa-form" loading={saving}>Salvar Etapa</Button>
        {mode === 'edit' && (
          <Button variant="danger" onClick={onDelete} disabled={saving}>Excluir Etapa</Button>
        )}
      </div>
    </div>
  );
};

export default EtapaPanel;
