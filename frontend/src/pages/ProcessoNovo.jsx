import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import ProcessoForm from '../components/processos/ProcessoForm';
import { criarProcesso } from '../services/processosApi';

const ProcessoNovo = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleSubmit = async (data) => {
    try {
      setLoading(true);
      setError(null);
      const newProcesso = await criarProcesso(data);
      navigate(`/processos/${newProcesso.id}`);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <ProcessoForm onSubmit={handleSubmit} loading={loading} error={error} />
    </div>
  );
};

export default ProcessoNovo;
