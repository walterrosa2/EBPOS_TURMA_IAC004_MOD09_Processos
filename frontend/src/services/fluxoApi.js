import { request } from './api';

export const obterFluxo = async (processoId) => {
  return request(`/api/processos/${processoId}/fluxo`);
};

export const salvarFluxo = async (processoId, payload) => {
  return request(`/api/processos/${processoId}/fluxo`, {
    method: 'PUT',
    body: JSON.stringify(payload)
  });
};
