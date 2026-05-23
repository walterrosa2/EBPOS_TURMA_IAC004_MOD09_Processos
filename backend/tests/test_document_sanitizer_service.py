from app.services.document_sanitizer_service import DocumentSanitizerService

def test_sanitize_passwords_and_keys():
    # Texto contendo senhas e chaves confidenciais
    text = "Acesse o sistema Protheus com o Usuário: admin e Senha: MinhaSenhaSuperSecreta123. Use o token sk-12345678901234567890123456789012 para autenticação."
    
    result = DocumentSanitizerService.sanitize(text)
    
    # Validar que a senha original foi removida/mascarada
    assert "MinhaSenhaSuperSecreta123" not in result.text
    assert "Senha: [MASCARADO]" in result.text
    
    # Validar que o login original foi higienizado
    assert "Usuário: [MASCARADO]" in result.text
    
    # Validar que o token da API foi mascarado
    assert "sk-12345678901234567890123456789012" not in result.text
    assert "[TOKEN_MASCARADO]" in result.text
    
    # Validar se os alertas foram gerados corretamente
    assert len(result.alerts) >= 3
    assert any(alert["tipo"] == "credencial" for alert in result.alerts)
    assert any(alert["tipo"] == "certificado" for alert in result.alerts)

def test_sanitize_emails():
    # Texto contendo e-mails pessoais
    text = "Para suporte, entre em contato com walter.rosa@gmail.com ou jose.silva@empresa.com.br."
    
    result = DocumentSanitizerService.sanitize(text)
    
    # Validar que os e-mails originais foram mascarados
    assert "walter.rosa@gmail.com" not in result.text
    assert "jose.silva@empresa.com.br" not in result.text
    
    # Validar mascaramento parcial
    assert "wal*****@gmail.com" in result.text or "wa*****@gmail.com" in result.text
    assert "jos*****@empresa.com.br" in result.text or "jo*****@empresa.com.br" in result.text
    
    # Validar se gerou alertas de dados pessoais
    assert len(result.alerts) >= 2
    assert all(alert["tipo"] == "dado_pessoal" for alert in result.alerts)

def test_sanitize_no_sensitive_data():
    # Texto limpo
    text = "O processo de Geração do SPED Fiscal consiste em reprocessar os livros fiscais e validar apurações no Protheus."
    
    result = DocumentSanitizerService.sanitize(text)
    
    # Validar que o texto permaneceu inalterado e nenhum alerta foi gerado
    assert result.text == text
    assert len(result.alerts) == 0
