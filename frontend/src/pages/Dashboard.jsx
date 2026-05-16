import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { listarProcessos } from '../services/processosApi';
import MetricCard from '../components/dashboard/MetricCard';
import RecentProcesses from '../components/dashboard/RecentProcesses';
import LoadingState from '../components/common/LoadingState';
import ErrorState from '../components/common/ErrorState';
import EmptyState from '../components/common/EmptyState';
import Button from '../components/common/Button';

const Dashboard = () => {
  const [processos, setProcessos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const fetchDados = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await listarProcessos();
      setProcessos(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDados();
  }, []);

  if (loading) return <LoadingState message="Carregando indicadores do dashboard..." />;
  if (error) return <ErrorState message={error} onRetry={fetchDados} />;

  if (processos.length === 0) {
    return (
      <EmptyState 
        message="Nenhum processo mapeado ainda." 
        actionText="Criar meu primeiro processo" 
        onAction={() => navigate('/processos/novo')} 
      />
    );
  }

  const processosCriticos = processos.filter(p => p.criticidade === 'Alta').length;
  const processosRascunho = processos.filter(p => p.status === 'Rascunho').length;
  const processosAnalisados = processos.filter(p => p.status === 'Analisado').length;

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: '24px' }}>
        <Button onClick={() => navigate('/processos/novo')}>+ Novo Processo</Button>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '24px', marginBottom: '32px' }}>
        <MetricCard 
          title="Total de Processos" 
          value={processos.length} 
          description="Processos catalogados" 
          color="var(--color-primary)" 
        />
        <MetricCard 
          title="Criticidade Alta" 
          value={processosCriticos} 
          description="Atenção prioritária" 
          color="var(--color-danger)" 
        />
        <MetricCard 
          title="Rascunhos" 
          value={processosRascunho} 
          description="Aguardando mapeamento" 
          color="var(--color-muted)" 
        />
        <MetricCard 
          title="Analisados" 
          value={processosAnalisados} 
          description="Mapeados e avaliados" 
          color="var(--color-success)" 
        />
      </div>

      <RecentProcesses processos={processos} />
    </div>
  );
};

export default Dashboard;
