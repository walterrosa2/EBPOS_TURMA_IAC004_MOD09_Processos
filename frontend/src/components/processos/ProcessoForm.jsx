import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Card from '../common/Card';
import Button from '../common/Button';
import ErrorState from '../common/ErrorState';
import { AREAS_CONTABEIS, CRITICIDADES, STATUS_PROCESSO, PERIODICIDADES } from '../../utils/constants';

const ProcessoForm = ({ initialData, onSubmit, loading, error }) => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    nome: '',
    area: '',
    descricao: '',
    objetivo: '',
    responsavel: '',
    periodicidade: 'Sob demanda',
    criticidade: 'Média',
    status: 'Rascunho',
    sistemas_utilizados: '',
    documentos_utilizados: '',
    observacoes: ''
  });
  const [validationError, setValidationError] = useState('');

  useEffect(() => {
    if (initialData) {
      setFormData({
        ...initialData,
        sistemas_utilizados: initialData.sistemas_utilizados || '',
        documentos_utilizados: initialData.documentos_utilizados || '',
        observacoes: initialData.observacoes || '',
        descricao: initialData.descricao || '',
        objetivo: initialData.objetivo || '',
        responsavel: initialData.responsavel || ''
      });
    }
  }, [initialData]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setValidationError('');
    
    if (!formData.nome.trim()) {
      setValidationError('O campo Nome é obrigatório.');
      return;
    }
    if (!formData.area.trim()) {
      setValidationError('O campo Área é obrigatório.');
      return;
    }

    onSubmit(formData);
  };

  return (
    <Card>
      <form onSubmit={handleSubmit} style={{ display: 'grid', gap: '20px' }}>
        {error && <ErrorState message={error} />}
        {validationError && <ErrorState message={validationError} />}

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
          <div>
            <label style={{ display: 'block', marginBottom: '8px', fontWeight: '500' }}>Nome do Processo *</label>
            <input type="text" name="nome" value={formData.nome} onChange={handleChange} required />
          </div>
          <div>
            <label style={{ display: 'block', marginBottom: '8px', fontWeight: '500' }}>Área *</label>
            <select name="area" value={formData.area} onChange={handleChange} required>
              <option value="">Selecione uma área</option>
              {AREAS_CONTABEIS.map(area => <option key={area} value={area}>{area}</option>)}
            </select>
          </div>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
          <div>
            <label style={{ display: 'block', marginBottom: '8px', fontWeight: '500' }}>Descrição</label>
            <textarea name="descricao" value={formData.descricao} onChange={handleChange} rows={3} />
          </div>
          <div>
            <label style={{ display: 'block', marginBottom: '8px', fontWeight: '500' }}>Objetivo</label>
            <textarea name="objetivo" value={formData.objetivo} onChange={handleChange} rows={3} />
          </div>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr 1fr', gap: '16px' }}>
          <div>
            <label style={{ display: 'block', marginBottom: '8px', fontWeight: '500' }}>Responsável</label>
            <input type="text" name="responsavel" value={formData.responsavel} onChange={handleChange} />
          </div>
          <div>
            <label style={{ display: 'block', marginBottom: '8px', fontWeight: '500' }}>Periodicidade</label>
            <select name="periodicidade" value={formData.periodicidade} onChange={handleChange}>
              {PERIODICIDADES.map(p => <option key={p} value={p}>{p}</option>)}
            </select>
          </div>
          <div>
            <label style={{ display: 'block', marginBottom: '8px', fontWeight: '500' }}>Criticidade</label>
            <select name="criticidade" value={formData.criticidade} onChange={handleChange}>
              {CRITICIDADES.map(c => <option key={c} value={c}>{c}</option>)}
            </select>
          </div>
          <div>
            <label style={{ display: 'block', marginBottom: '8px', fontWeight: '500' }}>Status</label>
            <select name="status" value={formData.status} onChange={handleChange}>
              {STATUS_PROCESSO.map(s => <option key={s} value={s}>{s}</option>)}
            </select>
          </div>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
          <div>
            <label style={{ display: 'block', marginBottom: '8px', fontWeight: '500' }}>Sistemas Utilizados</label>
            <input type="text" name="sistemas_utilizados" value={formData.sistemas_utilizados} onChange={handleChange} />
          </div>
          <div>
            <label style={{ display: 'block', marginBottom: '8px', fontWeight: '500' }}>Documentos Utilizados</label>
            <input type="text" name="documentos_utilizados" value={formData.documentos_utilizados} onChange={handleChange} />
          </div>
        </div>

        <div>
          <label style={{ display: 'block', marginBottom: '8px', fontWeight: '500' }}>Observações</label>
          <textarea name="observacoes" value={formData.observacoes} onChange={handleChange} rows={2} />
        </div>

        <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '16px', marginTop: '16px' }}>
          <Button variant="secondary" onClick={() => navigate(-1)} disabled={loading}>Cancelar</Button>
          <Button type="submit" loading={loading}>Salvar Processo</Button>
        </div>
      </form>
    </Card>
  );
};

export default ProcessoForm;
