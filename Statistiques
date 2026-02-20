import streamlit as st
import random
import pandas as pd

# --- CONFIGURATION ---
st.set_page_config(page_title="Résultats de 40 Tirages", layout="centered")

st.title("📊 Simulation de 40 croisements")
st.write("Ce programme tire 40 couples au hasard dans la population initiale et comptabilise les génotypes des enfants.")

# --- DÉFINITION DE LA POPULATION INITIALE ---
# 10 Aa, 5 AA, 5 aa pour chaque sexe (total 20 de chaque)
hommes = ['Aa']*10 + ['AA']*5 + ['aa']*5
femmes = ['Aa']*10 + ['AA']*5 + ['aa']*5

if st.button("🚀 Lancer les 40 simulations"):
    resultats = []

    for i in range(40):
        # 1. Tirage aléatoire des parents
        pere = random.choice(hommes)
        mere = random.choice(femmes)
        
        # 2. Tirage aléatoire de l'allèle transmis par chaque parent
        allele_pere = random.choice(list(pere))
        allele_mere = random.choice(list(mere))
        
        # 3. Formation du génotype de l'enfant (trié pour cohérence, ex: 'aA' devient 'Aa')
        enfant = "".join(sorted(allele_pere + allele_mere))
        resultats.append(enfant)

    # --- COMPTAGE DES RÉSULTATS ---
    total_AA = resultats.count('AA')
    total_Aa = resultats.count('Aa')
    total_aa = resultats.count('aa')

    # --- AFFICHAGE SOUS FORME DE TABLEAU ---
    df = pd.DataFrame({
        'Génotype': ['AA', 'Aa', 'aa', 'TOTAL'],
        'Nombre d\'enfants': [total_AA, total_Aa, total_aa, 40],
        'Fréquence (%)': [
            (total_AA/40)*100, 
            (total_Aa/40)*100, 
            (total_aa/40)*100, 
            100
        ]
    })

    # On utilise st.table pour un rendu fixe et clair sans scroll
    st.table(df)

    # --- PETIT RAPPEL THÉORIQUE ---
    st.info(f"""
    **Analyse rapide :**
    - Les homozygotes dominants (AA) représentent {total_AA} enfants.
    - Les hétérozygotes (Aa) représentent {total_Aa} enfants.
    - Les homozygotes récessifs (aa) représentent {total_aa} enfants.
    """)
else:
    st.write("Cliquez sur le bouton pour générer les données.")
