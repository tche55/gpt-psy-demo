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
Tu es un thérapeute virtuel fictif, expert en psychologie du travail et en développement personnel...
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
    # Contexte complet pour Adrien Audibert
    special_context = """
Adrien Audibert est un entrepreneur dynamique et passionné, né en février 1987 à Bordeaux. Il a suivi un parcours académique solide à l'IAE Bordeaux, se spécialisant en gestion, finance et stratégie d’entreprise. Cette formation l’a conduit à se spécialiser dans le conseil aux entreprises, notamment en fusions-acquisitions (M&A) et en gestion de PME.

Dès le début de sa carrière, Adrien Audibert a démontré un fort esprit d’initiative et une grande compréhension des enjeux des dirigeants d’entreprise. Il a travaillé chez TRANS-MISSIONS Falières & Associés, un cabinet de conseil en transmission d’entreprises à Bordeaux, où il a accompagné de nombreux chefs d'entreprise dans des projets de cession, d’acquisition ou de développement.

En 2020, Adrien fonde Audibert & Co, société innovante développée autour de deux activités principales :
- Conseil en gestion et en stratégie d’entreprise : accompagnement personnalisé de PME et d’ETI pour leur croissance, leur transmission, leur structuration ou leur optimisation.
- Négoce d’automobiles d’exception : recherche, achat, vente et location de véhicules de prestige (voitures de sport, voitures de collection, bateaux, avions), avec une approche sur-mesure et discrète.

Audibert & Co est basée au 21 avenue Carnot, 33200 Bordeaux (immatriculée sous le SIREN 879854354, code APE 7022Z).

Adrien Audibert est également à l’initiative d'un projet innovant de « garage 2.0 » mêlant univers automobile et gastronomie, en collaboration avec Nicolas Leroy-Fleuriot (ancien président de Cheops Technology). Ce lieu hybride proposera l'entretien de véhicules d'exception et un restaurant haut de gamme au milieu des voitures de collection. Ce concept suscite déjà un fort intérêt régional.

Expertise et réseau :
Adrien est reconnu pour son expertise en conseil stratégique, gestion de projets complexes et négociation. Il dispose d'une connaissance approfondie du tissu économique bordelais et du marché de l’automobile de luxe. Son réseau professionnel compte plus de 500 relations LinkedIn, avec une présence active sur Viadeo et GoToTheGrid. Il intervient fréquemment lors de conférences et d’ateliers sur des thématiques telles que la transmission d’entreprise, le management et l’innovation.

Informations administratives :
- Nom complet : Adrien Audibert
- Date de naissance : Février 1987
- Nationalité : Française
- Adresse professionnelle : 21 avenue Carnot, 33200 Bordeaux
- Société principale : Audibert & Co (SIREN 879854354)
- Activités : Conseil en gestion, négoce automobile, location, entretien de véhicules
- Mandats : Plusieurs mandats de direction liés à l’automobile et au conseil

Réputation et valeurs :
Adrien Audibert est apprécié pour son professionnalisme, sa discrétion et sa capacité à bâtir des relations de confiance durables. Il incarne des valeurs fortes d’exigence, de transparence, d'innovation et reste fidèle à ses racines bordelaises.

Analyse comportementale DISC :
Adrien présente un profil harmonieux entre Dominant, Influent et Conforme :
- 🔴 Dominant (D) : Leadership affirmé, esprit d'initiative, forte capacité à concrétiser des projets.
- 🟡 Influent (I) : Charisme naturel, aisance relationnelle, réseau professionnel étendu, interventions régulières en public.
- 🔵 Conforme (C) : Rigueur professionnelle, attention aux détails, prestations de haute qualité.
- 🟢 Stable (S) : Engagement local, fidélité à sa région et à ses passions, implication dans des projets régionaux.

Conclusion générale :
Adrien Audibert est un entrepreneur complet, innovant et inspirant. Il combine stratégie, passion, rigueur et valeurs humaines dans tous ses projets. Son parcours illustre parfaitement le profil d'un entrepreneur moderne et responsable, capable d’allier performance économique, excellence du service et engagement local.
"""

    # Si Adrien clique sur "Que penses-tu de moi"
    if user_message == "Que penses-tu de moi":
        custom_prompt = f"""
Tu es un expert en conseil stratégique pour entrepreneurs à haut potentiel.

À partir du profil suivant :
{special_context}

Donne ton analyse complète sur la personnalité, les forces principales, les atouts professionnels et le potentiel futur d'Adrien Audibert. 
Exprime ton analyse de manière humaine, valorisante et inspirante, comme un mentor de haut niveau. 
Sois sincère mais positif, sans rappeler que tu es une IA.
"""
        st.session_state.messages.append({"role": "user", "content": custom_prompt})
    else:
        st.session_state.messages.append({"role": "user", "content": user_message})

    # Appel à l'API OpenAI
    with st.spinner("Audrey réfléchit à votre situation..."):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages,
            max_tokens=1000
        )
        assistant_message = response.choices[0].message.content

    # Enregistrement de la réponse
    st.session_state.messages.append({"role": "assistant", "content": assistant_message})

    with st.chat_message("assistant"):
        st.write(assistant_message)

# --- Page Streamlit ---

inject_custom_css()
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
