import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { obterProcesso } from '../services/processosApi';
import { gerarAnalise } from '../services/analisesApi';
import Card from '../components/common/Card';
import Button from '../components/common/Button';
import LoadingState from '../components/common/LoadingState';
import ErrorState from '../components/common/ErrorState';
import ProcessoStatusBadge from '../components/processos/ProcessoStatusBadge';
import ProcessoCriticidadeBadge from '../components/processos/ProcessoCriticidadeBadge';
import { formatDate } from '../utils/formatters';

const ProcessoDetalhe = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [processo, setProcesso] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [analiseLoading, setAnaliseLoading] = useState(false);

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

  const handleGerarAnalise = async () => {
    try {
      setAnaliseLoading(true);
      const data = await gerarAnalise(id);
      navigate(`/processos/${id}/analises/${data.id}`);
    } catch (err) {
      if (err.message.includes('etapas')) {
        alert('O processo precisa ter pelo menos uma etapa cadastrada antes da análise IA.');
      } else if (err.message.includes('API_KEY')) {
        alert('O serviço de IA ainda não está configurado. Verifique a configuração do backend.');
      } else {
        alert(err.message || 'Não foi possível gerar a análise agora. Tente novamente em instantes.');
      }
    } finally {
      setAnaliseLoading(false);
    }
  };

  useEffect(() => {
    fetchProcesso();
  }, [id]);

  if (loading) return <LoadingState message="Carregando processo..." />;
  if (error) return <ErrorState message={error} onRetry={fetchProcesso} />;
  if (!processo) return <ErrorState message="Processo não encontrado." />;

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '24px' }}>
        <Button variant="secondary" onClick={() => navigate('/processos')}>&larr; Voltar</Button>
        <div style={{ display: 'flex', gap: '12px' }}>
          <Button variant="secondary" onClick={() => navigate(`/processos/${id}/editar`)}>Editar</Button>
          <Button variant="primary" onClick={() => navigate(`/processos/${id}/fluxo`)}>Abrir Fluxo Visual</Button>
          <Button variant="secondary" onClick={() => navigate(`/processos/${id}/analises`)}>Ver Análises</Button>
          <Button variant="secondary" onClick={() => navigate(`/processos/${id}/automacoes`)}>Ver Automações</Button>
          <Button 
            variant="primary" 
            onClick={handleGerarAnalise} 
            disabled={analiseLoading}
          >
            {analiseLoading ? 'Gerando Análise...' : 'Analisar com IA'}
          </Button>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '24px' }}>
        <Card>
          <div style={{ marginBottom: '24px' }}>
            <h2 style={{ fontSize: '1.5rem', marginBottom: '8px' }}>{processo.nome}</h2>
            <div style={{ display: 'flex', gap: '8px' }}>
              <ProcessoStatusBadge status={processo.status} />
              <ProcessoCriticidadeBadge criticidade={processo.criticidade} />
            </div>
          </div>

          <div style={{ display: 'grid', gap: '24px' }}>
            <div>
              <h3 style={{ fontSize: '1rem', color: 'var(--color-muted)', marginBottom: '8px' }}>Descrição</h3>
              <p>{processo.descricao || '-'}</p>
            </div>
            <div>
              <h3 style={{ fontSize: '1rem', color: 'var(--color-muted)', marginBottom: '8px' }}>Objetivo</h3>
              <p>{processo.objetivo || '-'}</p>
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
              <div>
                <h3 style={{ fontSize: '1rem', color: 'var(--color-muted)', marginBottom: '8px' }}>Sistemas Utilizados</h3>
                <p>{processo.sistemas_utilizados || '-'}</p>
              </div>
              <div>
                <h3 style={{ fontSize: '1rem', color: 'var(--color-muted)', marginBottom: '8px' }}>Documentos Utilizados</h3>
                <p>{processo.documentos_utilizados || '-'}</p>
              </div>
            </div>
            <div>
              <h3 style={{ fontSize: '1rem', color: 'var(--color-muted)', marginBottom: '8px' }}>Observações</h3>
              <p>{processo.observacoes || '-'}</p>
            </div>
          </div>
        </Card>

        <Card>
          <h3 style={{ fontSize: '1.125rem', marginBottom: '16px' }}>Metadados</h3>
          <div style={{ display: 'grid', gap: '16px' }}>
            <div>
              <span style={{ color: 'var(--color-muted)', fontSize: '0.875rem', display: 'block' }}>Área</span>
              <span style={{ fontWeight: '500' }}>{processo.area}</span>
            </div>
            <div>
              <span style={{ color: 'var(--color-muted)', fontSize: '0.875rem', display: 'block' }}>Responsável</span>
              <span style={{ fontWeight: '500' }}>{processo.responsavel || '-'}</span>
            </div>
            <div>
              <span style={{ color: 'var(--color-muted)', fontSize: '0.875rem', display: 'block' }}>Periodicidade</span>
              <span style={{ fontWeight: '500' }}>{processo.periodicidade || '-'}</span>
            </div>
            <div>
              <span style={{ color: 'var(--color-muted)', fontSize: '0.875rem', display: 'block' }}>Criado em</span>
              <span style={{ fontWeight: '500' }}>{formatDate(processo.criado_em)}</span>
            </div>
            <div>
              <span style={{ color: 'var(--color-muted)', fontSize: '0.875rem', display: 'block' }}>Atualizado em</span>
              <span style={{ fontWeight: '500' }}>{formatDate(processo.atualizado_em)}</span>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
};

export default ProcessoDetalhe;
