# Testes

## Backend
- Endpoint base de health funcionando com status 200 OK
- Tabelas SQLite sendo criadas no inicialização
- API de processos validada.
- API de etapas validada.
- API de fluxo validada.
- Validação de conexões entre etapas implementada.
- Schema da análise IA validado.
- JSON inválido da IA rejeitado.
- Processo sem etapas bloqueia análise.
- Processo inexistente retorna 404.
- Análise IA mockada gera registro no banco.
- Diretrizes são geradas após análise.
- Status de diretriz pode ser atualizado.
- Testes não chamam OpenAI real.
- Demais cenários conforme documentado no `prd.md` e nos pacotes de entrega.

## Frontend
- Dashboard validado.
- Catálogo de processos validado.
- Criação de processo validada.
- Edição de processo validada.
- Exclusão de processo validada.
- Detalhe do processo validado.
- Erro de API validado.

## Fluxo (React Flow)
- Editor visual validado.
- Criação de etapa pelo canvas validada.
- Edição de etapa pelo painel lateral validada.
- Exclusão de etapa validada.
- Conexão entre etapas validada.
- Persistência de posição X/Y validada.
- Persistência de conexões validada.
- Estado vazio do editor validado.
- Erro de API no editor validado.
