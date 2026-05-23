import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { listarProcessos, excluirProcesso } from '../services/processosApi';
import ProcessoTable from '../components/processos/ProcessoTable';
import ProcessoFilters from '../components/processos/ProcessoFilters';
import Card from '../components/common/Card';
import Button from '../components/common/Button';
import LoadingState from '../components/common/LoadingState';
import ErrorState from '../components/common/ErrorState';
import EmptyState from '../components/common/EmptyState';
import ConfirmDialog from '../components/common/ConfirmDialog';
import ImportProcessModal from '../components/processos/ImportProcessModal';

const Processos = () => {
  const [processos, setProcessos] = useState([]);
  const [filters, setFilters] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [processoParaExcluir, setProcessoParaExcluir] = useState(null);
  const [isImportModalOpen, setIsImportModalOpen] = useState(false);
  const navigate = useNavigate();

  const fetchProcessos = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await listarProcessos(filters);
      setProcessos(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // debounce opcional aqui
    const timer = setTimeout(() => {
      fetchProcessos();
    }, 300);
    return () => clearTimeout(timer);
  }, [filters]);

  const handleExcluir = async () => {
    if (!processoParaExcluir) return;
    try {
      await excluirProcesso(processoParaExcluir);
      setProcessos(processos.filter(p => p.id !== processoParaExcluir));
      setProcessoParaExcluir(null);
    } catch (err) {
      alert(`Erro ao excluir: ${err.message}`);
    }
  };

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
        <ProcessoFilters filters={filters} onFilterChange={setFilters} />
        <div style={{ display: 'flex', gap: '12px' }}>
          <Button 
            onClick={() => setIsImportModalOpen(true)} 
            style={{ backgroundColor: '#0284c7', color: '#ffffff' }}
          >
            💻 Importar por IA
          </Button>
          <Button onClick={() => navigate('/processos/novo')}>+ Novo Processo</Button>
        </div>
      </div>

      <Card>
        {error ? (
          <ErrorState message={error} onRetry={fetchProcessos} />
        ) : loading ? (
          <LoadingState message="Carregando processos..." />
        ) : processos.length === 0 ? (
          <EmptyState 
            message="Nenhum processo encontrado com estes filtros." 
            actionText="Limpar Filtros" 
            onAction={() => setFilters({})}
          />
        ) : (
          <ProcessoTable processos={processos} onDelete={setProcessoParaExcluir} />
        )}
      </Card>

      <ConfirmDialog
        isOpen={!!processoParaExcluir}
        title="Excluir Processo"
        message="Tem certeza de que deseja excluir este processo? Todas as etapas relacionadas também serão removidas. Esta ação não pode ser desfeita."
        onConfirm={handleExcluir}
        onCancel={() => setProcessoParaExcluir(null)}
      />

      <ImportProcessModal
        isOpen={isImportModalOpen}
        onClose={() => {
          setIsImportModalOpen(false);
          fetchProcessos();
        }}
      />
    </div>
  );
};

export default Processos;
