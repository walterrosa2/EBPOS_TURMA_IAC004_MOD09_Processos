import { request } from './api';

export const listarProcessos = async (filters = {}) => {
  const queryParams = new URLSearchParams();
  
  if (filters.area) queryParams.append('area', filters.area);
  if (filters.criticidade) queryParams.append('criticidade', filters.criticidade);
  if (filters.status) queryParams.append('status', filters.status);
  if (filters.q) queryParams.append('q', filters.q);
  
  const queryString = queryParams.toString();
  const url = queryString ? `/api/processos?${queryString}` : '/api/processos';
  
  return request(url);
};

export const obterProcesso = async (id) => {
  return request(`/api/processos/${id}`);
};

export const criarProcesso = async (payload) => {
  return request('/api/processos', {
    method: 'POST',
    body: JSON.stringify(payload)
  });
};

export const atualizarProcesso = async (id, payload) => {
  return request(`/api/processos/${id}`, {
    method: 'PUT',
    body: JSON.stringify(payload)
  });
};

export const excluirProcesso = async (id) => {
  return request(`/api/processos/${id}`, {
    method: 'DELETE'
  });
};
