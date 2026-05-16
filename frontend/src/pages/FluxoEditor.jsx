import React, { useState, useEffect, useCallback } from 'react';
import { useParams } from 'react-router-dom';
import { obterFluxo } from '../services/fluxoApi';
import { mapEtapasToNodes, mapConexoesToEdges } from '../utils/flowMappers';
import LoadingState from '../components/common/LoadingState';
import ErrorState from '../components/common/ErrorState';
import FlowEditor from '../components/fluxo/FlowEditor';

const FluxoEditor = () => {
  const { id } = useParams();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [flowData, setFlowData] = useState(null);

  const fetchFluxo = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await obterFluxo(id);
      
      const nodes = mapEtapasToNodes(data.etapas || []);
      const edges = mapConexoesToEdges(data.conexoes || []);
      
      setFlowData({ nodes, edges });
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [id]);

  useEffect(() => {
    fetchFluxo();
  }, [fetchFluxo]);

  if (loading && !flowData) return <LoadingState message="Carregando fluxo visual..." />;
  if (error && !flowData) return <ErrorState message={error} onRetry={fetchFluxo} />;

  return (
    <div style={{ width: '100%', height: 'calc(100vh - 64px)' }}>
      {flowData && (
        <FlowEditor 
          processoId={id} 
          initialNodes={flowData.nodes} 
          initialEdges={flowData.edges} 
          onReload={fetchFluxo} 
        />
      )}
    </div>
  );
};

export default FluxoEditor;
