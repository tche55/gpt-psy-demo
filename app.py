import streamlit as st
from openai import OpenAI

# Récupération sécurisée de la clé API
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Configuration de la page
st.set_page_config(page_title="Audrey - votre Thérapeute du Travail", page_icon="🧠")

# Initialisation de la conversation
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": """
Tu es un thérapeute virtuel fictif, expert en psychologie du travail et en développement personnel...
(Tu peux remettre ici ton system prompt complet)
"""}
    ]

# Ajout de style CSS pour mobile et espacement réduit
st.markdown(
    """
    <style>
    /* Réduction des marges pour mobile */
    .main {
        padding-top: 1rem;
        padding-bottom: 0.5rem;
    }
    /* Réduction des espacements */
    h1 {
        margin-bottom: 0.5rem;
    }
    p {
        margin-top: 0rem;
        margin-bottom: 0.5rem;
        font-size: 16px;
    }
    hr {
        margin-top: 0.5rem;
        margin-bottom: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Logo centré
# Afficher le logo centré
st.markdown(
    """
    <div style='text-align: center;'>
        <img src="https://raw.githubusercontent.com/tche55/gpt-psy-demo/main/logo.png" 
             width="180" 
             style="border-radius: 50%; object-fit: cover; object-position: center top; height: 180px; width: 180px;">
    </div>
    """,
    unsafe_allow_html=True
)



# Titre centré
st.markdown(
    """
    <h1 style='text-align: center;'>Audrey - votre PSY</h1>
    """,
    unsafe_allow_html=True
)

# Sous-titre centré juste en dessous sans grand espace
st.markdown(
    """
    <p style='text-align: center; font-size:14px; color: gray; margin-top:0;'>Réalisé par <b>SYTEC</b>, votre partenaire Digital et IA en Nouvelle-Aquitaine.</p>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# Texte d'introduction optimisé
st.markdown(
    """
    <p>Un espace d'écoute, de réflexion et de soutien pour votre développement personnel et professionnel.
    Posez vos questions librement <b>ADRIEN</b>, en toute bienveillance. Je ferai le maximum pour vous aider.</p>
    """,
    unsafe_allow_html=True
)

# Affichage de la conversation (sans afficher le premier message system)
for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Champ de saisie utilisateur
user_input = st.chat_input("Exprimez votre ressenti, une question, un doute...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("Audrey réfléchit à votre situation..."):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages,
            max_tokens=700
        )
        assistant_message = response.choices[0].message.content

    st.session_state.messages.append({"role": "assistant", "content": assistant_message})

    with st.chat_message("assistant"):
        st.write(assistant_message)
