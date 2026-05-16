# QDT Processos Contábeis - Frontend

Camada de exibição React Vite para visualização SaaS da plataforma.

## Instalação e Execução
1. Acesse o diretório: `cd frontend`
2. Instale os pacotes: `npm install`
3. Copie o arquivo `.env.example` para `.env` e ajuste se necessário a `VITE_API_URL` apontando para o seu backend.
4. Rode em modo dev: `npm run dev`

## Rotas Principais
- `/` - Dashboard
- `/processos` - Catálogo Geral de Processos
- `/processos/:id` - Detalhe do Processo (Visão Geral)
- `/processos/:id/fluxo` - Editor React Flow do Fluxo Visual
- `/processos/:id/analises` - Visão Gerencial das avaliações geradas por IA
- `/processos/:id/automacoes` - Tabela/Quadro de acompanhamento das recomendações de automação

## Cuidados com Deploy Produção
Atenção ao realizar o deploy de aplicações React em roteamento client-side (SPA). Plataformas sem servidor web Nginx ou Caddy podem retornar `404 Not Found` caso o usuário acesse rotas como `/processos` diretamente ou recarregue a aba.
Siga os guias de fallback providenciados pelos pacotes (ex: na Railway, o uso do pacote global `serve` com a flag `-s dist`).
