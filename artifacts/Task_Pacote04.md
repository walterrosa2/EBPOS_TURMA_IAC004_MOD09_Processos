# Checklist - Pacote 04

- [x] React Flow instalado corretamente via NPM.
- [x] Rota dinâmica de fluxo `/processos/:id/fluxo` implementada e mapeada no React Router (`App.jsx`).
- [x] O botão "Abrir fluxo visual" liberado no layout de detalhe (`ProcessoDetalhe.jsx`).
- [x] Tela de editor carrega o fluxo completo puxando dados da API.
- [x] Etapas de banco de dados são traduzidas em formato de Custom Node visual (`EtapaNode.jsx`).
- [x] O node customizado incorpora layout SaaS com meta-dados em Badges.
- [x] O usuário possui acesso ao painel direito lateral para criar e editar propriedades do Node (`EtapaPanel.jsx`).
- [x] A criação de uma nova etapa reflete instantaneamente no canvas.
- [x] A edição de uma etapa (clique em node já existente) reflete nos dados após salva.
- [x] O usuário pode destruir (excluir) um Node livremente do layout.
- [x] A interação arrastar (Drag-and-Drop) cria vínculos entre blocos de Etapa sem duplicidade abusiva.
- [x] É possível remover um vínculo indesejado.
- [x] O Botão de "Salvar Fluxo" varre a tela submetendo posições (X, Y) e os Vínculos de conexões (`Edges`) de volta para FastAPI (`salvarFluxo`).
- [x] A tela recarrega a si mesma reconstruindo o último fluxo congelado perfeitamente.
- [x] Nenhum erro descontrolado ocorre. O sistema blinda o Canvas com `ErrorState` e carrega transições com `LoadingState`.
- [x] Nenhum Fetch puritano está rodando internamente aos visuais. O service consome via `.env` a API unificada em `VITE_API_URL`.
- [x] Os documentos do repositório (`backlog`, `changelog` e `tests`) receberam o *stamp* da versão 0.4.0 validando a entrega para o tracking.
