import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { listarAnalises, gerarAnalise } from '../services/analisesApi';
import { obterProcesso } from '../services/processosApi';
import Card from '../components/common/Card';
import Button from '../components/common/Button';
import LoadingState from '../components/common/LoadingState';
import ErrorState from '../components/common/ErrorState';
import EmptyState from '../components/common/EmptyState';
import { formatDateTime } from '../utils/analysisFormatters';

const Analises = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [processo, setProcesso] = useState(null);
  const [analises, setAnalises] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [generating, setGenerating] = useState(false);

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);
      const procData = await obterProcesso(id);
      setProcesso(procData);
      
      const analisesData = await listarAnalises(id);
      setAnalises(analisesData.sort((a, b) => new Date(b.criado_em) - new Date(a.criado_em)));
    } catch (err) {
      setError(err.message || 'Erro ao carregar análises.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [id]);

  const handleGerarAnalise = async () => {
    try {
      setGenerating(true);
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
      setGenerating(false);
    }
  };

  if (loading) return <LoadingState message="Carregando análises..." />;
  if (error) return <ErrorState message={error} onRetry={fetchData} />;

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '24px' }}>
        <div style={{ display: 'flex', gap: '16px', alignItems: 'center' }}>
          <Button variant="secondary" onClick={() => navigate(`/processos/${id}`)}>&larr; Voltar ao Processo</Button>
          <h2 style={{ fontSize: '1.25rem', margin: 0 }}>Análises de Automação: {processo?.nome}</h2>
        </div>
        <Button 
          variant="primary" 
          onClick={handleGerarAnalise} 
          disabled={generating}
        >
          {generating ? 'Gerando Análise...' : 'Gerar Nova Análise IA'}
        </Button>
      </div>

      {analises.length === 0 ? (
        <EmptyState 
          title="Nenhuma análise encontrada" 
          description="Este processo ainda não foi analisado pela IA. Clique no botão acima para gerar o primeiro diagnóstico operacional e diretrizes de automação."
        />
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          {analises.map(analise => (
            <Card key={analise.id}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                <div>
                  <h3 style={{ fontSize: '1.1rem', marginBottom: '8px' }}>
                    Análise #{analise.id} - {formatDateTime(analise.criado_em)}
                  </h3>
                  <div style={{ display: 'flex', gap: '12px', marginBottom: '12px' }}>
                    <span style={{ 
                      padding: '4px 8px', 
                      borderRadius: '4px', 
                      fontSize: '0.875rem',
                      backgroundColor: 'var(--color-primary-light, #e0e7ff)',
                      color: 'var(--color-primary, #4338ca)',
                      fontWeight: '500'
                    }}>
                      Maturidade: {analise.nivel_maturidade || 'Não avaliada'}
                    </span>
                  </div>
                  <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem', maxWidth: '800px' }}>
                    {analise.resumo_executivo}
                  </p>
                </div>
                <Button 
                  variant="primary" 
                  onClick={() => navigate(`/processos/${id}/analises/${analise.id}`)}
                >
                  Abrir Análise Completa
                </Button>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
};

export default Analises;
