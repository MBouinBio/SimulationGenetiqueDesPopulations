import streamlit as st
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math

# Configuration de la page
st.set_page_config(page_title="Simulateur Hardy-Weinberg", layout="centered")

# --- CSS pour cacher le menu Streamlit et épurer l'interface ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_status_code=True)

st.title("🧬 Simulation de la Reproduction Sexuée")
st.write("Choisissez les paramètres dans la barre à gauche et observez la transmission des allèles.")

# --- BARRE LATÉRALE ---
with st.sidebar:
    st.header("⚙️ Paramètres")
    p_freq = st.slider("Fréquence de l'allèle A (beige)", 0.0, 1.0, 0.5, 0.05)
    taille_pop = st.number_input("Taille totale de la population", 4, 100, 20, 2)
    st.divider()
    if st.button("♻️ Générer une nouvelle population"):
        st.session_state.pop_init = False

# --- CONSTANTES VISUELLES ---
COULEUR_A, COULEUR_a = '#F5F5DC', '#8B4513'
COULEURS_INDIV = {'AA': '#FF595E', 'Aa': '#8AC926', 'aa': '#1982C4'}

def dessiner_individu(ax, x, y, ge, surlignage=None):
    r = 0.35
    edge = 'gold' if surlignage else 'black'
    lw = 4 if surlignage else 1
    ax.add_patch(patches.Ellipse((x, y), r*2.2, r*1.5, fc=COULEURS_INDIV[ge], ec=edge, lw=lw, zorder=2))
    for i, a in enumerate(list(ge)):
        dx = -0.3 * r if i == 0 else 0.3 * r
        c = COULEUR_A if a == 'A' else COULEUR_a
        ax.add_patch(patches.Ellipse((x + dx, y), r*0.5, r*0.8, fc=c, ec='black', lw=0.5, zorder=3))
        col_t = 'black' if a == 'A' else 'white'
        ax.text(x+dx, y, a, ha='center', va='center', fontsize=7, fontweight='bold', color=col_t, zorder=4)

def style_label(ax, x, y, texte, couleur='black'):
    ax.text(x, y, texte, ha='center', va='center', fontsize=10, fontweight='bold', 
            color=couleur, bbox=dict(facecolor='white', edgecolor='#CCCCCC', boxstyle='round,pad=0.3', alpha=0.9), zorder=5)

# --- INITIALISATION ---
if 'pop_init' not in st.session_state or st.session_state.pop_init == False:
    nb = taille_pop // 2
    w = [p_freq**2, 2*p_freq*(1-p_freq), (1-p_freq)**2]
    st.session_state.males = random.choices(['AA', 'Aa', 'aa'], weights=w, k=nb)
    st.session_state.femelles = random.choices(['AA', 'Aa', 'aa'], weights=w, k=nb)
    st.session_state.pop_init = True

# --- BOUTON D'ACTION ---
if st.button("👶 Tirer un couple et créer un descendant", type="primary"):
    m, f = st.session_state.males, st.session_state.femelles
    im, ifem = random.randint(0, len(m)-1), random.randint(0, len(f)-1)
    père, mère = m[im], f[ifem]
    a1, a2 = random.choice(list(père)), random.choice(list(mère))
    enfant = "".join(sorted(a1 + a2))

    # Dessin
    nb_l = math.ceil(len(m)/5)
    fig, ax = plt.subplots(figsize=(10, 6 + nb_l*0.5))
    ax.set_xlim(-1, 11); ax.set_ylim(-2.5, 4 + nb_l)
    ax.axis('off')

    # Population
    style_label(ax, 2, 3.5+nb_l, "MÂLES ♂")
    style_label(ax, 8, 3.5+nb_l, "FEMELLES ♀")
    for i in range(len(m)):
        dessiner_individu(ax, i%5, 3+(nb_l-(i//5)), m[i], surlignage=(i==im))
        dessiner_individu(ax, 6+(i%5), 3+(nb_l-(i//5)), f[i], surlignage=(i==ifem))

    # Parents et Enfant
    style_label(ax, 2.5, 1.8, "PÈRE", couleur='blue')
    dessiner_individu(ax, 2.5, 1, père, surlignage=True)
    style_label(ax, 7.5, 1.8, "MÈRE", couleur='magenta')
    dessiner_individu(ax, 7.5, 1, mère, surlignage=True)
    
    # Gamètes
    for x_p, al in [(2.5, a1), (7.5, a2)]:
        c = COULEUR_A if al == 'A' else COULEUR_a
        ax.add_patch(patches.Circle((x_p, 0.1), 0.2, fc=c, ec='black', zorder=3))
        ax.text(x_p, 0.1, al, ha='center', va='center', fontweight='bold', color=('black' if al=='A' else 'white'), zorder=4)

    style_label(ax, 5, -1.5, f"DESCENDANT : {enfant}")
    dessiner_individu(ax, 5, -0.8, enfant)
    
    st.pyplot(fig)
else:
    st.info("Cliquez sur le bouton pour simuler un croisement aléatoire.")
