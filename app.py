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
    textarea, input[type="text"], input[type="submit"], button {
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

# Afficher le logo rond centré
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
    st.markdown("---")

    st.write("""
    Un espace d'écoute, de réflexion et de soutien pour votre développement personnel et professionnel. 
    Posez vos questions librement, en toute bienveillance. Je ferai le maximum pour vous aider.
    """)

    # Initialiser la session_state si elle n'existe pas
    if "prompt" not in st.session_state:
        st.session_state.prompt = ""

    # Champ de texte contrôlé
    prompt = st.text_area(
        "Exprimez ici vos préoccupations, doutes ou envies de réflexion :",
        value=st.session_state.prompt,
        key="prompt"
    )

    # Bouton envoyer
    envoyer = st.button("Envoyer")

    if envoyer and st.session_state.prompt.strip():
        with st.spinner("Le thérapeute réfléchit avec vous..."):
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
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
                    ,
                    {"role": "user", "content": st.session_state.prompt}
                ],
                max_tokens=700
            )
            message = response.choices[0].message.content
            st.success(message)

        # Remettre prompt à vide sans casser Streamlit
        st.session_state.update(prompt="")

    elif envoyer:
        st.error("Merci de saisir un message avant d'envoyer.")
