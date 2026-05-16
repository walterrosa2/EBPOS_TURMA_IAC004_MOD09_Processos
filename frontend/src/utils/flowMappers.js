export const mapEtapasToNodes = (etapas) => {
  return etapas.map(etapa => ({
    id: etapa.id.toString(),
    type: 'etapaNode',
    position: {
      x: etapa.posicao_x !== null && etapa.posicao_x !== undefined ? etapa.posicao_x : Math.random() * 200,
      y: etapa.posicao_y !== null && etapa.posicao_y !== undefined ? etapa.posicao_y : Math.random() * 200
    },
    data: {
      etapa: { ...etapa }
    }
  }));
};

export const mapConexoesToEdges = (conexoes) => {
  return conexoes.map(conexao => ({
    id: `${conexao.etapa_origem_id}-${conexao.etapa_destino_id}`,
    source: conexao.etapa_origem_id.toString(),
    target: conexao.etapa_destino_id.toString(),
    type: 'smoothstep',
    label: conexao.tipo_conexao || 'sequencial',
    data: { conexao: { ...conexao } }
  }));
};

export const mapNodesToEtapasPayload = (nodes) => {
  return nodes.map(node => ({
    id: parseInt(node.id, 10),
    posicao_x: Math.round(node.position.x),
    posicao_y: Math.round(node.position.y)
  }));
};

export const mapEdgesToConexoesPayload = (edges) => {
  return edges.map(edge => ({
    etapa_origem_id: parseInt(edge.source, 10),
    etapa_destino_id: parseInt(edge.target, 10),
    tipo_conexao: edge.label || 'sequencial',
    condicao: edge.data?.conexao?.condicao || null
  }));
};
