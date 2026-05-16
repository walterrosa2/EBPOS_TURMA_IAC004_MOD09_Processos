Regras obrigatórias
Não implementar frontend.
Não implementar IA.
Não implementar autenticação.
Não salvar secrets no código.
Não criar regras específicas de uma única área contábil.
Não colocar regra de negócio diretamente nas rotas.
Rotas devem chamar services.
Services devem chamar repositories.
Repositories devem concentrar acesso ao banco.
Usar schemas Pydantic para entrada e saída.
Retornar erro 404 quando recurso não existir.
Retornar erro 400 para regra de negócio inválida.
Retornar erro 422 para payload inválido via Pydantic.
Não deixar conexões órfãs ao excluir etapa.
Não permitir conexão entre etapas de processos diferentes.
Não permitir fluxo para processo inexistente.
Atualizar /docs/backlog.md e /docs/changelog.md ao final.
Garantir que todos os testes criados passem com pytest.
Estrutura esperada após este pacote
backend/
  app/
    api/
      routes/
        __init__.py
        processos.py
        etapas.py
        fluxos.py

    repositories/
      __init__.py
      processo_repository.py
      etapa_repository.py
      conexao_repository.py

    services/
      __init__.py
      processo_service.py
      etapa_service.py
      fluxo_service.py

    schemas/
      processo_schema.py
      etapa_schema.py
      fluxo_schema.py

    main.py

  tests/
    test_health.py
    test_processos.py
    test_etapas.py
    test_fluxo.py
TASK-020 — CRUD de Processos
Objetivo

Implementar API completa para criação, listagem, filtro, busca, atualização e exclusão de processos.

Arquivos impactados
backend/app/api/routes/processos.py
backend/app/repositories/processo_repository.py
backend/app/services/processo_service.py
backend/app/schemas/processo_schema.py
backend/app/main.py
backend/tests/test_processos.py
docs/backlog.md
docs/changelog.md
Endpoints obrigatórios
GET    /api/processos
POST   /api/processos
GET    /api/processos/{processo_id}
PUT    /api/processos/{processo_id}
DELETE /api/processos/{processo_id}
Campos de Processo

O processo deve usar os campos já definidos no modelo:

id
nome
area
descricao
objetivo
responsavel
periodicidade
criticidade
status
sistemas_utilizados
documentos_utilizados
observacoes
created_at
updated_at
Validações
Obrigatórias
nome: obrigatório no create
area: obrigatório no create
Recomendadas
nome não pode ser string vazia
area não pode ser string vazia
criticidade, quando informada, deve aceitar: Baixa, Média, Alta
status, quando informado, deve aceitar: Rascunho, Mapeado, Em análise, Analisado, Em melhoria
periodicidade, quando informada, deve aceitar: Diário, Semanal, Quinzenal, Mensal, Trimestral, Anual, Sob demanda
Filtros no endpoint GET /api/processos

O endpoint deve aceitar query params opcionais:

area
criticidade
status
q

Comportamento:

area: filtra por área exata
criticidade: filtra por criticidade exata
status: filtra por status exato
q: busca textual simples por nome ou descrição

Exemplo:

GET /api/processos?area=Fiscal&criticidade=Alta&q=fechamento
Regras de negócio
RN01 — Um processo deve ter nome e área obrigatórios.
RN10 — O sistema não deve depender de área específica.
Repository

Criar processo_repository.py com funções claras, por exemplo:

list_processos(db, filters)
get_processo_by_id(db, processo_id)
create_processo(db, data)
update_processo(db, processo, data)
delete_processo(db, processo)

Regras:

Repository não deve levantar erro HTTP.
Repository deve trabalhar com SQLAlchemy e retornar objetos ou None.
Filtros devem ser aplicados de forma simples e legível.
Service

Criar processo_service.py com funções que aplicam regra de negócio:

listar_processos(db, filters)
obter_processo(db, processo_id)
criar_processo(db, payload)
atualizar_processo(db, processo_id, payload)
excluir_processo(db, processo_id)

Regras:

Service pode levantar HTTPException.
Processo inexistente deve retornar 404.
Exclusão de processo deve permitir cascade para etapas, conexões, análises e diretrizes se configurado nos models.
Route

Criar processos.py com APIRouter.

Prefixo:

/api/processos

Tags:

processos

Registrar router em main.py.

Critérios de aceite
Dado que envio POST /api/processos com nome e área,
quando o payload for válido,
então a API deve criar o processo e retornar status 201 ou 200 com o objeto criado.

Dado que envio POST /api/processos sem nome,
quando o payload for validado,
então a API deve retornar erro 422.

Dado que envio POST /api/processos sem área,
quando o payload for validado,
então a API deve retornar erro 422.

Dado que existem processos cadastrados,
quando envio GET /api/processos,
então a API deve retornar uma lista.

Dado que existe um processo com ID válido,
quando envio GET /api/processos/{id},
então a API deve retornar os dados do processo.

Dado que não existe processo com ID informado,
quando envio GET /api/processos/{id},
então a API deve retornar 404.

Dado que existe um processo,
quando envio PUT /api/processos/{id},
então a API deve atualizar os campos enviados.

Dado que existe um processo,
quando envio DELETE /api/processos/{id},
então a API deve excluir o processo.

Dado que existem processos de áreas diferentes,
quando filtro por área,
então a API deve retornar apenas processos daquela área.
Testes obrigatórios

Criar backend/tests/test_processos.py com:

test_create_processo_success
test_create_processo_without_nome_returns_422
test_create_processo_without_area_returns_422
test_list_processos
test_get_processo_by_id
test_get_processo_not_found_returns_404
test_update_processo
test_delete_processo
test_filter_processos_by_area
TASK-021 — CRUD de Etapas
Objetivo

Implementar API completa para criação, listagem, atualização e exclusão de etapas vinculadas a processos.

Arquivos impactados
backend/app/api/routes/etapas.py
backend/app/repositories/etapa_repository.py
backend/app/repositories/conexao_repository.py
backend/app/services/etapa_service.py
backend/app/schemas/etapa_schema.py
backend/app/main.py
backend/tests/test_etapas.py
docs/backlog.md
docs/changelog.md
Endpoints obrigatórios
GET    /api/processos/{processo_id}/etapas
POST   /api/processos/{processo_id}/etapas
PUT    /api/etapas/{etapa_id}
DELETE /api/etapas/{etapa_id}
Campos de Etapa
id
processo_id
nome
descricao
responsavel
entrada
saida
sistema_utilizado
tempo_estimado
tipo_etapa
risco
gargalo
oportunidade_automacao
posicao_x
posicao_y
created_at
updated_at
Validações
Obrigatórias
nome: obrigatório no create
processo_id: deve existir
Recomendadas
nome não pode ser string vazia
posicao_x e posicao_y devem aceitar número ou null
Regras de negócio
RN02 — Uma etapa deve ter nome obrigatório.
RN03 — Toda etapa deve pertencer a um processo existente.
Repository

Criar etapa_repository.py com:

list_etapas_by_processo(db, processo_id)
get_etapa_by_id(db, etapa_id)
create_etapa(db, processo_id, data)
update_etapa(db, etapa, data)
delete_etapa(db, etapa)

Criar ou complementar conexao_repository.py com:

delete_conexoes_by_etapa(db, etapa_id)
Service

Criar etapa_service.py com:

listar_etapas(db, processo_id)
criar_etapa(db, processo_id, payload)
atualizar_etapa(db, etapa_id, payload)
excluir_etapa(db, etapa_id)

Regras:

Antes de criar etapa, verificar se o processo existe.
Se processo não existir, retornar 404.
Se etapa não existir, retornar 404.
Ao excluir etapa, remover conexões onde ela aparece como origem ou destino.
Não deixar conexões órfãs.
Route

Criar etapas.py com APIRouter.

Rotas:

/api/processos/{processo_id}/etapas
/api/etapas/{etapa_id}

Registrar router em main.py.

Critérios de aceite
Dado que existe um processo,
quando envio POST /api/processos/{processo_id}/etapas com nome válido,
então a etapa deve ser criada vinculada ao processo.

Dado que o processo não existe,
quando tento criar etapa,
então a API deve retornar 404.

Dado que envio etapa sem nome,
quando o payload for validado,
então a API deve retornar 422.

Dado que existem etapas em um processo,
quando envio GET /api/processos/{processo_id}/etapas,
então a API deve retornar apenas etapas daquele processo.

Dado que uma etapa existe,
quando envio PUT /api/etapas/{id},
então os campos enviados devem ser atualizados.

Dado que uma etapa existe,
quando envio DELETE /api/etapas/{id},
então a etapa deve ser excluída.

Dado que uma etapa excluída tinha conexões,
quando buscar fluxo do processo,
então essas conexões não devem aparecer.
Testes obrigatórios

Criar backend/tests/test_etapas.py com:

test_create_etapa_success
test_create_etapa_without_nome_returns_422
test_create_etapa_for_invalid_processo_returns_404
test_list_etapas_by_processo
test_update_etapa
test_delete_etapa
test_delete_etapa_removes_related_conexoes
TASK-022 — API de Fluxo Visual
Objetivo

Criar API para recuperar e salvar o fluxo visual completo de um processo.

Esta API será usada futuramente pelo React Flow.

Arquivos impactados
backend/app/api/routes/fluxos.py
backend/app/repositories/conexao_repository.py
backend/app/repositories/etapa_repository.py
backend/app/services/fluxo_service.py
backend/app/schemas/fluxo_schema.py
backend/app/main.py
backend/tests/test_fluxo.py
docs/backlog.md
docs/changelog.md
Endpoints obrigatórios
GET /api/processos/{processo_id}/fluxo
PUT /api/processos/{processo_id}/fluxo
GET /api/processos/{processo_id}/fluxo
Objetivo

Retornar todas as etapas e conexões de um processo.

Resposta esperada
{
  "processo_id": 1,
  "etapas": [
    {
      "id": 1,
      "processo_id": 1,
      "nome": "Receber documentos",
      "descricao": "Receber documentos do cliente",
      "responsavel": "Analista",
      "entrada": "Documentos do cliente",
      "saida": "Documentos recebidos",
      "sistema_utilizado": "Portal",
      "tempo_estimado": "2 horas",
      "tipo_etapa": "Entrada de informação",
      "risco": "Atraso no envio",
      "gargalo": "Documentos incompletos",
      "oportunidade_automacao": "Checklist automático",
      "posicao_x": 120,
      "posicao_y": 80,
      "created_at": "2026-01-01T00:00:00",
      "updated_at": "2026-01-01T00:00:00"
    }
  ],
  "conexoes": [
    {
      "id": 1,
      "processo_id": 1,
      "etapa_origem_id": 1,
      "etapa_destino_id": 2,
      "tipo_conexao": "sequencial",
      "condicao": null,
      "created_at": "2026-01-01T00:00:00"
    }
  ]
}
PUT /api/processos/{processo_id}/fluxo
Objetivo

Salvar layout visual e conexões do processo.

Payload esperado
{
  "etapas": [
    {
      "id": 1,
      "posicao_x": 120,
      "posicao_y": 80
    },
    {
      "id": 2,
      "posicao_x": 420,
      "posicao_y": 80
    }
  ],
  "conexoes": [
    {
      "etapa_origem_id": 1,
      "etapa_destino_id": 2,
      "tipo_conexao": "sequencial",
      "condicao": null
    }
  ]
}
Comportamento esperado
1. Verificar se o processo existe.
2. Validar se todas as etapas do payload pertencem ao processo.
3. Atualizar posições X/Y das etapas informadas.
4. Validar se todas as conexões ligam etapas do mesmo processo.
5. Substituir conexões atuais do processo pelas conexões recebidas.
6. Retornar fluxo completo atualizado.
Regras de negócio
RN04 — Toda conexão deve ligar duas etapas do mesmo processo.
RN05 — O processo precisa ter ao menos uma etapa para ser analisado pela IA, mas essa regra será usada no pacote de IA, não aqui.
Repository

Criar ou complementar conexao_repository.py com:

list_conexoes_by_processo(db, processo_id)
delete_conexoes_by_processo(db, processo_id)
create_conexao(db, processo_id, data)

Complementar etapa_repository.py com:

update_etapa_position(db, etapa, posicao_x, posicao_y)
list_etapas_by_ids(db, ids)
Service

Criar fluxo_service.py com:

obter_fluxo(db, processo_id)
salvar_fluxo(db, processo_id, payload)

Regras:

Se processo não existir, retornar 404.
Se alguma etapa não pertencer ao processo, retornar 400.
Se origem ou destino de conexão não existir, retornar 400.
Se origem ou destino pertencer a outro processo, retornar 400.
Ao salvar fluxo, substituir conexões anteriores do processo.
Retornar fluxo atualizado.
Route

Criar fluxos.py com APIRouter.

Prefixo sugerido:

/api/processos/{processo_id}/fluxo

Registrar router em main.py.

Critérios de aceite
Dado que existe um processo com etapas,
quando envio GET /api/processos/{processo_id}/fluxo,
então a API deve retornar etapas e conexões do processo.

Dado que o processo não existe,
quando envio GET /api/processos/{processo_id}/fluxo,
então a API deve retornar 404.

Dado que envio PUT /api/processos/{processo_id}/fluxo com posições X/Y,
quando o payload for válido,
então as posições devem ser salvas.

Dado que envio PUT /api/processos/{processo_id}/fluxo com conexão válida,
quando salvar,
então a conexão deve ser persistida.

Dado que uma conexão aponta para etapa de outro processo,
quando salvar fluxo,
então a API deve retornar 400.

Dado que salvo o fluxo e depois faço GET,
quando recuperar o fluxo,
então as posições e conexões devem ser iguais às salvas.
Testes obrigatórios

Criar backend/tests/test_fluxo.py com:

test_get_fluxo_success
test_get_fluxo_invalid_processo_returns_404
test_save_fluxo_positions_success
test_save_fluxo_connection_success
test_save_fluxo_with_etapa_from_other_processo_returns_400
test_save_fluxo_then_get_returns_persisted_data
Registro de Rotas no main.py

O arquivo backend/app/main.py deve registrar:

processos router
etapas router
fluxos router

Exemplo conceitual:

/api/processos
/api/processos/{processo_id}/etapas
/api/etapas/{etapa_id}
/api/processos/{processo_id}/fluxo

Não remover /health.

Tratamento de Erros

Usar respostas consistentes:

404
{
  "detail": "Processo não encontrado."
}

ou

{
  "detail": "Etapa não encontrada."
}
400
{
  "detail": "Conexão inválida: as etapas devem pertencer ao mesmo processo."
}
422

Deixar FastAPI/Pydantic retornar o erro padrão de validação.

Testes do Pacote 02
Rodar todos os testes
cd backend
pytest
Testes mínimos esperados
test_health.py
test_processos.py
test_etapas.py
test_fluxo.py
Critérios de aceite dos testes
Todos os testes devem passar.
Testes não devem depender de dados manuais criados previamente.
Testes devem criar seus próprios registros.
Testes não devem usar OpenAI.
Testes não devem exigir frontend.
Comandos de validação manual
Subir backend
cd backend
uvicorn app.main:app --reload
Health
curl http://localhost:8000/health
Criar processo
curl -X POST http://localhost:8000/api/processos \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Processo de Teste",
    "area": "Fiscal",
    "descricao": "Processo usado para validação da API",
    "criticidade": "Alta",
    "status": "Rascunho"
  }'
Listar processos
curl http://localhost:8000/api/processos
Criar etapa
curl -X POST http://localhost:8000/api/processos/1/etapas \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Receber documentos",
    "descricao": "Receber documentos enviados pelo cliente",
    "responsavel": "Analista",
    "entrada": "Documentos do cliente",
    "saida": "Documentos recebidos",
    "posicao_x": 120,
    "posicao_y": 80
  }'
Obter fluxo
curl http://localhost:8000/api/processos/1/fluxo
Salvar fluxo
curl -X PUT http://localhost:8000/api/processos/1/fluxo \
  -H "Content-Type: application/json" \
  -d '{
    "etapas": [
      {
        "id": 1,
        "posicao_x": 120,
        "posicao_y": 80
      },
      {
        "id": 2,
        "posicao_x": 420,
        "posicao_y": 80
      }
    ],
    "conexoes": [
      {
        "etapa_origem_id": 1,
        "etapa_destino_id": 2,
        "tipo_conexao": "sequencial",
        "condicao": null
      }
    ]
  }'
Atualização obrigatória da documentação

Ao final do pacote, atualizar:

docs/backlog.md

Marcar como concluídas:

TASK-020 — CRUD de processos
TASK-021 — CRUD de etapas
TASK-022 — API de fluxo visual
docs/changelog.md

Adicionar:

## 0.2.0

- Implementado CRUD de processos.
- Implementado CRUD de etapas.
- Implementada API de fluxo visual.
- Adicionados testes de processos, etapas e fluxo.
docs/tests.md

Adicionar resultados esperados dos testes:

- API de processos validada.
- API de etapas validada.
- API de fluxo validada.
- Validação de conexões entre etapas implementada.
Definition of Done do Pacote 02

A entrega só estará concluída quando:

[ ] Endpoints de processos implementados.
[ ] Endpoints de etapas implementados.
[ ] Endpoints de fluxo implementados.
[ ] Rotas registradas em main.py.
[ ] Repositories criados.
[ ] Services criados.
[ ] Regras de negócio fora das rotas.
[ ] Processo sem nome retorna 422.
[ ] Processo sem área retorna 422.
[ ] Etapa sem nome retorna 422.
[ ] Processo inexistente retorna 404.
[ ] Etapa inexistente retorna 404.
[ ] Conexão entre processos diferentes retorna 400.
[ ] Exclusão de etapa remove conexões relacionadas.
[ ] Fluxo salva posições X/Y.
[ ] Fluxo salva conexões.
[ ] Fluxo é reconstruído após GET.
[ ] Testes de API passam.
[ ] Documentação atualizada.
[ ] Nenhuma chave ou segredo foi versionado.
Restrições

Não implemente neste pacote:

React
React Flow
Dashboard frontend
OpenAI
ia_service.py
system_process_mapper.md
Análise IA
Diretrizes de automação
Railway deploy
Login
Upload de arquivos
Exportação PDF
Resultado esperado

Ao final deste pacote, o backend deve estar pronto para ser consumido pelo frontend.

O próximo pacote será:

Pacote 03 — Frontend Base + Layout SaaS + Catálogo de Processos

Ele deverá implementar:

React + Vite
React Router
Layout com sidebar/header
Client de API
Dashboard inicial
Catálogo de processos
Formulário de criação/edição
Tela de detalhe do processo

---

# Checklist de Revisão após o Antigravity executar

Use este checklist antes de avançar:

```text
1. O backend continua subindo sem erro?
2. /health continua funcionando?
3. GET /api/processos retorna lista?
4. POST /api/processos cria processo?
5. POST /api/processos sem nome retorna 422?
6. POST /api/processos sem área retorna 422?
7. GET /api/processos/{id} inexistente retorna 404?
8. POST /api/processos/{id}/etapas cria etapa?
9. Criar etapa para processo inexistente retorna 404?
10. DELETE de etapa remove conexões relacionadas?
11. GET /api/processos/{id}/fluxo retorna etapas e conexões?
12. PUT /api/processos/{id}/fluxo salva posições X/Y?
13. PUT /api/processos/{id}/fluxo bloqueia etapa de outro processo?
14. pytest passa?
15. docs/backlog.md foi atualizado?
16. docs/changelog.md foi atualizado?