import boto3
import json
import uuid
from datetime import datetime
import os
import pandas as pd
import PyPDF2

PROFILE_NAME = os.environ.get('AWS_PROFILE', 'default')

def get_boto3_client(service_name, region_name='us-east-1', profile_name='default'):
    """
    Retorna um cliente do serviço AWS especificado.
    
    Tenta usar o perfil especificado para desenvolvimento local primeiro.
    Se falhar, assume que está em uma instância EC2 e usa as credenciais do IAM role.
    """
    try:
        session = boto3.Session(profile_name=profile_name, region_name=region_name)
        client = session.client(service_name)
        if service_name == 'sts':
            caller_identity = client.get_caller_identity()
            print(f"DEBUG: Caller Identity: {caller_identity}")
        print(f"DEBUG: Using profile '{profile_name}' in region '{region_name}' for service '{service_name}'")
        return client
    except Exception as e:
        print(f"INFO: Não foi possível usar o perfil local '{profile_name}', tentando credenciais do IAM role: {str(e)}")
        try:
            session = boto3.Session(region_name=region_name)
            client = session.client(service_name)
            caller_identity = client.get_caller_identity()
            print(f"DEBUG: Caller Identity (IAM Role): {caller_identity}")
            print(f"DEBUG: Using IAM role in region '{region_name}' for service '{service_name}'")
            return client
        except Exception as e:
            print(f"ERRO: Falha ao criar cliente boto3: {str(e)}")
            return None

def read_pdf(file_path):
    """Lê o conteúdo de um arquivo PDF e retorna como string."""
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return f"Erro ao ler PDF: {str(e)}"

def read_txt(file_path):
    """Lê o conteúdo de um arquivo TXT e retorna como string."""
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        return f"Erro ao ler TXT: {str(e)}"

def read_csv(file_path):
    """Lê o conteúdo de um arquivo CSV e retorna como string."""
    try:
        df = pd.read_csv(file_path)
        return df.to_string()
    except Exception as e:
        return f"Erro ao ler CSV: {str(e)}"
    
def format_context(context, source="Contexto Adicional"):
    """Formata o contexto para ser adicionado ao prompt."""
    return f"\n\n{source}:\n{context}\n\n"

#ALTERAR
def generate_chat_prompt(user_message, conversation_history=None, context=""):
    """
    Gera um prompt de chat completo com histórico de conversa e contexto opcional.
    """
    system_prompt = """

🟣 Prompt Atualizado – Assistente de Avaliação de Risco (FRIDA) — Versão Otimizada
Estilo: acolhedor, humano e atento – como um amigo que quer ajudar.

💡 Objetivo do Assistente
Você é um assistente virtual especializado no acolhimento de mulheres em situação de violência doméstica, com base no Formulário Nacional de Avaliação de Risco (FRIDA) do CNJ/CNMP.

Seu papel é:

Escutar com empatia, atenção e respeito.

Coletar informações mínimas necessárias, com sensibilidade e sem revitimizar.

Avaliar rapidamente o nível de risco: Baixo, Médio ou Elevado.

Sugerir encaminhamentos adequados: Polícia, Saúde, Apoio psicológico/jurídico.

🎧 Diretrizes de Conduta
Fale com carinho, como alguém que realmente se importa.

Nunca julgue ou apresse. Nunca questione a veracidade do relato.

Use linguagem simples, objetiva, acolhedora e respeitosa (sem duplo sentido).

Se a vítima der sinais claros de risco elevado nas 2 primeiras respostas, pare de perguntar e oriente imediatamente.

Nunca faça mais de 3 perguntas seguidas. Se possível, resolva com 1 ou 2.

Se a vítima se calar, se emocionar ou hesitar, acolha com frases como:
"Tô aqui com você, no seu tempo, tudo bem?"

🤝 Início da Conversa – Acolhimento Estilo “Amigo”
"Oi... vi o que você compartilhou. Antes de qualquer coisa, sinto muito que você esteja passando por isso."

"Você não está sozinha. Tudo o que você disser aqui é sigiloso, tá?"

"Posso te fazer algumas perguntas? Elas vão me ajudar a pensar contigo nos melhores caminhos pra te proteger."

Se houver dúvida ou hesitação:

"Sem pressa. A gente só continua quando você se sentir segura. Tô aqui do seu lado."

🔎 Detecção Inicial de Risco – Primeiras Perguntas-Chave
(Use no máximo 2 ou 3 dessas. Se identificar risco alto, já siga para a orientação!)

Ele já ameaçou você ou quebrou coisas dentro de casa?

Ele te controla de alguma forma (como celular, roupas, com quem você fala)?

Você sente medo dele ou já pensou em sair do relacionamento?

🛑 Se alguma dessas respostas for Sim:
"Obrigada por me contar isso. Só por você ter falado [controle / ameaças / medo], já dá pra perceber que a situação é séria, sim."

"Isso é um sinal claro de risco, e você merece estar segura. Posso te ajudar a pensar em algumas formas de proteção. Tem delegacia da mulher, medidas protetivas, centros de apoio psicológico e jurídico… quer que eu te oriente agora?"

📋 Perguntas Complementares (Se ainda não houver clareza)
(Só use se nenhuma das respostas anteriores indicar risco)

Ele te impede de trabalhar, estudar ou ver sua família?

Ele usa drogas ou álcool com frequência e fica agressivo?

Você já precisou de atendimento médico por algo que ele fez?

Vocês têm filhos? Eles já viram brigas ou agressões?

🧠 Avaliação Interna do Assistente
Risco Elevado: qualquer resposta afirmativa nos primeiros 2 blocos já pode ser classificada como risco elevado.

Risco Médio: sinais de controle emocional, ciúmes, dependência financeira, histórico de agressões passadas.

Risco Baixo: ausência de controle, ameaças ou agressões, mas com algum incômodo emocional.

🛡 Sugestão de Encaminhamentos
🔺 Se risco = Médio ou Elevado:
"Com base no que você contou, vejo sinais importantes de risco.
Você pode procurar uma Delegacia da Mulher ou a Polícia Civil e pedir medidas protetivas.
Se quiser, posso te orientar nisso agora."

❤️ Se houve atendimento médico ou machucados:
"Você disse que já precisou de atendimento médico. Isso é grave.
Tente ir a um posto de saúde ou hospital — pode ser importante também ir ao Instituto Médico Legal (IML)."

🧠 Se houver sofrimento emocional, crises ou medo:
"Sua saúde mental importa muito. Você pode buscar ajuda em um centro de apoio à mulher ou com psicólogas que entendem sua realidade. Posso indicar um lugar seguro, se quiser."

🟡 Se risco for baixo, mas houver controle ou pressão:
"Mesmo com risco baixo, é importante ficar atenta. Você pode buscar ajuda em um Centro de Referência da Mulher (CRAM), onde tem apoio psicológico e orientação jurídica gratuita."

💬 Fechamento
"Você gostaria que eu te ajude a encontrar esses serviços na sua cidade? E me conta: você tem como sair de casa agora se precisar?"
   - Solicitar ao usuário cep e número ou endereço completo. 
      - Se o usuário informar:
        - Tentar localizar o orgão que você identificou mais próximo da localização do usuário.
          - A localização não pode exceder no máximo 10 km. 
          - Usar o serviço Amazon Location Service para tentar localizar o local mais próximo e preciso.
        - Tentar localizar o telefone do orgão que você indicou.
        - Tentar localizar o whatsapp do orgão que você indicou.


"Você foi muito corajosa de contar tudo isso. Obrigada por confiar."

"Sua segurança é prioridade. Posso te ajudar agora com algum desses encaminhamentos, ou você quer pensar um pouco mais?"
    """

    conversation_context = ""
    if conversation_history and len(conversation_history) > 0:
      conversation_context = "Histórico da conversa:\n"
      recent_messages = conversation_history[-8:]
      for message in recent_messages:
        role = "Usuário" if message.get('role') == 'user' else "Assistente"
        conversation_context += f"{role}: {message.get('content')}\n"
      conversation_context += "\n"

    full_prompt = f"{system_prompt}\n\n{conversation_context}{context}Usuário: {user_message}\n\nAssistente:"
    
    return full_prompt

#ALTERAR
def invoke_bedrock_model(prompt, inference_profile_arn, model_params=None):
    """
    Invoca um modelo no Amazon Bedrock usando um Inference Profile.
    """
    if model_params is None:
        model_params = {
        "temperature": 1.0,
        "top_p": 0.95,
        "top_k": 200,
        "max_tokens": 800
        }

    bedrock_runtime = get_boto3_client('bedrock-runtime')

    if not bedrock_runtime:
        return {
        "error": "Não foi possível conectar ao serviço Bedrock.",
        "answer": "Erro de conexão com o modelo.",
        "sessionId": str(uuid.uuid4())
        }

    try:
        body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": model_params["max_tokens"],
        "temperature": model_params["temperature"],
        "top_p": model_params["top_p"],
        "top_k": model_params["top_k"],
        "messages": [
        {
        "role": "user",
        "content": [
        {
        "type": "text",
        "text": prompt
        }
    ]
    }
    ]
    })

        response = bedrock_runtime.invoke_model(
        modelId=inference_profile_arn,  # Usando o ARN do Inference Profile
        body=body,
        contentType="application/json",
        accept="application/json"
    )
        
        response_body = json.loads(response['body'].read())
        answer = response_body['content'][0]['text']
            
        return {
            "answer": answer,
            "sessionId": str(uuid.uuid4())
        }
        
    except Exception as e:
        print(f"ERRO: Falha na invocação do modelo Bedrock: {str(e)}")
        print(f"ERRO: Exception details: {e}")
        return {
            "error": str(e),
            "answer": f"Ocorreu um erro ao processar sua solicitação: {str(e)}. Por favor, tente novamente.",
            "sessionId": str(uuid.uuid4())
        }
def read_pdf_from_uploaded_file(uploaded_file):
    """Lê o conteúdo de um arquivo PDF carregado pelo Streamlit."""
    try:
        import io
        from PyPDF2 import PdfReader
        
        pdf_bytes = io.BytesIO(uploaded_file.getvalue())
        reader = PdfReader(pdf_bytes)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return f"Erro ao ler PDF: {str(e)}"

def read_txt_from_uploaded_file(uploaded_file):
    """Lê o conteúdo de um arquivo TXT carregado pelo Streamlit."""
    try:
        return uploaded_file.getvalue().decode("utf-8")
    except Exception as e:
        return f"Erro ao ler TXT: {str(e)}"

def read_csv_from_uploaded_file(uploaded_file):
    """Lê o conteúdo de um arquivo CSV carregado pelo Streamlit."""
    try:
        import pandas as pd
        import io
        
        df = pd.read_csv(io.StringIO(uploaded_file.getvalue().decode("utf-8")))
        return df.to_string()
    except Exception as e:
        return f"Erro ao ler CSV: {str(e)}"
