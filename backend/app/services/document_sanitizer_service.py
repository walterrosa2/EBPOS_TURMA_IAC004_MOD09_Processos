import re
from loguru import logger

class SanitizedDocument:
    def __init__(self, text: str, alerts: list):
        self.text = text
        self.alerts = alerts  # Lista de dicionários {"tipo": str, "descricao": str, "acao_aplicada": str}

class DocumentSanitizerService:
    @staticmethod
    def sanitize(text: str) -> SanitizedDocument:
        """
        Varre o texto em busca de padrões sensíveis (senhas, logins, chaves de API, e-mails pessoais)
        e aplica regras de sanitização/mascaramento com segurança.
        """
        logger.info("Iniciando sanitização de conteúdo do documento.")
        
        sanitized_text = text
        alerts = []
        
        # 1. Mascaramento de Senhas e Credenciais Explícitas
        # Padrões comuns: senha: 12345, password = secret, etc.
        password_patterns = [
            (r'(?i)(senha|password|pwd|pass|key)\s*[:=]\s*([^\s\r\n,;\|]+)', "credencial", "removido")
        ]
        
        for pattern, tipo, acao in password_patterns:
            matches = re.findall(pattern, sanitized_text)
            if matches:
                for label, value in matches:
                    # Evitar mascarar termos comuns sem valores confidenciais
                    if len(value) > 2 and value.lower() not in ["null", "none", "true", "false", "vazio"]:
                        logger.info("Detector de segurança: Credencial sensível mascarada.")
                        alerts.append({
                            "tipo": tipo,
                            "descricao": f"Detector identificou termo '{label}' associado a valor sensível, que foi higienizado.",
                            "acao_aplicada": acao
                        })
                
                # Substituir os valores encontrados
                sanitized_text = re.sub(
                    pattern,
                    lambda m: f"{m.group(1)}: [MASCARADO]",
                    sanitized_text
                )

        # 2. Mascaramento de Usuários/Login
        login_patterns = [
            (r'(?i)(login|usuario|usuário|user)\s*[:=]\s*([^\s\r\n,;\|]+)', "credencial", "removido")
        ]
        
        for pattern, tipo, acao in login_patterns:
            matches = re.findall(pattern, sanitized_text)
            if matches:
                for label, value in matches:
                    if len(value) > 2 and value.lower() not in ["null", "none", "true", "false", "vazio"]:
                        logger.info("Detector de segurança: Nome de usuário/login mascarado.")
                        alerts.append({
                            "tipo": tipo,
                            "descricao": f"Identificador '{label}' com valor de credencial de acesso foi removido.",
                            "acao_aplicada": acao
                        })
                
                sanitized_text = re.sub(
                    pattern,
                    lambda m: f"{m.group(1)}: [MASCARADO]",
                    sanitized_text
                )

        # 3. Mascaramento Parcial de E-mails
        # Exemplo: walter.rosa@gmail.com -> wa*****@gmail.com
        email_pattern = r'([a-zA-Z0-9._%+-]{1,3})([a-zA-Z0-9._%+-]*)(@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
        emails_found = re.findall(email_pattern, sanitized_text)
        if emails_found:
            for _ in emails_found:
                # Evitar mascarar e-mails genéricos de sistemas conhecidos se existirem
                logger.info("Detector de segurança: E-mail sensível detectado e mascarado.")
                alerts.append({
                    "tipo": "dado_pessoal",
                    "descricao": "E-mails pessoais identificados no procedimento operacional foram parcialmente mascarados.",
                    "acao_aplicada": "mascarado"
                })
            
            sanitized_text = re.sub(
                email_pattern,
                lambda m: f"{m.group(1)}*****{m.group(3)}",
                sanitized_text
            )

        # 4. Detecção de Tokens/Chaves de API longas
        # Ex: gpt-sk-1234... ou chaves de 32+ caracteres alfanuméricos
        token_pattern = r'\b(sk-[a-zA-Z0-9]{32,64}|[a-fA-F0-9]{32,64})\b'
        tokens_found = re.findall(token_pattern, sanitized_text)
        if tokens_found:
            for token in tokens_found:
                logger.info("Detector de segurança: Token/Chave de API detectado e removido.")
                alerts.append({
                    "tipo": "certificado",
                    "descricao": "Assinatura, chave de segurança ou token exposto foi totalmente removido do texto do documento.",
                    "acao_aplicada": "removido"
                })
            
            sanitized_text = re.sub(token_pattern, "[TOKEN_MASCARADO]", sanitized_text)

        logger.info(f"Sanitização finalizada. Quantidade de alertas gerados: {len(alerts)}.")
        return SanitizedDocument(text=sanitized_text, alerts=alerts)
