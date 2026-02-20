import streamlit as st
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd

# --- CONFIGURATION ---
st.set_page_config(page_title="Simulateur SVT", layout="centered")

# --- STYLE CSS ---
st.markdown("""
    <style>
    .block-container { padding-top: 1rem; }
    .stButton>button { width: 100%; font-weight: bold; height: 3rem; }
    </style>
    """, unsafe_allow_html=True)

# --- COULEURS ---
C_AA, C_aa, C_Aa = '#FFFFFF', '#DBDBDB', '#FFFFFF'
COULEURS_INDIV = {'AA': C_AA, 'aa': C_aa, 'Aa': C_Aa}
COULEUR_A, COULEUR_a = '#F5F0F0', '#BEA19D'

# --- INITIALISATION ---
if 'males' not in st.session_state:
    base = ['Aa']*10 + ['aa']*5 + ['AA']*5
    m, f = list(base), list(base)
    random.shuffle(m); random.shuffle(f)
    st.session_state.males = m
    st.session_state.femelles = f
    st.session_state.id_pere = st.session_state.id_mere = st.session_state.enfant = st.session_state.alleles_choisis = None

# --- FONCTION DE DESSIN UNIQUE ---
def dessiner_indiv(ax, x, y, ge, souligne=False, halo_allele=None, taille=0.28):
    r = taille
    ec = 'gold' if souligne else 'black'
    lw = 2.5 if souligne else 0.8
    # Corps
    ax.add_patch(patches.Ellipse((x, y), r*2.2, r*1.5, fc=COULEURS_INDIV[ge], ec=ec, lw=lw, zorder=5))
    # Allèles
    for i, a in enumerate(list(ge)):
        dx = -0.11 if i == 0 else 0.11
        c = COULEUR_A if a == 'A' else COULEUR_a
        ec_a = 'gold' if (halo_allele is not None and i == halo_allele) else 'black'
        lw_a = 1.5 if (halo_allele is not None and i == halo_allele) else 0.4
        ax.add_patch(patches.Ellipse((x+dx, y), 0.16, 0.25, fc=c, ec=ec_a, lw=lw_a, zorder=6))
        ax.text(x+dx, y, a, ha='center', va='center', fontsize=6, fontweight='bold', zorder=7)

def dessiner_label(ax, x, y, texte, align='center'):
    ax.text(x, y, texte.upper(), ha=align, va='center', fontsize=7, fontweight='bold',
            bbox=dict(facecolor='white', edgecolor='#CCCCCC', boxstyle='round,pad=0.2', alpha=0.8), zorder=10)

# --- INTERFACE ---
st.header("🧬 Simulation de Croisement")

# Boutons en une seule ligne pour compacter
c1, c2, c3, c4 = st.columns(4)
with c1: 
    if st.button("👨 Père"): st.session_state.id_pere = random.randint(0, 19); st.session_state.enfant = None; st.rerun()
with c2: 
    if st.button("👩 Mère"): st.session_state.id_mere = random.randint(0, 19); st.session_state.enfant = None; st.rerun()
with c3: 
    if st.button("🎲 Enfant", disabled=(st.session_state.id_pere is None or st.session_state.id_mere is None)):
        st.session_state.alleles_choisis = (random.randint(0, 1), random.randint(0, 1))
        p = st.session_state.males[st.session_state.id_pere][st.session_state.alleles_choisis[0]]
        m = st.session_state.femelles[st.session_state.id_mere][st.session_state.alleles_choisis[1]]
        st.session_state.enfant = "".join(sorted(p + m))
        st.rerun()
with c4:
    if st.button("🔄 Reset"): st.session_state.id_pere = st.session_state.id_mere = st.session_state.enfant = None; st.rerun()

# --- GRAPHIQUE UNIQUE (HAUTE QUALITÉ) ---
fig, ax = plt.subplots(figsize=(9, 7), dpi=100) # DPI remonté pour la netteté
ax.set_xlim(-1, 11); ax.set_ylim(-1.8, 5.8); ax.axis('off')

# 1. Population
dessiner_label(ax, 5, 5.5, "Population")
for i in range(20):
    mx, my = i%5, 4.8-(i//5)*0.7
    dessiner_indiv(ax, mx, my, st.session_state.males[i], souligne=(st.session_state.id_pere == i))
    if st.session_state.id_pere == i:
        ax.annotate("", xy=(2.5, 1.2), xytext=(mx, my-0.2), arrowprops=dict(arrowstyle="->", color="gold", lw=1.5, alpha=0.7, connectionstyle="arc3,rad=-0.1"))

    fx, fy = 6+i%5, 4.8-(i//5)*0.7
    dessiner_indiv(ax, fx, fy, st.session_state.femelles[i], souligne=(st.session_state.id_mere == i))
    if st.session_state.id_mere == i:
        ax.annotate("", xy=(7.5, 1.2), xytext=(fx, fy-0.2), arrowprops=dict(arrowstyle="->", color="gold", lw=1.5, alpha=0.7, connectionstyle="arc3,rad=0.1"))

# 2. Zone Parents (même échelle)
if st.session_state.id_pere is not None:
    dessiner_label(ax, 0.8, 1.2, "Père", align='right')
    dessiner_indiv(ax, 2.5, 1.2, st.session_state.males[st.session_state.id_pere], souligne=True, halo_allele=st.session_state.alleles_choisis[0] if st.session_state.enfant else None)

if st.session_state.id_mere is not None:
    dessiner_label(ax, 9.2, 1.2, "Mère", align='left')
    dessiner_indiv(ax, 7.5, 1.2, st.session_state.femelles[st.session_state.id_mere], souligne=True, halo_allele=st.session_state.alleles_choisis[1] if st.session_state.enfant else None)

# 3. Zone Enfant et Flèches d'allèles
if st.session_state.enfant:
    dessiner_label(ax, 3.8, -1.0, "Enfant", align='right')
    dessiner_indiv(ax, 5, -1.0, st.session_state.enfant)
    ax.annotate("", xy=(4.9, -0.7), xytext=(2.5, 0.9), arrowprops=dict(arrowstyle="->", color="#BEA19D", lw=1.5, ls="--"))
    ax.annotate("", xy=(5.1, -0.7), xytext=(7.5, 0.9), arrowprops=dict(arrowstyle="->", color="#BEA19D", lw=1.5, ls="--"))

st.pyplot(fig, use_container_width=True)

# --- STATISTIQUES ---
st.markdown("---")
if st.button("🚀 Lancer 40 tirages rapides"):
    res = ["".join(sorted(random.choice(list(random.choice(st.session_state.males))) + random.choice(list(random.choice(st.session_state.femelles))))) for _ in range(40)]
    counts = {g: res.count(g) for g in ['AA', 'Aa', 'aa']}
    df = pd.DataFrame({'Génotype': ['AA', 'Aa', 'aa', 'Total'], 'Nombre': [counts['AA'], counts['Aa'], counts['aa'], 40], 'Fréquence (%)': [counts['AA']/0.4, counts['Aa']/0.4, counts['aa']/0.4, 100]})
    st.table(df)
