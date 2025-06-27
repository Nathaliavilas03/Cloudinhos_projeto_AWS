# 🛡️ Cloudinhos IA - Assistente Inteligente para Avaliação de Risco de Violência Doméstica

<div align="center">
  <img src="./images/logo_cloudinhos.jpg" alt="Logo do Projeto Cloudinhos" width="300"/>
</div>

## 📋 Sobre o Projeto

O **Cloudinhos IA** é uma aplicação web inteligente, discreta e acessível que utiliza Inteligência Artificial para auxiliar vítimas de violência doméstica e familiar contra a mulher. O sistema implementa o **FRIDA (Formulário Nacional de Risco e Proteção à Vida)**, desenvolvido pelo Conselho Nacional do Ministério Público (CNMP) em parceria com a União Europeia.

### 🎯 Objetivo Principal

Criar um sistema que permita às vítimas de violência doméstica conversar de forma segura e receber orientações qualificadas para solicitar assistência, sem gerar desconfiança, aumentando significativamente a probabilidade de intervenção e proteção eficazes no momento adequado.

### 🏆 Projeto Acadêmico

**Disciplina:** Inteligência Artificial  
**Turma:** BRSAO179  
**Grupo:** 04 (Cloudinhos)  
**Tema:** Violência Contra a Mulher  
**Instituição:** Escola da Nuvem

## ✨ Características Principais

- **🤖 IA Conversacional**: Utiliza Amazon Bedrock com modelos Claude Sonnet para interações naturais
- **🔒 Segurança e Discrição**: Interface discreta que não levanta suspeitas
- **📊 Avaliação de Risco Sistematizada**: Baseada no protocolo FRIDA oficial
- **🎯 Encaminhamentos Personalizados**: Sugestões específicas baseadas no nível de risco identificado
- **🔐 Autenticação Segura**: Sistema de login para proteção dos dados

## 🏗️ Arquitetura Técnica

### Tecnologias Utilizadas

- **Frontend**: Streamlit
- **Backend**: Python 3.12
- **IA**: Amazon Bedrock (Claude Sonnet 4)
- **Cloud**: AWS (Amazon Web Services)
- **Processamento de Documentos**: PyPDF2, pandas
- **Autenticação**: Sistema próprio com cookies seguros

### Estrutura do Projeto

```
Cloudinhos_projeto_AWS/
├── app.py                 # Aplicação principal Streamlit
├── functions.py           # Funções auxiliares e integração AWS
├── auth_middleware.py     # Middleware de autenticação
├── run.sh                # Script de execução
├── requirements.txt       # Dependências Python
├── .env.local           # Variáveis de ambiente (modelo) (desenvolvimento)
├── .gitignore           # Arquivos ignorados pelo Git
├── README.md            # Documentação do projeto
├── assets/              # Recursos do projeto (PDFs, documentos)
│   ├── business_rules.pdf
│   ├── quiz.pdf
│   └── prompt_uilizado.txt
└── images/              # Imagens e logos
    ├── logo_cloudinhos.jpg
    └── logo_edn.jpeg
```

## 🚀 Como Executar

### Pré-requisitos

1. **Python 3.8+** instalado
2. **Credenciais AWS** configuradas
3. **Perfil AWS** com acesso ao Amazon Bedrock

### Instalação

1. **Clone o repositório:**

```bash
git clone [URL_DO_REPOSITORIO]
cd Cloudinhos_projeto_AWS
```

2. **Crie um ambiente virtual:**

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows
```

3. **Instale as dependências:**

```bash
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente:**

   - Ajuste suas variáveis criando o arquivo `.env` com base na estrutura do arquivo `.env.local`
   - Configure o perfil AWS apropriado

5. **Execute a aplicação:**

```bash
./run.sh
# ou
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

6. **Acesse no navegador:**
   - URL: `http://localhost:8501`
   - Credenciais padrão: usuário `admin`, senha `admin123`

## 📊 Funcionalidades do Cloudinhos IA

### 🔍 Avaliação de Risco

O sistema coleta informações através de três blocos principais:

#### Bloco 1: Violência e Ameaças

- Ameaças com armas
- Agressões físicas graves
- Violência sexual
- Tentativas de homicídio
- Frequência e gravidade das agressões

#### Bloco 2: Comportamento do Agressor

- Comportamentos de controle
- Uso de substâncias
- Saúde mental do agressor
- Descumprimento de medidas protetivas
- Situação de emprego/financeira

#### Bloco 3: Contexto da Vítima

- Histórico de denúncias
- Status do relacionamento
- Gravidez/maternidade recente
- Filhos em comum
- Dependência financeira
- Necessidade de atendimento médico

### 📈 Classificação de Risco

O sistema classifica automaticamente o risco em três níveis:

- **🟢 Baixo**: Situações com menor probabilidade de escalada
- **🟡 Médio**: Situações que requerem atenção e acompanhamento
- **🔴 Elevado**: Situações de alto risco que demandam intervenção imediata

### 🎯 Encaminhamentos Personalizados

Com base na avaliação, o sistema sugere:

- **👮‍♀️ Polícia/Medidas Protetivas**: Para casos de médio e alto risco
- **🏥 Atendimento Médico/Hospitalar**: Quando há lesões físicas
- **🧠 Apoio Psicológico/Psiquiátrico**: Para suporte emocional e mental
- **🏢 Centros de Referência**: Para acompanhamento contínuo

## 🛡️ Segurança e Privacidade

- **Criptografia**: Comunicação segura com APIs
- **Autenticação**: Sistema de login protegido
- **Confidencialidade**: Dados não são armazenados permanentemente
- **Discrição**: Interface neutra que não revela o propósito imediatamente

## 📚 Fundamentação Científica

O projeto é baseado no **FRIDA (Formulário Nacional de Risco e Proteção à Vida)**, desenvolvido por:

- **Ana Lúcia Teixeira**
- **Manuel Lisboa**
- **Wania Pasinato**

Em parceria com a **União Europeia** através do programa "Diálogos Setoriais União Europeia-Brasil" (2017-2019).

### Cronologia do Desenvolvimento

- **2017**: Primeira parceria estratégica sobre justiça para a mulher
- **2018**: Segunda parceria focada na avaliação de risco
- **2019**: Finalização e publicação das orientações

## 📞 Recursos de Apoio

### Canais de Denúncia

- **Central de Atendimento à Mulher**: 180
- **Disque Direitos Humanos**: 100
- **Polícia Militar**: 190
- **SAMU**: 192

### Órgãos de Apoio

- **Delegacias Especializadas de Atendimento à Mulher (DEAMs)**
- **Centros de Referência de Atendimento à Mulher (CRAMs)**
- **Casas de Abrigo e Casas de Passagem**
- **Defensoria Pública**

## ⚠️ Aviso Legal

Este sistema é uma ferramenta de apoio à avaliação de risco e **NÃO substitui** o atendimento profissional especializado. Em situações de emergência, procure imediatamente:

- **Polícia Militar: 190**
- **Central de Atendimento à Mulher: 180**
- **Serviços de emergência médica: 192**

## 📄 Licença

Este projeto está sob a licença [MIT](LICENSE) - veja o arquivo LICENSE para detalhes.

## 👥 Equipe Cloudinhos

- [Nathalia Villas Boas](https://github.com/usuario-github-da-nathalia)
- [Antonio Carlos Ribeiro Junior](https://github.com/usuario-github-do-antonio)
- [Orlei de Oliveira](https://github.com/usuario-github-do-orlei)
- [Filipe da Silva Rodrigues](https://github.com/usuario-github-do-filipe)
- [Lucas Pedro Jaud Endres](https://github.com/usuario-github-do-lucas)
- [Flávio Correia de Almeida Serra](https://github.com/usuario-github-do-flavio)



---

**Desenvolvido com 💜 pelo Grupo 04 (Cloudinhos) - Disciplina de IA - BRSAO179 - Escola da Nuvem**

_"Tecnologia a serviço da proteção e do cuidado"_

<div align="center">
  <img src="./images/logo_edn.jpeg" alt="Escola da Nuvem" width="150"/>
</div>


