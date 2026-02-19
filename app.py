import streamlit as st
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math

# Configuration de la page
st.set_page_config(page_title="Simulateur Hardy-Weinberg", layout="centered")

# --- CSS pour épurer l'interface ---
st.markdown("<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}</style>", unsafe_allow_html=True)

st.title("🧬 Simulation de la Reproduction Sexuée")

# --- BARRE LATÉRALE ---
with st.sidebar:
    st.header("⚙️ Paramètres")
    p_freq = st.slider("Fréquence de l'allèle A (beige)", 0.0, 1.0, 0.5, 0.05)
    taille_pop = st.number_input("Taille totale de la population", 4, 100, 20, 2)
    st.divider()
    if st.button("♻️ Générer une nouvelle population"):
        st.session_state.pop_init = False
        st.rerun()

# --- FONCTIONS ET CONSTANTES ---
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

# --- INITIALISATION DE LA POPULATION ---
if 'pop_init' not in st.session_state or st.session_state.pop_init == False:
    nb = taille_pop // 2
    w = [p_freq**2, 2*p_freq*(1-p_freq), (1-p_freq)**2]
    st.session_state.males = random.choices(['AA', 'Aa', 'aa'], weights=w, k=nb)
    st.session_state.femelles = random.choices(['AA', 'Aa', 'aa'], weights=w, k=nb)
    st.session_state.pop_init = True
    st.session_state.dernier_tirage = None

# --- 1. AFFICHAGE DE LA POPULATION (FIXE) ---
st.subheader("👥 Population de référence")
nb_l = math.ceil(len(st.session_state.males)/5)
fig_pop, ax_pop = plt.subplots(figsize=(10, nb_l * 0.8 + 1))
ax_pop.set_xlim(-1, 11); ax_pop.set_ylim(0, nb_l + 1)
ax_pop.axis('off')

style_label(ax_pop, 2, nb_l + 0.5, "MÂLES ♂")
style_label(ax_pop, 8, nb_l + 0.5, "FEMELLES ♀")

for i in range(len(st.session_state.males)):
    # Mâles
    dessiner_individu(ax_pop, i%5, nb_l - (i//5), st.session_state.males[i])
    # Femelles
    dessiner_individu(ax_pop, 6+(i%5), nb_l - (i//5), st.session_state.femelles[i])

st.pyplot(fig_pop)

st.divider()

# --- 2. ZONE DE CROISEMENT (DYNAMIQUE) ---
st.subheader("🐣 Nouveau Croisement")
placeholder = st.empty()

if st.button("👶 Tirer un couple et créer un descendant", type="primary"):
    m, f = st.session_state.males, st.session_state.femelles
    im, ifem = random.randint(0, len(m)-1), random.randint(0, len(f)-1)
    père, mère = m[im], f[ifem]
    a1, a2 = random.choice(list(père)), random.choice(list(mère))
    enfant = "".join(sorted(a1 + a2))

    # On dessine uniquement le croisement
    fig_cr, ax_cr = plt.subplots(figsize=(10, 4))
    ax_cr.set_xlim(-1, 11); ax_cr.set_ylim(-2, 3)
    ax_cr.axis('off')

    # Parents
    style_label(ax_cr, 2.5, 2.5, "PÈRE CHOISI", couleur='blue')
    dessiner_individu(ax_cr, 2.5, 1.5, père, surlignage=True)
    style_label(ax_cr, 7.5, 2.5, "MÈRE CHOISIE", couleur='magenta')
    dessiner_individu(ax_cr, 7.5, 1.5, mère, surlignage=True)
    
    # Gamètes
    for x_p, al in [(2.5, a1), (7.5, a2)]:
        c = COULEUR_A if al == 'A' else COULEUR_a
        ax_cr.add_patch(patches.Circle((x_p, 0.5), 0.25, fc=c, ec='black', zorder=3))
        ax_cr.text(x_p, 0.5, al, ha='center', va='center', fontweight='bold', color=('black' if al=='A' else 'white'), zorder=4)

    # Descendant
    style_label(ax_cr, 5, -1.5, f"DESCENDANT OBTENU : {enfant}")
    dessiner_individu(ax_cr, 5, -0.5, enfant)
    
    placeholder.pyplot(fig_cr)
else:
    placeholder.info("En attente d'un tirage au sort...")
