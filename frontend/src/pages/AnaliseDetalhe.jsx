import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { obterAnalise } from '../services/analisesApi';
import { obterProcesso } from '../services/processosApi';
import LoadingState from '../components/common/LoadingState';
import ErrorState from '../components/common/ErrorState';
import { parseAnaliseResultado } from '../utils/analysisFormatters';

import AnaliseHeader from '../components/ia/AnaliseHeader';
import AnaliseSummaryCard from '../components/ia/AnaliseSummaryCard';
import MaturidadeCard from '../components/ia/MaturidadeCard';
import GargalosList from '../components/ia/GargalosList';
import RiscosList from '../components/ia/RiscosList';
import MelhoriasList from '../components/ia/MelhoriasList';
import AutomacoesList from '../components/ia/AutomacoesList';
import OportunidadesIAList from '../components/ia/OportunidadesIAList';
import LacunasList from '../components/ia/LacunasList';
import IndicadoresList from '../components/ia/IndicadoresList';
import PerguntasList from '../components/ia/PerguntasList';
import AlertasList from '../components/ia/AlertasList';

const AnaliseDetalhe = () => {
  const { id, analiseId } = useParams();
  const navigate = useNavigate();
  const [analise, setAnalise] = useState(null);
  const [processo, setProcesso] = useState(null);
  const [parsedData, setParsedData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchAnalise = async () => {
    try {
      setLoading(true);
      setError(null);
      const proc = await obterProcesso(id);
      setProcesso(proc);
      const data = await obterAnalise(analiseId);
      setAnalise(data);
      
      const parsed = parseAnaliseResultado(data.json_resultado);
      if (!parsed) {
        throw new Error("Não foi possível interpretar o resultado da análise.");
      }
      setParsedData(parsed);
    } catch (err) {
      setError(err.message || 'Erro ao carregar análise.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAnalise();
  }, [id, analiseId]);

  if (loading) return <LoadingState message="Carregando relatório de análise..." />;
  if (error) return <ErrorState message={error} onRetry={fetchAnalise} />;
  if (!parsedData) return <ErrorState message="Análise inválida." />;

  return (
    <div style={{ paddingBottom: '40px' }}>
      <AnaliseHeader 
        processoNome={processo?.nome}
        createdAt={analise.criado_em}
        onBack={() => navigate(`/processos/${id}/analises`)}
        onGoToAutomacoes={() => navigate(`/processos/${id}/automacoes`)}
      />

      <AlertasList alertas={parsedData.alertas} />

      <div style={{ display: 'grid', gap: '24px' }}>
        <AnaliseSummaryCard 
          resumoExecutivo={parsedData.resumo_executivo}
          diagnosticoOperacional={parsedData.diagnostico_operacional}
        />
        
        <MaturidadeCard maturidade={parsedData.nivel_maturidade} />
        
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px' }}>
          <GargalosList gargalos={parsedData.gargalos} />
          <RiscosList riscos={parsedData.riscos} />
        </div>
        
        <MelhoriasList melhorias={parsedData.sugestoes_melhoria} />
        <AutomacoesList automacoes={parsedData.sugestoes_automacao} />
        <OportunidadesIAList oportunidades={parsedData.oportunidades_ia} />
        
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px' }}>
          <LacunasList lacunas={parsedData.lacunas_mapeamento} />
          <IndicadoresList indicadores={parsedData.indicadores_recomendados} />
        </div>
        
        <PerguntasList perguntas={parsedData.perguntas_para_aprofundamento} />
      </div>
    </div>
  );
};

export default AnaliseDetalhe;
