import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { importarProcessoDocx } from '../../services/processosImportApi';
import Button from '../common/Button';
import Badge from '../common/Badge';

const ImportProcessModal = ({ isOpen, onClose }) => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [successResult, setSuccessResult] = useState(null);
  const fileInputRef = useRef(null);
  const navigate = useNavigate();

  if (!isOpen) return null;

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (!selectedFile) return;

    // Validar extensão
    if (!selectedFile.name.toLowerCase().endsWith('.docx')) {
      setError('Formato inválido. Apenas documentos do tipo Microsoft Word (.docx) são aceitos.');
      setFile(null);
      return;
    }

    // Validar tamanho (10MB)
    if (selectedFile.size > 10 * 1024 * 1024) {
      setError('O arquivo excede o limite máximo permitido de 10 megabytes (MB).');
      setFile(null);
      return;
    }

    setError(null);
    setFile(selectedFile);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const droppedFile = e.dataTransfer.files[0];
    if (!droppedFile) return;

    if (!droppedFile.name.toLowerCase().endsWith('.docx')) {
      setError('Formato inválido. Apenas documentos do tipo Microsoft Word (.docx) são aceitos.');
      return;
    }

    if (droppedFile.size > 10 * 1024 * 1024) {
      setError('O arquivo excede o limite máximo permitido de 10 megabytes (MB).');
      return;
    }

    setError(null);
    setFile(droppedFile);
  };

  const handleImport = async () => {
    if (!file) return;

    try {
      setLoading(true);
      setError(null);
      const data = await importarProcessoDocx(file);
      setSuccessResult(data);
    } catch (err) {
      setError(err.message || 'Erro inesperado ao realizar importação.');
    } finally {
      setLoading(false);
    }
  };

  const handleProceedToProcess = () => {
    if (successResult && successResult.processo_id) {
      navigate(`/processos/${successResult.processo_id}`);
      onClose();
    }
  };

  return (
    <div style={modalOverlayStyle}>
      <div style={modalContentStyle} onDragOver={handleDragOver} onDrop={handleDrop}>
        
        {/* Cabeçalho */}
        <div style={modalHeaderStyle}>
          <h3 style={modalTitleStyle}>
            {!successResult ? '💻 Importar Processo com IA' : '🎉 Processo Importado com Sucesso!'}
          </h3>
          {!loading && (
            <button onClick={onClose} style={closeButtonStyle} aria-label="Fechar">✕</button>
          )}
        </div>

        {/* Corpo do Modal */}
        <div style={modalBodyStyle}>
          {!successResult ? (
            // Etapa 1: Upload e Envio
            <>
              <p style={subtitleStyle}>
                Envie um documento operacional ou manual de procedimentos do processo (formato <strong>.docx</strong>).
                Nossa IA irá estruturar as etapas operacionais, conexões lógicas e preencher metadados.
              </p>

              {/* Área de Drop do Arquivo */}
              <div 
                onClick={() => fileInputRef.current?.click()} 
                style={file ? activeDropZoneStyle : dropZoneStyle}
              >
                <input 
                  type="file" 
                  ref={fileInputRef} 
                  onChange={handleFileChange} 
                  accept=".docx" 
                  style={{ display: 'none' }}
                />
                
                <div style={iconContainerStyle}>
                  {file ? '📄' : '📤'}
                </div>

                {file ? (
                  <div>
                    <h4 style={fileNameStyle}>{file.name}</h4>
                    <p style={fileSizeStyle}>{(file.size / 1024 / 1024).toFixed(2)} MB</p>
                  </div>
                ) : (
                  <div>
                    <p style={dropZoneTextStyle}>Arraste o arquivo .docx aqui ou clique para selecionar</p>
                    <p style={dropZoneSubTextStyle}>Limite de tamanho: 10MB</p>
                  </div>
                )}
              </div>

              {error && <div style={errorBannerStyle}>⚠️ {error}</div>}

              {loading && (
                <div style={loadingContainerStyle}>
                  <div style={spinnerStyle}></div>
                  <p style={loadingTextStyle}>
                    Interpretando documento com IA...<br />
                    <span style={{ fontSize: '12px', opacity: 0.8 }}>
                      Extraindo macroetapas, validando dados sensíveis e estruturando conexões.
                    </span>
                  </p>
                </div>
              )}
            </>
          ) : (
            // Etapa 2: Resultado e Lacunas
            <>
              <div style={successBannerStyle}>
                <strong>{successResult.nome_processo}</strong> foi importado no sistema!
              </div>

              <div style={metricsGridStyle}>
                <div style={metricCardStyle}>
                  <span style={metricNumberStyle}>{successResult.etapas_criadas}</span>
                  <span style={metricLabelStyle}>Etapas Criadas</span>
                </div>
                <div style={metricCardStyle}>
                  <span style={metricNumberStyle}>{successResult.conexoes_criadas}</span>
                  <span style={metricLabelStyle}>Conexões Estabelecidas</span>
                </div>
              </div>

              {/* Alertas Sensíveis (Sanitização) */}
              {successResult.alertas_sensiveis && successResult.alertas_sensiveis.length > 0 && (
                <div style={alertSectionStyle}>
                  <h4 style={sectionTitleStyle}>🔒 Segurança e Sanitização de Dados</h4>
                  <div style={alertsListStyle}>
                    {successResult.alertas_sensiveis.map((alert, idx) => (
                      <div key={idx} style={alertItemStyle}>
                        <strong>[{alert.tipo.toUpperCase()}]</strong> {alert.descricao} - <span style={{ fontStyle: 'italic', color: '#b91c1c' }}>Ação: {alert.acao_aplicada}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Lacunas de Mapeamento */}
              {successResult.lacunas_identificadas && successResult.lacunas_identificadas.length > 0 ? (
                <div style={gapSectionStyle}>
                  <h4 style={sectionTitleStyle}>⚠️ Lacunas de Mapeamento Identificadas</h4>
                  <p style={gapSubtitleStyle}>
                    Recomendamos preencher ou revisar manualmente as seguintes pendências antes de iniciar a análise automatizada do processo:
                  </p>
                  <ul style={gapListStyle}>
                    {successResult.lacunas_identificadas.map((gap, idx) => (
                      <li key={idx} style={gapItemStyle}>{gap}</li>
                    ))}
                  </ul>
                </div>
              ) : (
                <div style={noGapsStyle}>
                  ✨ Nenhum print faltante ou lacuna crítica foi identificada! O processo foi mapeado integralmente.
                </div>
              )}
            </>
          )}
        </div>

        {/* Rodapé / Ações */}
        <div style={modalFooterStyle}>
          {!successResult ? (
            <>
              <Button 
                onClick={onClose} 
                disabled={loading} 
                style={{ backgroundColor: '#e2e8f0', color: '#475569', border: '1px solid #cbd5e1' }}
              >
                Cancelar
              </Button>
              <Button 
                onClick={handleImport} 
                disabled={!file || loading}
                style={{ backgroundColor: '#2563eb', color: '#ffffff' }}
              >
                {loading ? 'Importando...' : 'Iniciar Importação'}
              </Button>
            </>
          ) : (
            <Button onClick={handleProceedToProcess} style={{ backgroundColor: '#059669', color: '#ffffff', width: '100%' }}>
              Acessar Processo e Fluxo ➔
            </Button>
          )}
        </div>

      </div>
    </div>
  );
};

// Estilos CSS Inline Modernos e Premium (WOW aesthetics)
const modalOverlayStyle = {
  position: 'fixed',
  top: 0,
  left: 0,
  right: 0,
  bottom: 0,
  backgroundColor: 'rgba(15, 23, 42, 0.65)',
  backdropFilter: 'blur(8px)',
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
  zIndex: 9999,
  animation: 'fadeIn 0.25s ease-out',
};

const modalContentStyle = {
  backgroundColor: '#ffffff',
  borderRadius: '16px',
  width: '540px',
  maxWidth: '90%',
  boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
  display: 'flex',
  flexDirection: 'column',
  overflow: 'hidden',
  border: '1px solid #e2e8f0',
  animation: 'slideUp 0.3s cubic-bezier(0.16, 1, 0.3, 1)',
};

const modalHeaderStyle = {
  padding: '20px 24px',
  borderBottom: '1px solid #f1f5f9',
  display: 'flex',
  justifyContent: 'space-between',
  alignItems: 'center',
};

const modalTitleStyle = {
  margin: 0,
  fontSize: '18px',
  fontWeight: '600',
  color: '#0f172a',
};

const closeButtonStyle = {
  background: 'none',
  border: 'none',
  fontSize: '18px',
  cursor: 'pointer',
  color: '#64748b',
  padding: '4px',
  borderRadius: '4px',
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
  transition: 'background-color 0.2s',
  ':hover': {
    backgroundColor: '#f1f5f9',
  }
};

const modalBodyStyle = {
  padding: '24px',
  maxHeight: '450px',
  overflowY: 'auto',
};

const subtitleStyle = {
  margin: '0 0 20px 0',
  fontSize: '14px',
  lineHeight: '1.5',
  color: '#475569',
};

const dropZoneStyle = {
  border: '2px dashed #cbd5e1',
  borderRadius: '12px',
  padding: '32px 20px',
  textAlign: 'center',
  cursor: 'pointer',
  transition: 'all 0.2s ease-in-out',
  backgroundColor: '#f8fafc',
  ':hover': {
    borderColor: '#3b82f6',
    backgroundColor: '#eff6ff',
  }
};

const activeDropZoneStyle = {
  ...dropZoneStyle,
  border: '2px solid #3b82f6',
  backgroundColor: '#eff6ff',
};

const iconContainerStyle = {
  fontSize: '36px',
  marginBottom: '12px',
};

const dropZoneTextStyle = {
  margin: '0 0 6px 0',
  fontSize: '14px',
  fontWeight: '500',
  color: '#1e293b',
};

const dropZoneSubTextStyle = {
  margin: 0,
  fontSize: '12px',
  color: '#64748b',
};

const fileNameStyle = {
  margin: '0 0 4px 0',
  fontSize: '14px',
  fontWeight: '600',
  color: '#2563eb',
};

const fileSizeStyle = {
  margin: 0,
  fontSize: '12px',
  color: '#64748b',
};

const errorBannerStyle = {
  marginTop: '16px',
  padding: '12px',
  backgroundColor: '#fef2f2',
  border: '1px solid #fecaca',
  borderRadius: '8px',
  color: '#991b1b',
  fontSize: '13px',
};

const loadingContainerStyle = {
  marginTop: '20px',
  display: 'flex',
  alignItems: 'center',
  gap: '16px',
  padding: '16px',
  backgroundColor: '#f8fafc',
  borderRadius: '12px',
  border: '1px solid #e2e8f0',
};

const loadingTextStyle = {
  margin: 0,
  fontSize: '13px',
  fontWeight: '500',
  color: '#1e293b',
  lineHeight: '1.4',
};

const spinnerStyle = {
  width: '28px',
  height: '28px',
  border: '3px solid #cbd5e1',
  borderTop: '3px solid #2563eb',
  borderRadius: '50%',
  animation: 'spin 0.8s linear infinite',
};

const successBannerStyle = {
  padding: '12px 16px',
  backgroundColor: '#ecfdf5',
  border: '1px solid #a7f3d0',
  borderRadius: '8px',
  color: '#065f46',
  fontSize: '14px',
  textAlign: 'center',
  marginBottom: '20px',
};

const metricsGridStyle = {
  display: 'grid',
  gridTemplateColumns: '1fr 1fr',
  gap: '16px',
  marginBottom: '24px',
};

const metricCardStyle = {
  backgroundColor: '#f8fafc',
  border: '1px solid #e2e8f0',
  borderRadius: '12px',
  padding: '16px',
  textAlign: 'center',
};

const metricNumberStyle = {
  display: 'block',
  fontSize: '24px',
  fontWeight: '700',
  color: '#0f172a',
  marginBottom: '4px',
};

const metricLabelStyle = {
  fontSize: '12px',
  color: '#64748b',
};

const alertSectionStyle = {
  marginBottom: '20px',
  padding: '16px',
  backgroundColor: '#fffbeb',
  border: '1px solid #fef3c7',
  borderRadius: '12px',
};

const gapSectionStyle = {
  padding: '16px',
  backgroundColor: '#fafafa',
  border: '1px solid #e5e5e5',
  borderRadius: '12px',
};

const sectionTitleStyle = {
  margin: '0 0 8px 0',
  fontSize: '13px',
  fontWeight: '600',
  color: '#1e293b',
};

const gapSubtitleStyle = {
  margin: '0 0 12px 0',
  fontSize: '12px',
  color: '#475569',
  lineHeight: '1.4',
};

const gapListStyle = {
  margin: 0,
  paddingLeft: '20px',
  fontSize: '12px',
  color: '#334155',
  lineHeight: '1.6',
};

const gapItemStyle = {
  marginBottom: '6px',
};

const alertsListStyle = {
  display: 'flex',
  flexDirection: 'column',
  gap: '8px',
};

const alertItemStyle = {
  fontSize: '12px',
  color: '#334155',
  lineHeight: '1.4',
};

const noGapsStyle = {
  padding: '16px',
  backgroundColor: '#f0fdf4',
  border: '1px solid #bbf7d0',
  borderRadius: '12px',
  color: '#166534',
  fontSize: '13px',
  textAlign: 'center',
};

const modalFooterStyle = {
  padding: '16px 24px',
  borderTop: '1px solid #f1f5f9',
  display: 'flex',
  justifyContent: 'flex-end',
  gap: '12px',
};

// Injetar estilos de keyframe para animação de fade-in e spinner
if (typeof document !== 'undefined') {
  const style = document.createElement('style');
  style.innerHTML = `
    @keyframes spin {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }
  `;
  document.head.appendChild(style);
}

export default ImportProcessModal;
