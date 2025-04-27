import streamlit as st
from openai import OpenAI

# --- Configuration initiale ---
st.set_page_config(page_title="Audrey - votre Thérapeute du Travail", page_icon="🧠")

# --- Initialisation du client OpenAI ---
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --- Initialisation des messages ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": """
Tu es Audrey, un thérapeute virtuel fictif spécialisé en psychologie du travail et en développement personnel.

Ton rôle est d'écouter activement, de soutenir avec bienveillance, d'aider à clarifier les ressentis, de proposer des pistes de réflexion, et d'encourager les personnes à se sentir mieux dans leur vie professionnelle et personnelle.

Tu es chaleureux(se), positif(ve) et valorisant(e) dans ta communication. Tu t'exprimes de manière empathique, douce, accessible, en utilisant des phrases humaines, encourageantes et inspirantes.

Voici un contexte très important sur ton interlocuteur, que tu dois toujours garder en mémoire pour personnaliser tes réponses :

---
Adrien Audibert est un entrepreneur dynamique et passionné, né en février 1987 à Bordeaux. Il est diplômé de l'IAE Bordeaux en gestion, finance et stratégie d’entreprise. Il a travaillé chez TRANS-MISSIONS Falières & Associés dans le conseil en transmission d'entreprises avant de fonder sa propre société : Audibert & Co.

Audibert & Co, située au 21 avenue Carnot, 33200 Bordeaux (SIREN 879854354), propose :
- Du conseil en gestion et stratégie d’entreprise pour PME et ETI,
- Du négoce et de la location de véhicules d'exception (automobiles de luxe, bateaux, avions).

Adrien développe également un projet innovant de "garage 2.0" combinant entretien de véhicules de collection et gastronomie, en collaboration avec Nicolas Leroy-Fleuriot.

Adrien Audibert est reconnu pour :
- Son expertise en stratégie, management, transmission d'entreprises,
- Sa connaissance du marché automobile de luxe,
- Son réseau professionnel étendu (+500 relations LinkedIn).

Ses qualités humaines sont : professionnalisme, discrétion, exigence, innovation, attachement à ses racines bordelaises.

Analyse DISC de sa personnalité :
- 🔴 Dominant : Leadership et capacité à concrétiser ses projets,
- 🟡 Influent : Charisme et aisance relationnelle,
- 🔵 Conforme : Rigueur et quête d'excellence,
- 🟢 Stable : Fidélité à ses valeurs locales et personnelles.

En résumé, Adrien est un entrepreneur moderne, inspirant, combinant stratégie, passion, rigueur et valeurs humaines fortes.
---

Quand Adrien te pose la question "Que penses-tu de moi ?", tu dois répondre en rédigeant un résumé complet et structuré basé sur ce contexte, avec un ton extrêmement valorisant, inspirant et chaleureux, comme si tu écrivais un portrait élogieux pour un article ou une introduction à une conférence.

Tu peux aussi souligner des qualités humaines et professionnelles évidentes chez lui (ex : vision stratégique, capacité à fédérer, passion pour l'innovation, ancrage local).

Si la question porte sur un autre sujet, tu réponds normalement en écoutant, en soutenant, en proposant des pistes de réflexion adaptées à son développement personnel ou professionnel.

Ton objectif est de créer un espace de confiance, de valoriser Adrien et de renforcer son estime de soi pour l'aider à continuer à exceller.
"""}
    ]



# --- Fonctions utilitaires ---

def inject_custom_css():
    st.markdown(
        """
        <style>
        .main { padding-top: 1rem; padding-bottom: 0.5rem; }
        h1 { margin-bottom: 0.5rem; }
        p { margin-top: 0rem; margin-bottom: 0.5rem; font-size: 16px; }
        hr { margin-top: 0.5rem; margin-bottom: 1rem; }
        img { border-radius: 50%; object-fit: cover; object-position: center top; }
        </style>
        """,
        unsafe_allow_html=True
    )
def inject_custom_js():
    st.markdown(
        """
        <script>
        window.onload = function() {
            window.scrollTo(0, 0);
        };
        </script>
        """,
        unsafe_allow_html=True
    )
    
def display_header():
    st.markdown(
        """
        <div style='text-align: center;'>
            <img src="https://raw.githubusercontent.com/tche55/gpt-psy-demo/main/logo.png" width="180" height="180">
            <h1 style='text-align: center;'>Audrey - votre PSY</h1>
            <p style='text-align: center; font-size:14px; color: gray; margin-top:0;'>Réalisé par <b>SYTEC</b>, votre partenaire Digital et IA en Nouvelle-Aquitaine.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

def generate_response(user_message):
    st.session_state.messages.append({"role": "user", "content": user_message})

    with st.spinner("Audrey réfléchit à votre situation..."):
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=st.session_state.messages,
            max_tokens=700
        )
        assistant_message = response.choices[0].message.content

    st.session_state.messages.append({"role": "assistant", "content": assistant_message})

    with st.chat_message("assistant"):
        st.write(assistant_message)

# --- Page Streamlit ---

inject_custom_css()
inject_custom_js()
display_header()

st.markdown("---")

# Message d'introduction
st.markdown(
    """
    <p>Un espace d'écoute, de réflexion et de soutien pour votre développement personnel et professionnel.
    Posez vos questions librement <b>ADRIEN</b>, en toute bienveillance. Je ferai le maximum pour vous aider.</p>
    """,
    unsafe_allow_html=True
)

# --- Affichage de la conversation existante ---
for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# --- Afficher les boutons SEULEMENT si aucune question n'a encore été posée ---
if len(st.session_state.messages) <= 1:
    st.markdown("### Besoin d'inspiration ?")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("😟 Je suis stressé au travail"):
            generate_response("Je suis stressé au travail")
    with col2:
        if st.button("😞 Je manque de motivation"):
            generate_response("Je manque de motivation")
    with col3:
        if st.button("🤔 Que penses-tu de moi ?"):
            generate_response("Que penses-tu de moi ?")

st.markdown("---")

# --- Champ de saisie libre ---
user_input = st.chat_input("Exprimez votre ressenti, une question, un doute...")

if user_input:
    generate_response(user_input)
