import { request } from './api';

export const listarEtapas = async (processoId) => {
  return request(`/api/processos/${processoId}/etapas`);
};

export const criarEtapa = async (processoId, payload) => {
  return request(`/api/processos/${processoId}/etapas`, {
    method: 'POST',
    body: JSON.stringify(payload)
  });
};

export const atualizarEtapa = async (etapaId, payload) => {
  return request(`/api/etapas/${etapaId}`, {
    method: 'PUT',
    body: JSON.stringify(payload)
  });
};

export const excluirEtapa = async (etapaId) => {
  return request(`/api/etapas/${etapaId}`, {
    method: 'DELETE'
  });
};
