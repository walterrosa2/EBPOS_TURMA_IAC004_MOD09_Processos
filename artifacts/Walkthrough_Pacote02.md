# Walkthrough - Pacote 02

## O que foi feito
A implementação da primeira API funcional do sistema **QDT Processos Contábeis** foi concluída com sucesso. O pacote cobre todo o CRUD de Processos, Etapas e o gerenciamento visual do fluxo.
1. **Repository Pattern e Services**: Todas as operações de banco foram abstraídas nos repositórios (`processo_repository.py`, `etapa_repository.py`, `conexao_repository.py`). As regras de negócio e lançamentos de erro HTTP foram delegadas para as camadas de serviço (`processo_service.py`, `etapa_service.py`, `fluxo_service.py`).
2. **Rotas (FastAPI)**:
    - `/api/processos`: Criar, listar (com filtro textual, área, criticidade e status), obter por ID, editar e excluir.
    - `/api/processos/{processo_id}/etapas`: Criar e listar as etapas referentes ao processo. E para edição/exclusão: `/api/etapas/{etapa_id}`.
    - `/api/processos/{processo_id}/fluxo`: Rota GET/PUT para recuperar ou salvar as conexões e o posicionamento X/Y do layout visual.
3. **Cascatas e Integridade**: Na exclusão de etapas, as conexões atreladas a ela são limpadas automaticamente. A inserção de fluxo também recria e valida para que conexões entre etapas de processos diferentes sejam bloqueadas (erro 400).
4. **Testes Unitários Integrados (Pytest)**: As três suítes `test_processos.py`, `test_etapas.py` e `test_fluxo.py` estão passando com sucesso (100% dos cenários do Pacote).
5. **Documentação de Versão**: Os arquivos `docs/backlog.md`, `docs/changelog.md` (Versão 0.2.0) e `docs/tests.md` foram devidamente atualizados.

## Onde no código
- Arquivos de Rotas criados e registrados em `backend/app/main.py`:
  - `backend/app/api/routes/processos.py`
  - `backend/app/api/routes/etapas.py`
  - `backend/app/api/routes/fluxos.py`
- Regras de negócio e Repositories criados nos diretórios correspondentes (`backend/app/services` e `backend/app/repositories`).
- Bateria de Testes Unitários em `backend/tests/`.

## Como validar
1. Certifique-se de estar com a virtual environment (venv) ativada.
2. Execute a suíte de testes com o comando:
   ```bash
   cd backend
   pytest
   ```
3. Suba a aplicação com:
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```
4. Siga os comandos manuais `curl` descritos no doc `tasks_02.md` ou verifique as transações de API pelo navegador com a interface do Swagger disponível em `http://localhost:8000/docs`.
