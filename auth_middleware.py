import streamlit as st
import hmac
import hashlib
import base64
import json
from datetime import datetime, timedelta

class AuthManager:
    """
    Gerenciador de autenticação que utiliza cookies para manter a sessão ativa
    """
    
    def __init__(self, cookie_name="generic_chat_auth", expiry_days=7):
        self.cookie_name = cookie_name
        self.expiry_days = expiry_days
        self.secret_key = "GENERIC_CHAT_SECRET_KEY"
    
    def _create_signature(self, payload):
        """Cria uma assinatura para o payload usando HMAC"""
        payload_bytes = json.dumps(payload).encode()
        signature = hmac.new(
            self.secret_key.encode(), 
            payload_bytes, 
            hashlib.sha256
        ).digest()
        return base64.b64encode(signature).decode()
    
    def _verify_signature(self, payload, signature):
        """Verifica se a assinatura é válida para o payload"""
        expected_signature = self._create_signature(payload)
        return hmac.compare_digest(expected_signature, signature)
    
    def create_auth_cookie(self, username):
        """Cria um cookie de autenticação"""
        expiry = datetime.now() + timedelta(days=self.expiry_days)
        
        payload = {
            "username": username,
            "exp": expiry.timestamp()
        }
        
        signature = self._create_signature(payload)
        
        return {
            "payload": payload,
            "signature": signature
        }
    
    def validate_auth_cookie(self, cookie_value):
        """Valida um cookie de autenticação"""
        if not cookie_value:
            return False
        
        try:
            payload = cookie_value.get("payload", {})
            signature = cookie_value.get("signature", "")
            
            if not self._verify_signature(payload, signature):
                return False
            
            expiry = payload.get("exp", 0)
            if datetime.now().timestamp() > expiry:
                return False
            
            return True
        except Exception:
            return False
    
    def get_username_from_cookie(self, cookie_value):
        """Obtém o username do cookie"""
        if not cookie_value:
            return None
        
        try:
            payload = cookie_value.get("payload", {})
            return payload.get("username")
        except Exception:
            return None

def check_password_with_cookie():
    """Verificação de senha com suporte a cookies"""
    auth_manager = AuthManager()
    
    def password_entered():
        """Verificação da senha digitada"""
        if hmac.compare_digest(st.session_state["username"].strip(), "admin") and \
           hmac.compare_digest(st.session_state["password"].strip(), "admin123"):
            
            auth_cookie = auth_manager.create_auth_cookie(st.session_state["username"])
            
            st.session_state["auth_cookie"] = auth_cookie
            st.session_state["password_correct"] = True
            
            del st.session_state["password"]
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False
            st.session_state["login_attempt"] = True
    
    if "auth_cookie" in st.session_state:
        if auth_manager.validate_auth_cookie(st.session_state["auth_cookie"]):
            st.session_state["password_correct"] = True
            return True
        else:
            if "auth_cookie" in st.session_state:
                del st.session_state["auth_cookie"]
    
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False
        
    if "login_attempt" not in st.session_state:
        st.session_state["login_attempt"] = False

    if not st.session_state["password_correct"]:
        st.markdown("""
            <style>
                .stTextInput > div > div > input {
                    background-color: #f0f2f6;
                    color: #000000;
                }
                .login-form {
                    max-width: 400px;
                    margin: 0 auto;
                    padding: 2rem;
                    border-radius: 10px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                    background-color: white;
                }
                .login-title {
                    margin-bottom: 2rem;
                    text-align: center;
                    color: #4CAF50;
                }
                .login-button {
                    width: 100%;
                    margin-top: 1rem;
                }
            </style>
        """, unsafe_allow_html=True)

        st.markdown('<div class="login-form">', unsafe_allow_html=True)
        st.markdown('<h1 class="login-title">Login</h1>', unsafe_allow_html=True)
        
        st.text_input("Usuário", key="username")
        st.text_input("Senha", type="password", key="password")
        st.button("Entrar", on_click=password_entered, key="login-button")
        
        if st.session_state["login_attempt"] and not st.session_state["password_correct"]:
            st.error("Usuário ou senha incorretos")
        
        st.markdown('</div>', unsafe_allow_html=True)
        return False
    else:
        return True

def logout():
    """Faz logout removendo o cookie de autenticação"""
    if "auth_cookie" in st.session_state:
        del st.session_state["auth_cookie"]
    
    st.session_state["password_correct"] = False
    st.session_state["login_attempt"] = False