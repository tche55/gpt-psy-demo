import streamlit as st
from openai import OpenAI

# Récupération sécurisée de la clé API
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Page configuration
st.set_page_config(page_title="Audrey - votre Thérapeute du Travail", page_icon="🧠")

# Initialiser la conversation si elle n'existe pas
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": """
Tu es Audrey, une thérapeute du travail fictive, bienveillante, calme et professionnelle. 
Tu aides les utilisateurs à travers leurs défis professionnels, carrière, stress, relations au travail et épanouissement personnel.
Réponds toujours en français, de manière positive, chaleureuse et respectueuse.
"""}
    ]

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

# Titre
st.title("Audrey - votre PSY du travail")
st.markdown("---")
st.write("""
Un espace d'écoute, de réflexion et de soutien pour votre développement personnel et professionnel. 
Posez vos questions librement, en toute bienveillance. Je ferai le maximum pour vous aider.
""")

# Affichage de la conversation
for message in st.session_state.messages[1:]:  # On saute le "system" pour l'affichage
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Champ de saisie en bas
user_input = st.chat_input("Exprimez votre ressenti, une question, un doute...")

if user_input:
    # Ajouter la question de l'utilisateur
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Appel à OpenAI
    with st.spinner("Audrey réfléchit à votre situation..."):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages,
            max_tokens=700
        )
        assistant_message = response.choices[0].message.content

    # Ajouter la réponse de l'assistant
    st.session_state.messages.append({"role": "assistant", "content": assistant_message})

    # Afficher la réponse tout de suite
    with st.chat_message("assistant"):
        st.write(assistant_message)
