# TASKS.md — Implementação da Importação Inteligente de Processo Mapeado

## 1. Contexto da tarefa

Implementar a melhoria **Importação Inteligente de Processo Mapeado por Documento** no sistema QDT Processos Contábeis.

A funcionalidade deve permitir que o usuário envie um documento `.docx`, como o exemplo de SPED Fiscal EFD ICMS/IPI, e que a IA converta o conteúdo em processo, etapas e conexões compatíveis com a aplicação atual.

A implementação deve manter a estrutura técnica atual:
- Backend FastAPI/Python.
- Frontend React/Vite.
- SQLite/SQLAlchemy.
- Pydantic.
- OpenAI `gpt-4o`.
- React Flow.
- Organização em rotas, services, repositories, schemas e prompts.

---

## 2. Decisões técnicas desta entrega

| ID | Decisão | Justificativa |
|---|---|---|
| DT01 | Priorizar suporte a `.docx`. | O anexo real de validação está em DOCX. |
| DT02 | Não persistir arquivo original. | Evita alteração no modelo de dados nesta iteração. |
| DT03 | Criar endpoint novo `POST /api/processos/importar`. | Não altera endpoints existentes. |
| DT04 | Usar Pydantic para validar resposta da IA. | Mantém padrão atual de structured output. |
| DT05 | Criar processo, etapas e conexões em transação única. | Evita cadastro parcial. |
| DT06 | Sanitizar credenciais antes de logs/persistência. | O documento de exemplo contém dados sensíveis. |
| DT07 | Detectar imagens embutidas e registrar lacunas. | O DOCX possui muitos prints; OCR completo fica fora da v1. |
| DT08 | Reaproveitar repositories existentes. | Reduz duplicidade e preserva arquitetura. |
| DT09 | Posicionar etapas automaticamente em grade. | Garante visualização inicial no React Flow. |
| DT10 | Não acionar automaticamente a análise de IA existente após importação. | Usuário deve revisar antes de analisar. |

---

## 3. Backlog de implementação

### Épico 1 — Backend: rota de importação

| ID | Tarefa | Arquivos | Prioridade | Critério de aceite |
|---|---|---|---|---|
| T01 | Criar rota `importacao_processos.py`. | `backend/app/api/routes/importacao_processos.py` | Alta | [X] Arquivo criado com router FastAPI. |
| T02 | Registrar router no app principal. | `backend/app/main.py` | Alta | [X] Endpoint aparece em `/docs`. |
| T03 | Implementar endpoint `POST /api/processos/importar`. | `importacao_processos.py` | Alta | [X] Endpoint recebe `UploadFile` via multipart. |
| T04 | Validar extensão `.docx`. | `importacao_processos.py` | Alta | [X] Arquivo não permitido retorna 400. |
| T05 | Validar tamanho máximo do arquivo. | `importacao_processos.py` | Alta | [X] Arquivo acima do limite retorna 413 ou 400 controlado. |
| T06 | Validar arquivo vazio. | `importacao_processos.py` | Alta | [X] Upload vazio retorna erro claro. |

### Épico 2 — Backend: leitura documental

| ID | Tarefa | Arquivos | Prioridade | Critério de aceite |
|---|---|---|---|---|
| T07 | Adicionar dependência `python-docx`, se ainda não existir. | `backend/requirements.txt` | Alta | [X] Backend instala dependência sem erro. |
| T08 | Criar serviço de leitura documental. | `backend/app/services/document_reader_service.py` | Alta | [X] Serviço expõe função para ler DOCX. |
| T09 | Extrair parágrafos em ordem. | `document_reader_service.py` | Alta | [X] Texto do DOCX é extraído preservando seções. |
| T10 | Extrair metadados do arquivo. | `document_reader_service.py` | Média | [X] Retorna nome, extensão, tamanho, número de parágrafos e caracteres. |
| T11 | Detectar imagens embutidas. | `document_reader_service.py` | Alta | [X] Retorna contagem de imagens ou lista de referências internas. |
| T12 | Tratar DOCX corrompido. | `document_reader_service.py` | Alta | [X] Erro controlado sem stack trace no frontend. |
| T13 | Implementar limite mínimo de texto. | `document_reader_service.py` | Alta | [X] Documento sem texto suficiente retorna erro. |

### Épico 3 — Backend: sanitização

| ID | Tarefa | Arquivos | Prioridade | Critério de aceite |
|---|---|---|---|---|
| T14 | Criar serviço de sanitização. | `backend/app/services/document_sanitizer_service.py` | Alta | [X] Serviço criado e testável isoladamente. |
| T15 | Mascarar/remover padrões de senha. | `document_sanitizer_service.py` | Crítica | [X] `Senha:` e similares não aparecem no output. |
| T16 | Mascarar/remover padrões de usuário/login. | `document_sanitizer_service.py` | Alta | [X] Credenciais não são persistidas. |
| T17 | Mascarar e-mails sensíveis quando não necessários. | `document_sanitizer_service.py` | Média | [X] E-mails são removidos ou mascarados conforme regra. |
| T18 | Retornar alertas de dados sensíveis. | `document_sanitizer_service.py` | Alta | [X] Serviço informa quantidade/tipo de itens removidos. |
| T19 | Garantir que logs não recebam texto integral. | Rotas/services | Crítica | [X] Logs mostram apenas metadados e IDs. |

### Épico 4 — Backend: schemas Pydantic

| ID | Tarefa | Arquivos | Prioridade | Critério de aceite |
|---|---|---|---|---|
| T20 | Criar schema de processo importado. | `backend/app/schemas/importacao_processo_schema.py` | Alta | [X] Classe Pydantic criada. |
| T21 | Criar schema de etapa importada. | `importacao_processo_schema.py` | Alta | [X] Etapa exige `ordem`, `nome`, `descricao`. |
| T22 | Criar schema de conexão importada. | `importacao_processo_schema.py` | Alta | [X] Conexão valida origem/destino por ordem. |
| T23 | Criar schema de lacunas. | `importacao_processo_schema.py` | Média | [X] Lacunas têm tema, descrição e pergunta recomendada. |
| T24 | Criar schema de alertas sensíveis. | `importacao_processo_schema.py` | Alta | [X] Alertas registram tipo e ação aplicada. |
| T25 | Criar schema de response da API. | `importacao_processo_schema.py` | Alta | [X] Endpoint retorna formato estável ao frontend. |
| T26 | Validar valores permitidos para `tipo_etapa`. | `importacao_processo_schema.py` | Média | [X] Valores fora do enum são rejeitados ou normalizados. |

### Épico 5 — Backend: prompts de IA

| ID | Tarefa | Arquivos | Prioridade | Critério de aceite |
|---|---|---|---|---|
| T27 | Criar system prompt importador. | `backend/app/prompts/system_process_importer.md` | Alta | [X] Prompt define papel de especialista fiscal/processos. |
| T28 | Criar user prompt template. | `backend/app/prompts/user_process_import_template.md` | Alta | [X] Template recebe texto sanitizado e metadados. |
| T29 | Instruir IA a não retornar credenciais. | Prompts | Crítica | [X] Prompt contém regra explícita de segurança. |
| T30 | Instruir IA a gerar JSON estrito. | Prompts | Alta | [X] Prompt contém schema esperado. |
| T31 | Instruir IA a criar lacunas para imagens não interpretadas. | Prompts | Alta | [X] Prompt trata prints e campos visuais como lacunas. |
| T32 | Instruir IA a gerar etapas compatíveis com o modelo atual. | Prompts | Alta | [X] Campos retornados correspondem a processos/etapas/conexões. |

### Épico 6 — Backend: serviço de IA de importação

| ID | Tarefa | Arquivos | Prioridade | Critério de aceite |
|---|---|---|---|---|
| T33 | Criar serviço `process_import_ia_service.py`. | `backend/app/services/process_import_ia_service.py` | Alta | [X] Serviço invoca OpenAI reaproveitando padrão atual. |
| T34 | Carregar prompts de importação. | `process_import_ia_service.py` | Alta | [X] Serviço lê arquivos em `/prompts`. |
| T35 | Montar payload para IA. | `process_import_ia_service.py` | Alta | [X] Payload includes texto sanitizado, metadados e instruções. |
| T36 | Processar resposta JSON. | `process_import_ia_service.py` | Alta | [X] JSON é convertido para schema Pydantic. |
| T37 | Tratar JSON inválido. | `process_import_ia_service.py` | Alta | [X] Erro controlado, sem persistência. |
| T38 | Tratar timeout/erro OpenAI. | `process_import_ia_service.py` | Alta | [X] API retorna erro compreensível. |
| T39 | Implementar retry único opcional para JSON inválido. | `process_import_ia_service.py` | Média | [X] Retry não duplica gravação. |

### Épico 7 — Backend: persistência da importação

| ID | Tarefa | Arquivos | Prioridade | Critério de aceite |
|---|---|---|---|---|
| T40 | Criar orquestrador `process_import_service.py`. | `backend/app/services/process_import_service.py` | Alta | [X] Serviço coordena leitura, sanitização, IA e persistência. |
| T41 | Reaproveitar repository de processo. | `process_import_service.py` | Alta | [X] Processo é criado por camada de persistência atual. |
| T42 | Reaproveitar repository de etapas. | `process_import_service.py` | Alta | [X] Etapas são criadas vinculadas ao processo. |
| T43 | Reaproveitar repository de conexões. | `process_import_service.py` | Alta | [X] Conexões são criadas quando aplicável. |
| T44 | Implementar transação única. | `process_import_service.py` | Crítica | [X] Falha executa rollback. |
| T45 | Converter `ordem` em posições X/Y. | `process_import_service.py` | Alta | [X] Etapas aparecem organizadas no React Flow. |
| T46 | Criar conexões sequenciais padrão. | `process_import_service.py` | Alta | [X] Etapas conectadas por ordem quando IA não retornar conexões. |
| T47 | Gravar lacunas em `observacoes`. | `process_import_service.py` | Média | [X] Processo indica que precisa revisão. |
| T48 | Não gravar conteúdo integral do documento. | `process_import_service.py` | Crítica | [X] Banco não contém texto integral nem credenciais. |

### Épico 8 — Frontend: client API

| ID | Tarefa | Arquivos | Prioridade | Critério de aceite |
|---|---|---|---|---|
| T49 | Criar service de importação. | `frontend/src/services/processosImportApi.js` | Alta | [X] Função envia multipart/form-data. |
| T50 | Tratar resposta de sucesso. | `processosImportApi.js` | Alta | [X] Retorna `processo_id` e metadados. |
| T51 | Tratar erro do backend. | `processosImportApi.js` | Alta | [X] Erro exibe mensagem amigável. |

### Épico 9 — Frontend: modal de upload

| ID | Tarefa | Arquivos | Prioridade | Critério de aceite |
|---|---|---|---|---|
| T52 | Criar componente `ImportProcessModal`. | `frontend/src/components/ImportProcessModal.jsx` | Alta | [X] Modal abre/fecha corretamente. |
| T53 | Implementar input de arquivo. | `ImportProcessModal.jsx` | Alta | [X] Usuário seleciona `.docx`. |
| T54 | Validar extensão no frontend. | `ImportProcessModal.jsx` | Média | [X] Arquivo inválido bloqueado antes do envio. |
| T55 | Exibir nome e tamanho do arquivo. | `ImportProcessModal.jsx` | Média | [X] Usuário vê o arquivo selecionado. |
| T56 | Exibir estado de carregamento. | `ImportProcessModal.jsx` | Alta | [X] Mensagem “Interpretando documento com IA...” aparece. |
| T57 | Exibir erros de importação. | `ImportProcessModal.jsx` | Alta | [X] Erros do backend são compreensíveis. |
| T58 | Exibir lacunas após sucesso, se aplicável. | `ImportProcessModal.jsx` | Média | [X] Usuário entende necessidade de revisão. |

### Épico 10 — Frontend: tela de processos

| ID | Tarefa | Arquivos | Prioridade | Critério de aceite |
|---|---|---|---|---|
| T59 | Adicionar botão **Importar processo com IA**. | `frontend/src/pages/Processos.jsx` | Alta | [X] Botão visível na tela de processos. |
| T60 | Integrar modal ao botão. | `Processos.jsx` | Alta | [X] Clique abre modal. |
| T61 | Redirecionar após sucesso. | `Processos.jsx` | Alta | [X] Navega para `/processos/{id}`. |
| T62 | Atualizar lista após importação, se não redirecionar. | `Processos.jsx` | Baixa | [X] Lista reflete processo novo. |


### Épico 11 — Validação com o anexo SPED

| ID | Tarefa | Arquivos | Prioridade | Critério de aceite |
|---|---|---|---|---|
| T63 | Testar importação do arquivo `sped fiscal exemplo.docx`. | Manual/backend tests | Alta | Processo criado com nome relacionado a SPED Fiscal. |
| T64 | Validar campos do processo criado. | Manual/backend tests | Alta | Área Fiscal, criticidade Alta e periodicidade Mensal quando inferidas. |
| T65 | Validar extração de etapas principais. | Manual/backend tests | Alta | Pelo menos 15 etapas relevantes são criadas. |
| T66 | Validar presença de etapas de PVA, transmissão e Auditor IOB. | Manual/backend tests | Alta | Etapas finais do processo são mapeadas. |
| T67 | Validar lacunas sobre imagens embutidas. | Manual/backend tests | Alta | Sistema informa imagens/prints como lacuna se não interpretadas. |
| T68 | Validar remoção de credenciais. | Manual/backend tests | Crítica | Usuários/senhas do documento não aparecem no banco ou UI. |

### Épico 12 — Testes automatizados backend

| ID | Tarefa | Arquivos | Prioridade | Critério de aceite |
|---|---|---|---|---|
| T69 | Testar endpoint com arquivo válido mockado. | `backend/tests/test_importacao_processos.py` | Alta | [X] Retorna 200/201 e cria processo. |
| T70 | Testar arquivo inválido. | `test_importacao_processos.py` | Alta | [X] Retorna 400. |
| T71 | Testar arquivo vazio. | `test_importacao_processos.py` | Alta | [X] Retorna erro controlado. |
| T72 | Testar DOCX sem texto. | `test_importacao_processos.py` | Alta | [X] Retorna erro controlado. |
| T73 | Testar sanitização de senha. | `backend/tests/test_document_sanitizer_service.py` | Crítica | [X] Senha é removida/mascarada. |
| T74 | Testar JSON inválido da IA. | `backend/tests/test_process_import_ia_service.py` | Alta | [X] Não cria dados. |
| T75 | Testar rollback de persistência. | `backend/tests/test_process_import_service.py` | Crítica | [X] Falha no meio desfaz gravação. |
| T76 | Testar geração de posições X/Y. | `test_process_import_service.py` | Média | [X] Etapas recebem coordenadas. |

### Épico 13 — Testes frontend

| ID | Tarefa | Arquivos | Prioridade | Critério de aceite |
|---|---|---|---|---|
| T77 | Testar abertura do modal. | Teste manual ou componente | Média | [X] Botão abre modal. |
| T78 | Testar seleção de DOCX. | Teste manual ou componente | Média | [X] Arquivo aparece no modal. |
| T79 | Testar loading. | Teste manual ou componente | Média | [X] Estado visual impede duplo envio. |
| T80 | Testar erro. | Teste manual ou componente | Média | [X] Mensagem exibida. |
| T81 | Testar redirecionamento. | Teste manual ou componente | Alta | [X] Vai para detalhe do processo criado. |

---

## 4. Ordem recomendada de execução

1. T07 — Dependência `python-docx`.
2. T08 a T13 — Leitura documental.
3. T14 a T19 — Sanitização.
4. T20 a T26 — Schemas Pydantic.
5. T27 a T32 — Prompts.
6. T33 a T39 — Serviço IA.
7. T40 a T48 — Persistência transacional.
8. T01 a T06 — Endpoint e router.
9. T49 a T51 — API frontend.
10. T52 a T58 — Modal.
11. T59 a T62 — Tela de processos.
12. T63 a T68 — Homologação com anexo SPED.
13. T69 a T81 — Testes automatizados e manuais.

---

## 5. Especificação dos arquivos a criar

### 5.1 `backend/app/api/routes/importacao_processos.py`

Responsabilidades:
- Receber `UploadFile`.
- Validar extensão e tamanho.
- Chamar `ProcessImportService`.
- Retornar response schema.
- Não logar conteúdo do arquivo.

### 5.2 `backend/app/services/document_reader_service.py`

Responsabilidades:
- Ler `.docx`.
- Extrair parágrafos.
- Detectar imagens embutidas.
- Retornar texto e metadados.
- Tratar erros de arquivo inválido.

Interface esperada:

```python
class DocumentReaderService:
    def read_docx(self, file_bytes: bytes, filename: str) -> DocumentReadResult:
        ...
```

### 5.3 `backend/app/services/document_sanitizer_service.py`

Responsabilidades:
- Remover ou mascarar credenciais.
- Retornar texto sanitizado.
- Retornar alertas sensíveis.

Interface esperada:

```python
class DocumentSanitizerService:
    def sanitize(self, text: str) -> SanitizedDocument:
        ...
```

### 5.4 `backend/app/services/process_import_ia_service.py`

Responsabilidades:
- Carregar prompts.
- Montar chamada ao modelo.
- Solicitar JSON estruturado.
- Validar retorno com Pydantic.
- Tratar timeout e JSON inválido.

### 5.5 `backend/app/services/process_import_service.py`

Responsabilidades:
- Orquestrar leitura, sanitização, IA e persistência.
- Criar processo, etapas e conexões.
- Calcular posições X/Y.
- Fazer rollback em falhas.
- Retornar resumo ao endpoint.

### 5.6 `backend/app/schemas/importacao_processo_schema.py`

Schemas mínimos:
- `ImportedProcessSchema`
- `ImportedStepSchema`
- `ImportedConnectionSchema`
- `ImportGapSchema`
- `SensitiveAlertSchema`
- `ProcessImportAIResultSchema`
- `ProcessImportResponseSchema`

### 5.7 `frontend/src/services/processosImportApi.js`

Responsabilidades:
- Enviar arquivo como `multipart/form-data`.
- Retornar dados da importação.
- Tratar erros HTTP.

### 5.8 `frontend/src/components/ImportProcessModal.jsx`

Responsabilidades:
- Modal com input de arquivo.
- Botões cancelar/importar.
- Loading.
- Erros.
- Mensagens de sucesso/lacunas.

---

## 6. Prompt técnico para o agente de código

Use este bloco diretamente na IDE agentic.

```markdown
# Implementar Importação Inteligente de Processo por DOCX

## Contexto
O sistema QDT Processos Contábeis já possui backend FastAPI/Python, frontend React/Vite, SQLite/SQLAlchemy, schemas Pydantic, prompts de IA e integração com OpenAI gpt-4o. A aplicação já permite cadastrar processos, etapas, conexões, editar o fluxo no React Flow e gerar análise de IA.

## Objetivo
Adicionar a funcionalidade de importação de processo mapeado via upload de documento DOCX. O documento deve ser lido, sanitizado, interpretado por IA e convertido em cadastro automático de processo, etapas e conexões.

## Restrições obrigatórias
- Não alterar a stack principal.
- Não substituir endpoints existentes.
- Não alterar o fluxo atual de análise de IA.
- Não criar tabela obrigatória de documentos nesta entrega.
- Não persistir o arquivo original.
- Não logar o conteúdo integral do documento.
- Não persistir credenciais, senhas, usuários ou tokens extraídos do documento.
- Usar transação para evitar gravação parcial.
- Reaproveitar repositories e padrões existentes.

## Backend — criar
- backend/app/api/routes/importacao_processos.py
- backend/app/schemas/importacao_processo_schema.py
- backend/app/services/document_reader_service.py
- backend/app/services/document_sanitizer_service.py
- backend/app/services/process_import_ia_service.py
- backend/app/services/process_import_service.py
- backend/app/prompts/system_process_importer.md
- backend/app/prompts/user_process_import_template.md

## Backend — alterar
- backend/app/main.py
- backend/requirements.txt, se `python-docx` ainda não estiver instalado

## Frontend — criar
- frontend/src/services/processosImportApi.js
- frontend/src/components/ImportProcessModal.jsx

## Frontend — alterar
- frontend/src/pages/Processos.jsx

## Endpoint esperado
POST /api/processos/importar

## Entrada
multipart/form-data:
- file: arquivo .docx

## Saída esperada
- processo_id
- mensagem
- nome_processo
- etapas_criadas
- conexoes_criadas
- lacunas_identificadas
- alertas_sensiveis

## Critérios de aceite principais
- Upload DOCX funciona.
- Arquivo inválido é rejeitado.
- Texto do DOCX é extraído.
- Credenciais são removidas ou mascaradas.
- IA retorna JSON validado por Pydantic.
- Processo, etapas e conexões são criados em transação.
- Etapas aparecem no React Flow com posições X/Y.
- Processo importado pode seguir para a análise de IA já existente.
```

---

## 7. Plano de testes

### Cenário 1 — Importação válida do SPED Fiscal

- Dado: arquivo `sped fiscal exemplo.docx`.
- Quando: usuário importa o documento.
- Então: processo fiscal é criado com múltiplas etapas relevantes.
- Tipo: integração/manual.
- Resultado esperado: processo aparece no catálogo e pode ser aberto.

### Cenário 2 — Detecção de etapas principais

- Dado: arquivo de SPED Fiscal.
- Quando: IA interpreta o documento.
- Então: etapas como reprocessamento ICMS/IPI, Bloco G, Bloco K, PVA, transmissão e Auditor IOB aparecem.
- Tipo: aceitação.
- Resultado esperado: pelo menos 15 etapas úteis são criadas.

### Cenário 3 — Sanitização de credenciais

- Dado: documento contendo campos de usuário/senha.
- Quando: backend sanitiza o texto.
- Então: credenciais não aparecem no banco, logs ou frontend.
- Tipo: segurança.
- Resultado esperado: alertas sensíveis informam remoção.

### Cenário 4 — Arquivo inválido

- Dado: arquivo `.exe` ou `.png`.
- Quando: usuário tenta importar.
- Então: API retorna 400.
- Tipo: API.
- Resultado esperado: nenhum processo criado.

### Cenário 5 — DOCX sem texto extraível

- Dado: documento vazio ou apenas com imagens.
- Quando: backend tenta extrair texto.
- Então: retorna erro ou lacuna indicando necessidade de OCR/multimodal.
- Tipo: API.
- Resultado esperado: nenhum processo parcial criado.

### Cenário 6 — JSON inválido da IA

- Dado: mock da IA retornando JSON inválido.
- Quando: serviço valida resposta.
- Então: erro controlado e rollback.
- Tipo: unitário/integração.
- Resultado esperado: banco permanece inalterado.

### Cenário 7 — Falha ao criar etapa

- Dado: processo criado em memória/transação.
- Quando: criação de etapa falha.
- Então: processo também é removido/rollback.
- Tipo: integração.
- Resultado esperado: sem cadastro parcial.

### Cenário 8 — Continuidade do pipeline atual

- Dado: processo importado.
- Quando: usuário executa análise de IA existente.
- Então: análise e diretrizes são geradas normalmente.
- Tipo: ponta a ponta.
- Resultado esperado: pipeline atual permanece funcional.

---

## 8. Checklist de homologação

- [ ] Botão aparece em `/processos`.
- [ ] Modal abre corretamente.
- [ ] Upload `.docx` funciona.
- [ ] Upload inválido é bloqueado.
- [ ] Backend extrai texto.
- [ ] Backend detecta imagens embutidas.
- [ ] Backend sanitiza credenciais.
- [ ] IA retorna JSON válido.
- [ ] Processo é criado.
- [ ] Etapas são criadas.
- [ ] Conexões são criadas.
- [ ] Etapas aparecem no React Flow.
- [ ] Lacunas aparecem para revisão.
- [ ] Nenhuma senha aparece na UI.
- [ ] Nenhum conteúdo sensível aparece nos logs.
- [ ] Análise de IA existente funciona após importação.
- [ ] Diretrizes de automação continuam sendo geradas.
- [ ] Teste com `sped fiscal exemplo.docx` aprovado.

---

## 9. Riscos técnicos e mitigação

| Risco | Severidade | Mitigação |
|---|---|---|
| Credenciais vazarem em logs ou banco | Crítica | Sanitizador obrigatório antes de IA/persistência/logs. |
| IA gerar etapas inventadas | Alta | Prompt exige evidência e confiança por etapa. |
| DOCX com muitos prints perder informação | Alta | Detectar imagens e criar lacunas; evoluir para multimodal/OCR depois. |
| JSON inválido da IA | Alta | Pydantic, retry controlado e erro sem persistência. |
| Processo parcial no banco | Crítica | Transação única e rollback. |
| Documento muito grande | Média | Limite de tamanho + chunking futuro. |
| Frontend permitir duplo envio | Média | Desabilitar botão durante loading. |
| Etapas ficarem sobrepostas no canvas | Média | Layout em grade por ordem. |

---

## 10. Definição de pronto

A tarefa será considerada pronta quando:

1. O usuário conseguir importar o DOCX de exemplo.
2. O sistema criar processo e etapas automaticamente.
3. O processo importado aparecer no catálogo.
4. O fluxo visual abrir com as etapas posicionadas.
5. As lacunas forem exibidas ou registradas.
6. Nenhuma credencial do documento for exposta.
7. A análise de IA existente puder ser executada no processo importado.
8. Os testes críticos de backend passarem.
9. A implementação não alterar a stack nem quebrar funcionalidades existentes.
