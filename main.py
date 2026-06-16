import os
import sys
from dotenv import load_dotenv
from supabase import create_client, Client
import requests

load_dotenv()

def validar_ambiente():
    variaveis_obrigatorias = [
        "SUPABASE_URL",
        "SUPABASE_KEY",
        "ZAPI_INSTANCE_ID",
        "ZAPI_INSTANCE_TOKEN"
    ]
    
    erros = [var for var in variaveis_obrigatorias if not os.getenv(var)]
            
    if erros:
        print("[ERRO] Configuração incompleta. Variáveis ausentes no .env:")
        for erro in erros:
            print(f"  - {erro}")
        sys.exit(1)

def buscar_contatos_supabase() -> list:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    
    print("[INFO] Buscando contatos no Supabase...")
    try:
        supabase: Client = create_client(url, key)
        resposta = supabase.table("contatos").select("name, telefone").limit(3).execute()
        return resposta.data
    except Exception as e:
        print(f"[ERRO CRÍTICO] Falha na comunicação com o banco: {e}")
        sys.exit(1)

def enviar_mensagem_zapi(nome: str, telefone: str) -> bool:
    instance_id = os.getenv("ZAPI_INSTANCE_ID")
    instance_token = os.getenv("ZAPI_INSTANCE_TOKEN")
    
    url = f"https://api.z-api.io/instances/{instance_id}/token/{instance_token}/send-text"
    
    payload = {
        "phone": telefone,
        "message": f"Olá, {nome} tudo bem com você?"
    }
    
    headers = {"Content-Type": "application/json"}
    
    try:
        resposta = requests.post(url, json=payload, headers=headers, timeout=10)
        
        if resposta.status_code == 200:
            print(f"[OK] Mensagem enviada para {nome} ({telefone}).")
            return True
            
        print(f"[AVISO] Erro no envio para {nome}. Status: {resposta.status_code}")
        return False
            
    except requests.exceptions.RequestException as e:
        print(f"[ERRO] Falha na conexão com a Z-API para {nome}: {e}")
        return False

def main():
    validar_ambiente()
    
    lista_contatos = buscar_contatos_supabase()
    if not lista_contatos:
        print("[AVISO] Nenhum contato encontrado. Execução encerrada.")
        return

    print(f"[INFO] Processando {len(lista_contatos)} contato(s).\n")
    
    sucessos = 0
    falhas = 0
    
    for contato in lista_contatos:
        nome = contato.get('name')
        telefone = contato.get('telefone')
        
        if enviar_mensagem_zapi(nome, telefone):
            sucessos += 1
        else:
            falhas += 1
            
    print("\n--------------------------")
    print(f"[FIM] Resumo: {sucessos} enviados com sucesso | {falhas} falha(s).")

if __name__ == "__main__":
    main()