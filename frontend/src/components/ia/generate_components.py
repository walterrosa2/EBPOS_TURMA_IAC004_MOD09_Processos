import os

path = "g:/Meu Drive/Backup_HD_Walter/PROJETO_EBPOS_IAC004_MOD09/frontend/src/components/ia/"
os.makedirs(path, exist_ok=True)

files = {
"GargalosList.jsx": """import React from 'react';
import Card from '../common/Card';
import { safeList, getImpactoVariant } from '../../utils/analysisFormatters';

const GargalosList = ({ gargalos }) => {
  const lista = safeList(gargalos);
  if (lista.length === 0) return null;

  return (
    <Card>
      <h3 style={{ fontSize: '1.25rem', marginBottom: '16px' }}>Gargalos Identificados</h3>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        {lista.map((item, i) => (
          <div key={i} style={{ padding: '16px', border: '1px solid var(--color-border)', borderRadius: '8px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
              <h4 style={{ fontWeight: '600' }}>{item.titulo || item}</h4>
              {item.impacto && (
                <span className={`badge badge-${getImpactoVariant(item.impacto)}`}>Impacto: {item.impacto}</span>
              )}
            </div>
            {item.descricao && <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginBottom: '8px' }}>{item.descricao}</p>}
            {item.etapa_relacionada && <p style={{ fontSize: '0.85rem', color: 'var(--color-primary)' }}>Etapa: {item.etapa_relacionada}</p>}
          </div>
        ))}
      </div>
    </Card>
  );
};
export default GargalosList;
""",
"RiscosList.jsx": """import React from 'react';
import Card from '../common/Card';
import { safeList, getSeveridadeVariant } from '../../utils/analysisFormatters';

const RiscosList = ({ riscos }) => {
  const lista = safeList(riscos);
  if (lista.length === 0) return null;

  return (
    <Card>
      <h3 style={{ fontSize: '1.25rem', marginBottom: '16px' }}>Riscos Identificados</h3>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        {lista.map((item, i) => (
          <div key={i} style={{ padding: '16px', border: '1px solid var(--color-border)', borderRadius: '8px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
              <h4 style={{ fontWeight: '600' }}>{item.titulo || item}</h4>
              {item.severidade && (
                <span className={`badge badge-${getSeveridadeVariant(item.severidade)}`}>Severidade: {item.severidade}</span>
              )}
            </div>
            {item.descricao && <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginBottom: '8px' }}>{item.descricao}</p>}
            {item.tipo && <p style={{ fontSize: '0.85rem' }}>Tipo: <strong>{item.tipo}</strong></p>}
            {item.mitigacao && <p style={{ fontSize: '0.85rem', color: 'var(--color-success)', marginTop: '8px' }}>Mitigação: {item.mitigacao}</p>}
          </div>
        ))}
      </div>
    </Card>
  );
};
export default RiscosList;
""",
"MelhoriasList.jsx": """import React from 'react';
import Card from '../common/Card';
import { safeList, getImpactoVariant } from '../../utils/analysisFormatters';

const MelhoriasList = ({ melhorias }) => {
  const lista = safeList(melhorias);
  if (lista.length === 0) return null;

  return (
    <Card>
      <h3 style={{ fontSize: '1.25rem', marginBottom: '16px' }}>Sugestões de Melhoria</h3>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        {lista.map((item, i) => (
          <div key={i} style={{ padding: '16px', border: '1px solid var(--color-border)', borderRadius: '8px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
              <h4 style={{ fontWeight: '600' }}>{item.titulo || item}</h4>
              {item.impacto && (
                <span className={`badge badge-${getImpactoVariant(item.impacto)}`}>Impacto: {item.impacto}</span>
              )}
            </div>
            {item.descricao && <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>{item.descricao}</p>}
          </div>
        ))}
      </div>
    </Card>
  );
};
export default MelhoriasList;
""",
"AutomacoesList.jsx": """import React from 'react';
import Card from '../common/Card';
import { safeList, getPrioridadeVariant, getImpactoVariant } from '../../utils/analysisFormatters';

const AutomacoesList = ({ automacoes }) => {
  const lista = safeList(automacoes);
  if (lista.length === 0) return null;

  return (
    <Card>
      <h3 style={{ fontSize: '1.25rem', marginBottom: '16px' }}>Sugestões de Automação</h3>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        {lista.map((item, i) => (
          <div key={i} style={{ padding: '16px', border: '1px solid var(--color-border)', borderRadius: '8px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
              <h4 style={{ fontWeight: '600', color: 'var(--color-primary)' }}>{item.titulo || item}</h4>
              <div style={{ display: 'flex', gap: '8px' }}>
                {item.prioridade && <span className={`badge badge-${getPrioridadeVariant(item.prioridade)}`}>{item.prioridade}</span>}
                {item.impacto && <span className={`badge badge-${getImpactoVariant(item.impacto)}`}>Impacto {item.impacto}</span>}
              </div>
            </div>
            {item.descricao && <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginBottom: '8px' }}>{item.descricao}</p>}
            {item.esforco && <p style={{ fontSize: '0.85rem' }}>Esforço: <strong>{item.esforco}</strong></p>}
            {item.pre_requisitos && item.pre_requisitos.length > 0 && (
              <div style={{ marginTop: '8px', fontSize: '0.85rem', padding: '8px', backgroundColor: 'var(--bg-secondary)', borderRadius: '4px' }}>
                <strong>Pré-requisitos:</strong> {item.pre_requisitos.join(', ')}
              </div>
            )}
          </div>
        ))}
      </div>
    </Card>
  );
};
export default AutomacoesList;
""",
"OportunidadesIAList.jsx": """import React from 'react';
import Card from '../common/Card';
import { safeList } from '../../utils/analysisFormatters';

const OportunidadesIAList = ({ oportunidades }) => {
  const lista = safeList(oportunidades);
  if (lista.length === 0) return null;

  return (
    <Card>
      <h3 style={{ fontSize: '1.25rem', marginBottom: '16px', color: '#6366f1' }}>✨ Oportunidades de Inteligência Artificial</h3>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        {lista.map((item, i) => (
          <div key={i} style={{ padding: '16px', border: '1px solid #c7d2fe', backgroundColor: '#f5f7ff', borderRadius: '8px' }}>
            <h4 style={{ fontWeight: '600', marginBottom: '8px' }}>{item.titulo || item}</h4>
            {item.descricao && <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>{item.descricao}</p>}
            {item.beneficio_esperado && <p style={{ fontSize: '0.85rem', color: '#4338ca', marginTop: '8px' }}>Benefício: {item.beneficio_esperado}</p>}
          </div>
        ))}
      </div>
    </Card>
  );
};
export default OportunidadesIAList;
""",
"LacunasList.jsx": """import React from 'react';
import Card from '../common/Card';
import { safeList } from '../../utils/analysisFormatters';

const LacunasList = ({ lacunas }) => {
  const lista = safeList(lacunas);
  if (lista.length === 0) return null;

  return (
    <Card>
      <h3 style={{ fontSize: '1.25rem', marginBottom: '16px' }}>Lacunas no Mapeamento</h3>
      <ul style={{ paddingLeft: '20px', display: 'flex', flexDirection: 'column', gap: '8px', color: 'var(--text-secondary)' }}>
        {lista.map((item, i) => (
          <li key={i}>{typeof item === 'string' ? item : item.descricao || item.titulo}</li>
        ))}
      </ul>
    </Card>
  );
};
export default LacunasList;
""",
"IndicadoresList.jsx": """import React from 'react';
import Card from '../common/Card';
import { safeList } from '../../utils/analysisFormatters';

const IndicadoresList = ({ indicadores }) => {
  const lista = safeList(indicadores);
  if (lista.length === 0) return null;

  return (
    <Card>
      <h3 style={{ fontSize: '1.25rem', marginBottom: '16px' }}>Indicadores Recomendados (KPIs)</h3>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(250px, 1fr))', gap: '16px' }}>
        {lista.map((item, i) => (
          <div key={i} style={{ padding: '12px', border: '1px solid var(--color-border)', borderRadius: '8px', backgroundColor: 'var(--bg-secondary)' }}>
            <h4 style={{ fontWeight: '600', fontSize: '0.95rem', marginBottom: '4px' }}>{item.nome || item}</h4>
            {item.descricao && <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>{item.descricao}</p>}
            {item.formula && <code style={{ display: 'block', marginTop: '8px', fontSize: '0.75rem', padding: '4px', backgroundColor: '#e2e8f0', borderRadius: '4px' }}>{item.formula}</code>}
          </div>
        ))}
      </div>
    </Card>
  );
};
export default IndicadoresList;
""",
"PerguntasList.jsx": """import React from 'react';
import Card from '../common/Card';
import { safeList } from '../../utils/analysisFormatters';

const PerguntasList = ({ perguntas }) => {
  const lista = safeList(perguntas);
  if (lista.length === 0) return null;

  return (
    <Card>
      <h3 style={{ fontSize: '1.25rem', marginBottom: '16px' }}>Perguntas para Aprofundamento</h3>
      <ul style={{ paddingLeft: '20px', display: 'flex', flexDirection: 'column', gap: '12px', color: 'var(--text-primary)' }}>
        {lista.map((item, i) => (
          <li key={i}>{item}</li>
        ))}
      </ul>
    </Card>
  );
};
export default PerguntasList;
""",
"AlertasList.jsx": """import React from 'react';
import { safeList } from '../../utils/analysisFormatters';

const AlertasList = ({ alertas }) => {
  const lista = safeList(alertas);
  if (lista.length === 0) return null;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', marginBottom: '24px' }}>
      {lista.map((item, i) => (
        <div key={i} style={{ padding: '16px', backgroundColor: '#fef2f2', borderLeft: '4px solid #ef4444', borderRadius: '4px', color: '#991b1b' }}>
          <strong>Aviso Importante:</strong> {item}
        </div>
      ))}
    </div>
  );
};
export default AlertasList;
"""
}

for k, v in files.items():
    with open(path+k, "w", encoding="utf-8") as f:
        f.write(v)
