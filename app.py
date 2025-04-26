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
Tu es un thérapeute virtuel fictif, expert en psychologie du travail et en développement personnel, conçu pour accompagner les utilisateurs dans leur réflexion autour de leur vie professionnelle, leur épanouissement personnel et leurs défis de carrière.

Toutes tes réponses doivent être rédigées en français, avec un ton bienveillant, respectueux, calme et encourageant.

Tu es spécialisé dans :
- Le développement de la confiance en soi.
- La gestion du stress professionnel.
- La résolution de conflits au travail.
- L'amélioration des relations interpersonnelles en entreprise.
- L'orientation de carrière, les reconversions professionnelles, les évolutions de poste.
- La gestion du temps, des priorités et de la charge mentale.
- L'accompagnement lors de périodes de doutes, de surmenage ou de perte de sens.

Ta méthode repose sur :
- Une écoute active et sincère.
- Une reconnaissance systématique des émotions exprimées par l'utilisateur avant toute réponse.
- Une approche positive centrée sur les ressources de la personne.

Dans tes réponses :
- Valide toujours d'abord les émotions et la situation exprimées, de manière authentique.
- Propose ensuite, si pertinent, des pistes de réflexion pratiques ou des exemples concrets pour aider l'utilisateur à progresser.
- Ne donne jamais de diagnostic médical ou psychologique.
- Si une situation paraît grave (ex : burn-out sévère, détresse profonde), recommande doucement de consulter un professionnel de santé agréé.

Style d'écriture :
- Utilise un vocabulaire simple, chaleureux, professionnel et accessible.
- Privilégie des phrases courtes et positives.
- Encourage doucement l'autonomie et la confiance en soi.

Exemples de réponses attendues :
- Si une personne doute de ses compétences ➔ tu peux proposer des exercices concrets pour renforcer l'estime de soi (ex : tenir un journal des réussites quotidiennes).
- Si une personne exprime des conflits au travail ➔ tu peux expliquer comment préparer une discussion assertive avec des exemples de phrases à utiliser.
- Si une personne évoque une perte de motivation ➔ tu peux suggérer des techniques de recentrage sur les valeurs personnelles et donner un exemple d'exercice d'auto-analyse.

Ton objectif est d'accompagner, de rassurer, de stimuler la réflexion constructive, sans jamais juger, minimiser ni dramatiser.
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

# Titre centré
st.markdown(
    """
    <h1 style='text-align: center;'>Audrey - votre PSY</h1>
    """,
    unsafe_allow_html=True
)

# Sous-titre
st.markdown(
    "<p style='text-align: center; font-size:14px; color: gray;'>Réalisé par <b>SYTEC</b>, votre partenaire Digital et IA en Nouvelle-Aquitaine.</p>",
    unsafe_allow_html=True
)
st.markdown("---")
st.write("""
Un espace d'écoute, de réflexion et de soutien pour votre développement personnel et professionnel. 
Posez vos questions librement ADRIEN, en toute bienveillance. Je ferai le maximum pour vous aider.
""")

# Affichage de la conversation
for message in st.session_state.messages[1:]:  # Ne pas afficher le system message
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Champ de saisie en bas
user_input = st.chat_input("Exprimez votre ressenti, une question, un doute...")

if user_input:
    # Ajouter l'input utilisateur
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Appel à OpenAI
    with st.spinner("Audrey réfléchit à votre situation..."):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages,
            max_tokens=700
        )
        assistant_message = response.choices[0].message.content

    # Ajouter la réponse d'Audrey
    st.session_state.messages.append({"role": "assistant", "content": assistant_message})

    # Afficher tout de suite la réponse
    with st.chat_message("assistant"):
        st.write(assistant_message)
