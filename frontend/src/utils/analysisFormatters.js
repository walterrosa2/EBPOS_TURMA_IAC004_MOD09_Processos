export function parseAnaliseResultado(json_resultado) {
  if (typeof json_resultado === 'object' && json_resultado !== null) {
    return json_resultado;
  }
  try {
    return JSON.parse(json_resultado);
  } catch (error) {
    return null;
  }
}

export function getImpactoVariant(impacto) {
  const map = {
    'Alto': 'danger',
    'Médio': 'warning',
    'Baixo': 'success'
  };
  return map[impacto] || 'default';
}

export function getPrioridadeVariant(prioridade) {
  const map = {
    'Urgente': 'danger',
    'Alta': 'warning',
    'Média': 'primary',
    'Baixa': 'default'
  };
  return map[prioridade] || 'default';
}

export function getSeveridadeVariant(severidade) {
  const map = {
    'Alta': 'danger',
    'Média': 'warning',
    'Baixa': 'success'
  };
  return map[severidade] || 'default';
}

export function formatDateTime(dateString) {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleString('pt-BR');
}

export function safeList(value) {
  return Array.isArray(value) ? value : [];
}
