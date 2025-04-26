import streamlit as st
from openai import OpenAI

# Récupération sécurisée de la clé API
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Configuration de la page
st.set_page_config(page_title="Thérapeute du Travail Virtuel", page_icon="🧠")

# Personnalisation du style avec CSS
st.markdown(
    """
    <style>
    body {
        background-color: #f5f7fa;
    }
    .main {
        background-color: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        max-width: 700px;
        margin: auto;
    }
    textarea, input[type="text"], input[type="submit"] {
        border-radius: 10px;
    }
    button[kind="primary"] {
        border-radius: 10px;
        background-color: #4CAF50;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

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



# Zone principale
with st.container():
    st.title("Audrey - votre PSY du travail")
    st.markdown("---")  # Ligne de séparation légère

    st.write("""
    Un espace d'écoute, de réflexion et de soutien pour votre développement personnel et professionnel. 
    Posez vos questions librement, en toute bienveillance. Je ferai le maximum pour vous aider.
    """)

    prompt = st.text_area("Exprimez ici vos préoccupations, doutes ou envies de réflexion :", "")

    if st.button("Envoyer"):
        if prompt:
            with st.spinner("Le thérapeute réfléchit avec vous..."):
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": """(TON SYSTEM PROMPT ICI COMME AVANT)"""}
                        ,
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=700
                )
                message = response.choices[0].message.content
                st.success(message)
        else:
            st.error("Merci de saisir un message avant d'envoyer.")
