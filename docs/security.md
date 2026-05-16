# Checklist de Segurança - MVP

## Configurações Gerais
- [x] O arquivo `.env` está inserido no `.gitignore`.
- [x] Nenhuma chave sensível (como `OPENAI_API_KEY`) foi commitada no código-fonte.
- [x] Os arquivos `.env.example` foram revisados e contêm apenas placeholders ou valores seguros.

## CORS e Comunicação
- [x] O `CORS_ORIGINS` no backend está configurado para não permitir domínios curinga (`*`) no ambiente de produção. As origens são listadas estritamente via variável.
- [x] O frontend consome dinamicamente a `VITE_API_URL` sem exposição de URLs expostas em código (hardcoded).

## Operações e Logs
- [x] Logs da aplicação não imprimem o conteúdo do payload de respostas extensas da IA.
- [x] A chave de API da OpenAI só existe no escopo do backend e não é acessível publicamente via endpoints ou no build client-side.

## Armazenamento
- [x] O banco de dados SQLite está configurado para usar um caminho em volume persistente (`/app/data`) em ambiente produtivo, prevenindo deleção não intencional durante redeploys do container Railway.
