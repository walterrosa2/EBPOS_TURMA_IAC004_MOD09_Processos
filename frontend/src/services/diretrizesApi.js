import { request } from './api';

export async function listarDiretrizes(processoId) {
  return request(`/api/processos/${processoId}/diretrizes`, {
    method: 'GET'
  });
}

export async function atualizarDiretriz(diretrizId, payload) {
  return request(`/api/diretrizes/${diretrizId}`, {
    method: 'PUT',
    body: JSON.stringify(payload)
  });
}
