const API_BASE_URL = import.meta.env.VITE_API_URL !== undefined 
  ? import.meta.env.VITE_API_URL 
  : (import.meta.env.DEV ? 'http://localhost:8000' : '');

/**
 * Envia o arquivo DOCX via multipart/form-data para o endpoint de importação da API.
 * @param {File} file - Arquivo .docx selecionado pelo usuário.
 * @returns {Promise<Object>} Resposta contendo processo_id e metadados.
 */
export async function importarProcessoDocx(file) {
  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await fetch(`${API_BASE_URL}/api/processos/importar`, {
      method: 'POST',
      body: formData
      // Importante: Deixar o cabeçalho 'Content-Type' vazio para que o navegador
      // defina automaticamente o boundary correto para 'multipart/form-data'.
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || data.message || 'Ocorreu um erro ao importar o documento.');
    }

    return data;
  } catch (error) {
    if (error.name === 'TypeError') {
      throw new Error('Falha de conexão: Verifique se a API está online.');
    }
    throw error;
  }
}
