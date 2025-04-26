import streamlit as st

# Titre de l'app
st.title("Hello World 🚀")

# Message interactif
name = st.text_input("Entrez votre prénom :")

if st.button("Valider"):
    if name:
        st.success(f"Bonjour {name} ! 🌟 Ravi de voyager avec toi dans le monde du déploiement web avec Streamlit !")
    else:
        st.warning("N'oublie pas d'entrer ton prénom avant de valider !")
