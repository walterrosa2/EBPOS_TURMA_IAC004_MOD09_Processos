from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app
from app.schemas.importacao_processo_schema import (
    ProcessImportAIResultSchema, ImportedProcessSchema, 
    ImportedStepSchema, ImportedConnectionSchema, 
    ImportGapSchema, ResumoImportacaoSchema
)

client = TestClient(app)

# Mock da resposta estruturada da IA de importação
MOCK_AI_RESPONSE = ProcessImportAIResultSchema(
    processo=ImportedProcessSchema(
        nome="Processo de Apuração SPED Mock",
        area="Fiscal",
        descricao="Processo de teste importado",
        objetivo="Validar fluxo de testes",
        responsavel="Testador",
        periodicidade="Mensal",
        criticidade="Alta",
        status="Ativo",
        sistemas_utilizados="TOTVS, PVA",
        documentos_utilizados="Livro Fiscal, Apuração",
        observacoes="Mock de importação"
    ),
    etapas=[
        ImportedStepSchema(
            ordem=1,
            nome="Acessar Sistema",
            descricao="Fazer login no Protheus",
            responsavel="Analista",
            entrada="Login/Senha",
            saida="Painel Principal",
            sistema_utilizado="TOTVS",
            tempo_estimado="5 min",
            tipo_etapa="Manual",
            risco="Erro de credencial",
            gargalo="Lentidão de login",
            oportunidade_automacao="Integrar SSO Single Sign-On",
            confianca_extracao="Alta",
            evidencia_documental="Parágrafo 1 do manual"
        ),
        ImportedStepSchema(
            ordem=2,
            nome="Validar Apurações",
            descricao="Auditar livro fiscal",
            responsavel="Auditor",
            entrada="Relatório",
            saida="Apuração validada",
            sistema_utilizado="PVA",
            tempo_estimado="10 min",
            tipo_etapa="Validação",
            risco="Apuração incorreta",
            gargalo="Revisão manual demorada",
            oportunidade_automacao="Cruzamento contábil eletrônico",
            confianca_extracao="Alta",
            evidencia_documental="Parágrafo 3 do manual"
        )
    ],
    conexoes=[
        ImportedConnectionSchema(
            ordem_origem=1,
            ordem_destino=2,
            tipo_conexao="padrao"
        )
    ],
    lacunas_mapeamento=[
        ImportGapSchema(
            campo_ou_tema="Imagem 1",
            descricao="Screenshot não visível na página 2",
            pergunta_recomendada="O que está contido no print de tela do Protheus?"
        )
    ],
    alertas_sensiveis=[],
    resumo_importacao=ResumoImportacaoSchema(
        quantidade_etapas=2,
        quantidade_conexoes=1,
        quantidade_lacunas=1,
        confianca_geral="Alta"
    )
)

@patch("app.services.process_import_ia_service.ProcessImportIAService.call_import_ia")
@patch("app.services.document_reader_service.DocumentReaderService.read_docx")
def test_import_process_success(mock_read_docx, mock_call_ia, db_session):
    """
    Testa a importação de processos com sucesso usando mocks para leitura e IA.
    """
    # 1. Configurar o mock de leitura para retornar um resultado simulado
    from app.services.document_reader_service import DocumentReadResult
    mock_read_docx.return_value = DocumentReadResult(
        text="Acesse o Protheus e valide a apuração fiscal.",
        filename="test_process.docx",
        size_bytes=1200,
        num_paragraphs=3,
        num_characters=45,
        num_images=1
    )
    
    # 2. Configurar o mock da IA para retornar o nosso JSON Pydantic estruturado
    mock_call_ia.return_value = MOCK_AI_RESPONSE
    
    # 3. Executar chamada multipart/form-data
    files = {"file": ("test_process.docx", b"conteudo_simulado_docx_bytes", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
    response = client.post("/api/processos/importar", files=files)
    
    # 4. Validar retornos e status
    assert response.status_code == 201
    json_data = response.json()
    assert json_data["processo_id"] is not None
    assert json_data["nome_processo"] == "Processo de Apuração SPED Mock"
    assert json_data["etapas_criadas"] == 2
    assert json_data["conexoes_criadas"] == 1
    assert len(json_data["lacunas_identificadas"]) == 1

def test_import_process_invalid_extension():
    """
    Testa rejeição de arquivos com extensões inválidas (ex: .png).
    """
    files = {"file": ("imagem.png", b"fake_png_bytes", "image/png")}
    response = client.post("/api/processos/importar", files=files)
    
    assert response.status_code == 400
    assert "Extensão de arquivo não permitida" in response.json()["detail"]

def test_import_process_empty_file():
    """
    Testa rejeição de arquivos vazios.
    """
    files = {"file": ("vazio.docx", b"", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
    response = client.post("/api/processos/importar", files=files)
    
    assert response.status_code == 400
    assert "O arquivo enviado está vazio" in response.json()["detail"]
