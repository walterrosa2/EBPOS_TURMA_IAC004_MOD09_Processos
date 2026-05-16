import React, { useState, useCallback, useMemo } from 'react';
import ReactFlow, { 
  Background, 
  Controls, 
  MiniMap,
  applyNodeChanges,
  applyEdgeChanges,
  addEdge
} from 'reactflow';
import EtapaNode from './EtapaNode';
import FlowEmptyState from './FlowEmptyState';
import FlowToolbar from './FlowToolbar';
import EtapaPanel from './EtapaPanel';

import { criarEtapa, atualizarEtapa, excluirEtapa } from '../../services/etapasApi';
import { salvarFluxo } from '../../services/fluxoApi';
import { mapNodesToEtapasPayload, mapEdgesToConexoesPayload } from '../../utils/flowMappers';

const FlowEditor = ({ processoId, initialNodes, initialEdges, onReload }) => {
  const [nodes, setNodes] = useState(initialNodes);
  const [edges, setEdges] = useState(initialEdges);
  const [panelMode, setPanelMode] = useState(null); // 'create' | 'edit' | null
  const [selectedEtapa, setSelectedEtapa] = useState(null);
  const [saving, setSaving] = useState(false);
  const [panelError, setPanelError] = useState(null);
  
  const nodeTypes = useMemo(() => ({ etapaNode: EtapaNode }), []);

  const onNodesChange = useCallback(
    (changes) => setNodes((nds) => applyNodeChanges(changes, nds)),
    []
  );

  const onEdgesChange = useCallback(
    (changes) => setEdges((eds) => applyEdgeChanges(changes, eds)),
    []
  );

  const onConnect = useCallback(
    (params) => setEdges((eds) => addEdge({ ...params, type: 'smoothstep', label: 'sequencial' }, eds)),
    []
  );

  const onNodeClick = (event, node) => {
    setSelectedEtapa(node.data.etapa);
    setPanelMode('edit');
    setPanelError(null);
  };

  const handleAddEtapa = () => {
    setSelectedEtapa(null);
    setPanelMode('create');
    setPanelError(null);
  };

  const handleClosePanel = () => {
    setPanelMode(null);
    setSelectedEtapa(null);
  };

  const handleSaveEtapa = async (etapaData) => {
    try {
      setSaving(true);
      setPanelError(null);
      if (panelMode === 'create') {
        const payload = { ...etapaData, posicao_x: 50, posicao_y: 50 };
        await criarEtapa(processoId, payload);
      } else if (panelMode === 'edit') {
        const payload = { ...etapaData };
        await atualizarEtapa(selectedEtapa.id, payload);
      }
      handleClosePanel();
      onReload();
    } catch (err) {
      setPanelError(err.message);
    } finally {
      setSaving(false);
    }
  };

  const handleDeleteEtapa = async () => {
    if (!selectedEtapa) return;
    if (!window.confirm('Deseja realmente excluir esta etapa?')) return;
    try {
      setSaving(true);
      setPanelError(null);
      await excluirEtapa(selectedEtapa.id);
      handleClosePanel();
      onReload();
    } catch (err) {
      setPanelError(err.message);
    } finally {
      setSaving(false);
    }
  };

  const handleSaveFluxo = async () => {
    try {
      setSaving(true);
      const payload = {
        etapas: mapNodesToEtapasPayload(nodes),
        conexoes: mapEdgesToConexoesPayload(edges)
      };
      await salvarFluxo(processoId, payload);
      alert('Fluxo salvo com sucesso!');
      onReload();
    } catch (err) {
      alert(`Erro ao salvar fluxo: ${err.message}`);
    } finally {
      setSaving(false);
    }
  };

  const isFlowEmpty = nodes.length === 0 && panelMode !== 'create';

  return (
    <div style={{ width: '100%', height: '100%', display: 'flex', position: 'relative' }}>
      <div style={{ flex: 1, position: 'relative' }}>
        <FlowToolbar 
          processoId={processoId} 
          onAddEtapa={handleAddEtapa} 
          onSave={handleSaveFluxo}
          onReload={onReload}
          saving={saving}
        />
        
        {isFlowEmpty && <FlowEmptyState onAddEtapa={handleAddEtapa} />}

        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          onNodeClick={onNodeClick}
          nodeTypes={nodeTypes}
          fitView
          deleteKeyCode={['Backspace', 'Delete']}
        >
          <Background color="#ccc" gap={16} />
          <Controls />
          <MiniMap />
        </ReactFlow>
      </div>

      {panelMode && (
        <EtapaPanel 
          mode={panelMode}
          initialData={selectedEtapa}
          onSave={handleSaveEtapa}
          onCancel={handleClosePanel}
          onDelete={handleDeleteEtapa}
          saving={saving}
          error={panelError}
        />
      )}
    </div>
  );
};

export default FlowEditor;
