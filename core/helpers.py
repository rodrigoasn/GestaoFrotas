# ────────────────────────────────────────────────────────────────────
# IMPORTS
# ────────────────────────────────────────────────────────────────────
import requests
from django.utils.translation import gettext as _


# ────────────────────────────────────────────────────────────────────
# API: BUSCA CNPJ
# ────────────────────────────────────────────────────────────────────
def buscar_cnpj_receitaws(cnpj):
    """
    Busca dados de uma empresa na API pública da ReceitaWS pelo CNPJ.
    Retorna um dicionário com os dados mapeados ou um dicionário com chave 'erro'.
    """
    # Remove formatação do CNPJ (pontos, barras, traços)
    cnpj_limpo = ''.join([c for c in str(cnpj) if c.isdigit()])
    
    url = f"https://www.receitaws.com.br/v1/cnpj/{cnpj_limpo}"
    headers = {"Accept": "application/json"}
    
    try:
        # Timeout de 10 segundos para evitar travar a thread
        response = requests.get(url, headers=headers, timeout=10)
    except requests.exceptions.RequestException as e:
        return {"erro": _("Erro de conexão com a API da ReceitaWS.")}

    if response.status_code == 200:
        try:
            data = response.json()
        except ValueError:
             return {"erro": _("Resposta inválida da API.")}
             
        if data.get("status") == "OK":
            # Extrai atividade principal com segurança
            atividades = data.get("atividade_principal", [])
            atividade_principal = atividades[0].get("text", "") if atividades else ""
            
            # Tratamento de telefones (pode vir "11 1111-1111 / 11 2222-2222")
            raw_telefones = data.get("telefone", "")
            telefones = [t.strip() for t in raw_telefones.split("/")]
            
            telefone_principal = telefones[0] if len(telefones) > 0 else ""
            whatsapp = telefones[1] if len(telefones) > 1 else ""
            
            return {
                "razao_social": data.get("nome"),
                "nome_fantasia": data.get("fantasia"),
                "atividade_principal": atividade_principal,
                "endereco_cep": data.get("cep"),
                "endereco_logradouro": data.get("logradouro"),
                "endereco_numero": data.get("numero"),
                "endereco_complemento": data.get("complemento"),
                "endereco_estado": data.get("uf"),
                "endereco_cidade": data.get("municipio"),
                "endereco_bairro": data.get("bairro"),
                "email_root": data.get("email"),
                "telefone_contato_principal": telefone_principal,
                "whatsapp": whatsapp,
            }
        else:
            return {"erro": data.get("message", _("CNPJ inválido ou não encontrado."))}
            
    elif response.status_code == 429:
        return {"erro": _("Muitas requisições. Tente novamente em instantes (Limite da API Pública).")}
    
    return {"erro": _("Erro ao consultar a API da Receita (Status %s)") % response.status_code}


# ────────────────────────────────────────────────────────────────────
# API: BUSCA CEP
# ────────────────────────────────────────────────────────────────────
def buscar_cep_viacep(cep):
    """
    Busca dados de endereço na API pública ViaCEP pelo CEP.
    Retorna um dicionário com os dados mapeados ou um dicionário com chave 'erro'.
    """
    if not cep:
        return {"erro": _("CEP não fornecido.")}

    # Remove formatação do CEP
    cep_limpo = ''.join([c for c in str(cep) if c.isdigit()])
    
    if len(cep_limpo) != 8:
        return {"erro": _("CEP inválido. Deve conter 8 dígitos.")}

    url = f"https://viacep.com.br/ws/{cep_limpo}/json/"
    
    try:
        # Timeout de 5 segundos
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException:
        return {"erro": _("Erro de conexão com a API ViaCEP.")}

    if response.status_code == 200:
        try:
            data = response.json()
        except ValueError:
             return {"erro": _("Resposta inválida da API.")}
        
        if "erro" in data:
            return {"erro": _("CEP não encontrado.")}
            
        return {
            "endereco_cep": data.get("cep"),
            "endereco_logradouro": data.get("logradouro"),
            "endereco_bairro": data.get("bairro"),
            "endereco_cidade": data.get("localidade"),
            "endereco_estado": data.get("uf"),
            "endereco_complemento": data.get("complemento"),
        }
    
    return {"erro": _("Erro ao consultar CEP (Status %s)") % response.status_code}