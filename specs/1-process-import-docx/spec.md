# Especificação de Recurso: Importação Inteligente de Processo por Documento

**ID da Feature**: `1-process-import-docx`  
**Título**: Importação Inteligente de Processos Baseada em Documentos Operacionais  
**Autor**: Antigravity (AI Pair Programmer)  
**Status**: Em Revisão (Spec Ready)  
**Data**: 2026-05-23  

---

## 1. Contexto de Negócio e Valor para o Usuário

### 1.1 Objetivo
Atualmente, no sistema **QDT Processos Contábeis**, os usuários (analistas, gestores e consultores fiscais/contábeis) precisam cadastrar manualmente cada processo, detalhando suas etapas, entradas, saídas, sistemas utilizados, riscos e conexões lineares ou condicionais. Para procedimentos reais complexos — como a escrituração e transmissão do **SPED Fiscal EFD ICMS/IPI**, que contém dezenas de etapas, subetapas, regras de validação por filial e integrações —, esse processo de digitação manual gera alto esforço operacional, consome muito tempo e eleva o risco de omissões ou erros no mapeamento do fluxo.

Esta melhoria adiciona uma nova e inteligente porta de entrada ao sistema: a **Importação Inteligente de Processos**. O usuário poderá enviar um documento de procedimento operacional existente (como um arquivo `.docx`) e, através de Inteligência Artificial, o sistema fará a leitura, sanitização de segurança, interpretação e conversão desse arquivo em um cadastro de processo estruturado com suas respectivas etapas operacionais, conexões lógicas e identificação de lacunas de mapeamento.

### 1.2 Personas Envolvidas
*   **Gestores e Consultores Contábeis/Fiscais**: Responsáveis por padronizar as operações, identificar gargalos, auditar fluxos e propor melhorias de automação (RPA/IA). Eles possuem manuais de processos em formato texto ou editor de documentos e desejam acelerar a modelagem desses fluxos no canvas.

---

## 2. Cenários de Uso e Critérios de Aceite (Comportamento Esperado)

Os cenários a seguir descrevem a experiência do usuário de ponta a ponta e definem como o sistema deve reagir a interações típicas e atípicas.

### Cenário 1: Importação de Sucesso de Documento Operacional
*   **Dado** que o gestor de processos está na tela principal de listagem de processos (`/processos`).
*   **Quando** ele clica no botão **Importar processo com IA**, seleciona um arquivo válido no formato de documento de texto operacionais (`.docx`) que descreve o procedimento do SPED Fiscal e clica em **Iniciar Importação**.
*   **Então** o sistema exibe visualmente uma indicação de processamento ("*Interpretando documento com IA...*") e, em seguida, o redireciona automaticamente para a tela de visualização e edição do processo recém-criado.
*   **E** o processo é exibido no catálogo contendo:
    *   Informações gerais preenchidas (Nome, Descrição, Área, Criticidade, Sistemas Usados, etc.).
    *   Etapas operacionais dispostas e ordenadas sequencialmente no fluxo gráfico (React Flow) com posições adequadas para evitar sobreposição.
    *   Conexões de transição desenhadas de forma linear e conexões condicionais indicadas nas decisões do fluxo.

### Cenário 2: Tratamento de Lacunas e Alertas de Evidências Visuais
*   **Dado** que o documento `.docx` enviado possui screenshots embutidos ou menções textuais a fluxogramas visuais que a IA textual não consegue ler diretamente.
*   **Quando** a importação é processada com sucesso.
*   **Então** o processo é criado com alertas indicando lacunas específicas de mapeamento (ex: "*Imagem embutida não interpretada na etapa X*").
*   **E** a interface detalhada do processo exibe uma seção proeminente de alertas com as lacunas identificadas e perguntas recomendadas para que o usuário revise e preencha o fluxo manualmente antes de acionar a análise automatizada.

### Cenário 3: Proteção de Segurança e Sanitização de Credenciais
*   **Dado** que o documento operacional carregado possui dados confidenciais inseridos acidentalmente ou por instrução padrão (como senhas fictícias de sistemas, e-mails específicos, tokens de API ou nomes de usuários).
*   **Quando** o arquivo é processado pelo sistema.
*   **Então** o sistema deve remover ou mascarar esses elementos sensíveis antes que qualquer conteúdo seja registrado em logs permanentes ou enviado para a Inteligência Artificial.
*   **E** a resposta final da importação deve conter uma lista de alertas sensíveis sinalizando que dados foram higienizados e ocultados com sucesso por motivos de segurança.

### Cenário 4: Rejeição de Arquivo Inválido ou Corrompido
*   **Dado** que o usuário tenta selecionar e carregar um arquivo com extensão não permitida (ex: `.exe`, `.png`) ou um arquivo `.docx` corrompido ou vazio.
*   **Quando** ele solicita a importação.
*   **Então** o sistema rejeita o arquivo imediatamente, impede o upload e exibe uma mensagem de erro clara no modal (ex: "*O arquivo selecionado é inválido. Por favor, envie um documento .docx contendo texto extraível.*").
*   **E** nenhuma entidade ou registro parcial de processo é gravado no banco de dados.

---

## 3. Requisitos Funcionais (Testáveis e Agnósticos de Tecnologia)

### RF01: Ponto de Entrada da Importação
O sistema deve apresentar uma opção visual clara para importação por IA na tela de gerenciamento de processos, abrindo uma janela interativa de upload.

### RF02: Validação de Upload
O sistema deve validar os arquivos carregados nos seguintes aspectos:
*   **Extensão permitida**: Aceitar prioritariamente o formato de documento de texto padrão de mercado (`.docx`).
*   **Tamanho máximo**: Limitar o arquivo para evitar estouro de memória ou timeouts no servidor.
*   **Conteúdo mínimo**: Exigir que o arquivo contenha texto extraível relevante.

### RF03: Sanitização de Dados Sensíveis
O sistema deve escanear o texto e mascarar automaticamente credenciais de login, senhas explícitas, chaves secretas ou tokens, gerando um registro descritivo dos itens removidos sem expor o valor original.

### RF04: Interpretação de Processos por Inteligência Artificial
O motor de análise deve converter o texto sanitizado do documento em uma estrutura compreensível pelo sistema, identificando:
*   **Metadados do Processo**: Nome, área de atuação, descrição geral, objetivo de negócio, responsável, periodicidade e nível de criticidade fiscal.
*   **Etapas**: Nome do passo, descrição das atividades, insumos necessários (entradas), resultados (saídas), sistemas envolvidos, tempo de execução e tipo de atividade (Manual, Decisão, Validação, etc.).
*   **Conexões**: Fluxo sequencial entre as etapas e caminhos lógicos com base em critérios condicionais.
*   **Lacunas de Mapeamento**: Áreas com baixa confiança de extração, ambiguidades no texto ou presença de imagens e mídias não processadas.

### RF05: Gravação Transacional
A gravação do processo e de todas as suas dependências (etapas, conexões e lacunas) deve ser atômica. Se qualquer etapa ou conexão falhar ao ser inserida, nenhuma informação parcial do processo deve persistir no banco de dados.

### RF06: Posicionamento Inteligente das Etapas
Para que o fluxo de trabalho seja utilizável imediatamente na interface gráfica, as etapas importadas devem receber coordenadas bidimensionais organizadas de forma lógica e sequencial (por exemplo, em grade ou linha horizontal), evitando que fiquem sobrepostas no canvas do diagrama.

### RF07: Fluxo de Revisão e Análise Existente
O processo importado deve ser totalmente compatível com as funcionalidades de visualização, edição manual e geração de diagnósticos de IA já funcionais no sistema. A análise automática de maturidade e geração de diretrizes contidas no MVP atual só deve rodar após o usuário revisar a importação.

---

## 4. Requisitos Não Funcionais e Restrições de Escopo

### RNF01: Preservação de Tecnologia e Arquitetura
A melhoria não deve exigir alterações nas tecnologias estruturais do sistema atual (monorepo, banco de dados leve local, serviços baseados em camadas, bibliotecas de interface). A nova rota deve complementar o fluxo existente sem substituir os CRUDs manuais de processos.

### RNF02: Privacidade de Dados e Higiene de Logs
O texto integral do documento extraído ou enviado à IA nunca deve ser armazenado permanentemente no banco de dados nem ser escrito em logs de auditoria ou servidor. Os logs devem conter exclusivamente metadados operacionais (como tamanho do arquivo, número de etapas geradas, status da requisição e identificadores).

### RNF03: Robustez em Falhas da IA
Se a Inteligência Artificial retornar uma resposta estruturada fora do padrão técnico esperado, o sistema deve registrar a falha, cancelar a persistência temporária através de rollback da transação e alertar o usuário sem expor detalhes técnicos internos de depuração.

---

## 5. Conceitos Lógicos e Entidades do Domínio

A importação baseia-se em conceitos estruturais que mapeiam as informações do documento para o modelo lógico da aplicação.

### 5.1 Processo Importado
A entidade principal que representa o fluxo de trabalho capturado.
*   **Nome**: Título do procedimento operacional (ex: "Geração do SPED Fiscal").
*   **Área**: Classificação departamental (ex: "Fiscal").
*   **Objetivo**: Razão de existência do fluxo de trabalho.
*   **Responsável**: Cargo, equipe ou papel encarregado pela execução geral do processo.
*   **Periodicidade**: Frequência de execução (Mensal, Diário, etc.).
*   **Criticidade**: Classificação de risco/impacto para a organização.

### 5.2 Etapa de Processo
Os passos individuais extraídos ordenadamente do manual de procedimentos.
*   **Ordem**: Indicador sequencial de execução (1, 2, 3...).
*   **Nome**: Título curto da atividade.
*   **Descrição**: O detalhamento de como a atividade é executada.
*   **Tipo**: Classificação funcional da atividade (Validação, Decisão, Operação Manual, etc.).
*   **Sistemas**: Softwares ou ferramentas de suporte utilizados no passo.
*   **Entrada/Saída**: Arquivos, planilhas ou informações de insumo e produto.
*   **Nível de Confiança**: Avaliação da IA sobre a clareza desse passo no documento.

### 5.3 Conexão Lógica
A representação das setas direcionais e decisões lógicas entre as etapas.
*   **Origem e Destino**: Definição de qual etapa antecede e qual sucede.
*   **Tipo de Conexão**: Define se é a transição padrão (sequencial) ou condicional baseada em validações (ex: sucesso, falha ou condicional).
*   **Condição**: Critério textual que rege a transição (ex: "Se Cajamar, gerar Registro 1100").

### 5.4 Lacuna de Mapeamento
Identificação de pontos ambíguos ou incompletos no documento carregado.
*   **Campo ou Tema**: Qual informação ficou faltante ou com baixa clareza.
*   **Descrição**: O motivo do aviso (ex: "Presença de screenshot não interpretado na página 12").
*   **Pergunta Recomendada**: Uma sugestão de pergunta para auxiliar o usuário a complementar a informação de forma manual.

---

## 6. Critérios de Sucesso (Tecnologicamente Agnósticos)

Para que esta funcionalidade seja declarada um sucesso comercial e técnico, as seguintes métricas devem ser atingíveis:

1.  **Redução de Tempo de Cadastro**: O usuário deve conseguir cadastrar e modelar um processo longo com mais de 20 etapas (como o exemplo do SPED Fiscal) em menos de **3 minutos** no total (incluindo tempo de upload e processamento), comparado ao tempo médio estimado de **30 minutos** para digitação manual campo a campo.
2.  **Taxa de Sucesso na Extração**: Pelo menos **85% das etapas descritas textualmente** no documento operacional carregado devem ser mapeadas de forma legível e correta na primeira tentativa.
3.  **Mascaramento de Dados**: **100% das senhas e credenciais explícitas** presentes no documento original não devem ser gravadas na base de dados ou enviadas em texto aberto à Inteligência Artificial.
4.  **Consistência Gráfica**: **100% das etapas criadas automaticamente** devem aparecer de forma legível no canvas visual do diagrama sem sobreposição inicial.
5.  **Gravação Transacional**: Em caso de erros de processamento ou formatação durante a importação, o banco de dados não deve conter nenhum registro residual ou incompleto do processo.

---

## 7. Premissas e Comportamentos Padrão (Assumptions)

1.  **Regra de Área Inferida**: Se o documento operacional contiver palavras-chave fiscais comuns (como *ICMS, IPI, SPED, EFD, Contábil, Livro Fiscal*), mas o documento não declarar explicitamente o campo de área, o sistema definirá a área do processo como **"Fiscal"** de forma padrão.
2.  **Criticidade Fiscal Padrão**: Se a criticidade não puder ser extraída diretamente, ela será inferida como **"Alta"** caso o texto contenha menções a multas, prazos oficiais, transmissão governamental ou uso de assinaturas e certificados digitais.
3.  **Conexões Lineares por Padrão**: Se a IA não conseguir identificar critérios específicos de caminhos lógicos ou ramificações, ela estabelecerá conexões lineares simples do início ao fim (Etapa 1 -> Etapa 2 -> Etapa 3...) seguindo a ordem de numeração das etapas extraídas.
4.  **Imagens e Prints de Tela**: Como a primeira versão possui restrições técnicas para OCR pesado ou interpretação visual complexa de imagens, todas as imagens detectadas nos parágrafos do arquivo serão mapeadas como avisos de "Lacunas de Mapeamento", alertando o usuário sobre a necessidade de revisão daquele ponto específico.
5.  **Uso de IA no Pipeline**: Assume-se que o serviço de IA para estruturar os dados continuará operando sob o modelo `gpt-4o` da OpenAI configurado no sistema atual do cliente.

---

## 8. Clarificações Pendentes (Clarifications)

Abaixo estão listadas as questões de negócio e escopo refinadas.

### Pergunta 1: Comportamento das Lacunas de Mapeamento na Análise Existente
**Contexto**: O PRD menciona no item 8.2 que se houver lacunas e prints não interpretados, um alerta será exibido na interface detalhada do processo para que o usuário revise.
**O que precisamos saber**: A presença de lacunas ou baixa confiança em etapas deve bloquear o usuário de rodar a funcionalidade de análise operacional e diretrizes de IA já existente no MVP, ou apenas funcionar como alerta recomendável?

**Sugestão de Respostas**:

| Opção | Resposta | Implicações |
| :--- | :--- | :--- |
| **A (Recomendado)** | **Apenas Alerta Visual** | O usuário visualiza o alerta de lacunas, mas pode rodar a análise de IA existente quando desejar. Promove maior flexibilidade e evita bloqueios rígidos. |
| **B** | **Bloqueio até Revisão** | O botão de análise de IA existente fica desabilitado até que o usuário marque todas as lacunas identificadas como "Resolvidas" ou faça uma edição manual. Garante dados mais limpos, mas reduz a usabilidade. |
| **Custom** | Fornecer resposta customizada | Explicar como deseja que o fluxo de bloqueio ocorra. |

**Escolha do Usuário**: _[Aguardando resposta do utilizador ou preenchida com a opção A como premissa padrão de usabilidade rápida]_
