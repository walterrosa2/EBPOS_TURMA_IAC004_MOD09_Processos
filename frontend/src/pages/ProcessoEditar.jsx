import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import ProcessoForm from '../components/processos/ProcessoForm';
import { obterProcesso, atualizarProcesso } from '../services/processosApi';
import LoadingState from '../components/common/LoadingState';
import ErrorState from '../components/common/ErrorState';

const ProcessoEditar = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [processo, setProcesso] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);

  const fetchProcesso = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await obterProcesso(id);
      setProcesso(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProcesso();
  }, [id]);

  const handleSubmit = async (data) => {
    try {
      setSaving(true);
      setError(null);
      await atualizarProcesso(id, data);
      navigate(`/processos/${id}`);
    } catch (err) {
      setError(err.message);
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <LoadingState message="Carregando processo..." />;
  if (error && !processo) return <ErrorState message={error} onRetry={fetchProcesso} />;

  return (
    <div>
      <ProcessoForm initialData={processo} onSubmit={handleSubmit} loading={saving} error={error} />
    </div>
  );
};

export default ProcessoEditar;
