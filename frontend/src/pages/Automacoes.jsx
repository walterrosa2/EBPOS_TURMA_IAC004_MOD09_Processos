import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { listarDiretrizes, atualizarDiretriz } from '../services/diretrizesApi';
import { obterProcesso } from '../services/processosApi';
import LoadingState from '../components/common/LoadingState';
import ErrorState from '../components/common/ErrorState';
import EmptyState from '../components/common/EmptyState';
import Button from '../components/common/Button';
import AutomacaoBoard from '../components/automacoes/AutomacaoBoard';

const Automacoes = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [processo, setProcesso] = useState(null);
  const [diretrizes, setDiretrizes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({ text: '', prioridade: '', status: '' });

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);
      const proc = await obterProcesso(id);
      setProcesso(proc);
      
      const data = await listarDiretrizes(id);
      // Ordenar por prioridade Urgente -> Alta -> Média -> Baixa, e depois mais recentes
      const prioMap = { 'Urgente': 4, 'Alta': 3, 'Média': 2, 'Baixa': 1 };
      data.sort((a, b) => {
        const pA = prioMap[a.prioridade] || 0;
        const pB = prioMap[b.prioridade] || 0;
        if (pA !== pB) return pB - pA;
        return new Date(b.criado_em) - new Date(a.criado_em);
      });
      setDiretrizes(data);
    } catch (err) {
      setError(err.message || 'Erro ao carregar automações.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [id]);

  const handleStatusChange = async (diretrizId, novoStatus) => {
    try {
      await atualizarDiretriz(diretrizId, { status: novoStatus });
      setDiretrizes(prev => prev.map(d => d.id === diretrizId ? { ...d, status: novoStatus } : d));
    } catch (err) {
      alert('Erro ao atualizar status: ' + err.message);
    }
  };

  if (loading) return <LoadingState message="Carregando diretrizes de automação..." />;
  if (error) return <ErrorState message={error} onRetry={fetchData} />;

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
        <div style={{ display: 'flex', gap: '16px', alignItems: 'center' }}>
          <Button variant="secondary" onClick={() => navigate(`/processos/${id}`)}>&larr; Voltar</Button>
          <h2 style={{ fontSize: '1.5rem', margin: 0 }}>Automações: {processo?.nome}</h2>
        </div>
      </div>

      {diretrizes.length === 0 ? (
        <EmptyState 
          title="Nenhuma diretriz de automação" 
          description="Ainda não existem diretrizes geradas para este processo. Faça uma Análise IA primeiro para gerar as sugestões."
          action={<Button variant="primary" onClick={() => navigate(`/processos/${id}/analises`)}>Ir para Análises</Button>}
        />
      ) : (
        <AutomacaoBoard 
          diretrizes={diretrizes} 
          onStatusChange={handleStatusChange} 
          filters={filters} 
          setFilters={setFilters} 
        />
      )}
    </div>
  );
};

export default Automacoes;
