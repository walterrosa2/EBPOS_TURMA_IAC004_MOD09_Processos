import { request } from './api';

export async function gerarAnalise(processoId) {
  return request(`/api/processos/${processoId}/analises`, {
    method: 'POST'
  });
}

export async function listarAnalises(processoId) {
  return request(`/api/processos/${processoId}/analises`, {
    method: 'GET'
  });
}

export async function obterAnalise(analiseId) {
  return request(`/api/analises/${analiseId}`, {
    method: 'GET'
  });
}
