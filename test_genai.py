import google.generativeai as genai
import os

def test_connection():
    try:
        # Tenta usar as credenciais padrão do ambiente
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Olá, você está online?")
        print(f"✅ Conexão Direta: {response.text}")
        return True
    except Exception as e:
        print(f"❌ Falha na Conexão Direta: {e}")
        return False

if __name__ == "__main__":
    test_connection()
