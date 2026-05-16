# Changelog

## 0.7.0
- Realizada revisão técnica geral e validado checklist.
- Adicionado checklist de segurança e config de ambiente.
- Adicionado checklist de homologação ponta a ponta.
- Preparado backend para deploy via Railway.
- Preparado frontend para deploy via Railway.
- Configurado uso de SQLite com volume persistente.
- Documentado processo de deploy na Railway.
- Documentado teste de persistência pós-redeploy.
- Atualizado README final com instruções gerais.
- Criado roadmap e acceptance do MVP.

## 0.6.0
- Criados services do frontend para analisesApi e diretrizesApi.
- Criada tela de Análises (`Analises.jsx`) e Detalhe de Análise (`AnaliseDetalhe.jsx`).
- Criados múltiplos micro-componentes de visualização dos dados da Inteligência Artificial.
- Criada tela de Automações (`Automacoes.jsx`) com quadro gerencial.
- Implementado controle visual para atualização de status de automações.
- Atualizado `global.css` com sistema de badges do UI.
## 0.5.0
- Adicionada dependência OpenAI no backend.
- Criado system prompt especialista em processos contábeis.
- Criado template de user prompt para análise estruturada.
- Criado schema completo de resposta da IA.
- Implementado serviço de IA com modelo gpt-4o.
- Implementado endpoint de geração de análise IA.
- Implementada persistência de análise IA no SQLite.
- Implementada geração de diretrizes de automação.
- Implementados endpoints de listagem e atualização de diretrizes.
- Adicionados testes com mock para IA.

## 0.4.0
- Implementado editor visual de fluxo com React Flow.
- Criada rota /processos/:id/fluxo.
- Criados services de etapas e fluxo.
- Criado mapeamento entre API e React Flow.
- Criado node customizado de etapa.
- Criado painel lateral para criação e edição de etapas.
- Implementada conexão visual entre etapas.
- Implementada persistência de posições X/Y.
- Implementada persistência de conexões.
- Ativado botão Abrir fluxo visual na tela de detalhe do processo.
- Adicionados estados de loading, erro, vazio e sucesso no editor.

## 0.3.0
- Criado frontend React com Vite.
- Configurado React Router.
- Criado layout dashboard SaaS.
- Criado client de API com VITE_API_URL.
- Criado dashboard inicial.
- Criado catálogo de processos.
- Criado formulário de criação e edição de processos.
- Criada tela de detalhe do processo.
- Adicionados estados de loading, erro e vazio.

## 0.2.0
- Implementado CRUD de processos.
- Implementado CRUD de etapas.
- Implementada API de fluxo visual.
- Adicionados testes de processos, etapas e fluxo.

## [Unreleased] (Pacote 01)
- Inicialização do monorepo base
- Configuração do projeto FastAPI e estrutura modular do diretório
- Implementação dos modelos de banco de dados (SQLAlchemy) e schemas de validação (Pydantic)
- Inicialização da documentação base
