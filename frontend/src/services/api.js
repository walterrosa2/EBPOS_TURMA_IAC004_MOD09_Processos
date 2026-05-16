const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export async function request(path, options = {}) {
  try {
    const response = await fetch(`${API_BASE_URL}${path}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });

    if (response.status === 204) {
      return null;
    }

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || data.message || 'Erro ao comunicar com a API');
    }

    return data;
  } catch (error) {
    if (error.name === 'TypeError') {
      throw new Error('Falha de conexão: Verifique se a API está online.');
    }
    throw error;
  }
}
