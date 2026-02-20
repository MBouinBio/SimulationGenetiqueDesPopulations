import streamlit as st
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Simulateur Génétique SVT", layout="wide")

# --- CSS POUR COMPACTAGE MAXIMAL ---
st.markdown("""
    <style>
    .block-container { padding-top: 0.5rem; padding-bottom: 0rem; }
    h1 { font-size: 1.2rem !important; margin-bottom: 0.2rem; text-align: left; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    /* Style des boutons verticaux */
    .stButton>button { width: 100%; height: 3rem; margin-bottom: 0.5rem; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- COULEURS ---
C_AA = '#FFFFFF'
C_aa = '#DBDBDB'
C_Aa = '#FFFFFF'
COULEURS_INDIV = {'AA': C_AA, 'aa': C_aa, 'Aa': C_Aa}
COULEUR_A = '#F5F0F0'
COULEUR_a = '#BEA19D'

# --- INITIALISATION ---
if 'males' not in st.session_state:
    base = ['Aa']*10 + ['aa']*5 + ['AA']*5
    st.session_state.males = list(base); random.shuffle(st.session_state.males)
    st.session_state.femelles = list(base); random.shuffle(st.session_state.femelles)
    st.session_state.id_pere = None
    st.session_state.id_mere = None
    st.session_state.enfant = None
    st.session_state.alleles_choisis = None

# --- FONCTIONS DE DESSIN ---
def dessiner_label(ax, x, y, texte, align='center'):
    ax.text(x, y, texte.upper(), ha=align, va='center', fontsize=7, fontweight='bold',
            bbox=dict(facecolor='white', edgecolor='#CCCCCC', boxstyle='round,pad=0.2', alpha=0.8), zorder=10)

def dessiner_indiv(ax, x, y, ge, souligne=False, halo_allele=None):
    r = 0.28
    ec = 'gold' if souligne else 'black'
    lw = 2.5 if souligne else 0.8
    ax.add_patch(patches.Ellipse((x, y), r*2.2, r*1.5, fc=COULEURS_INDIV[ge], ec=ec, lw=lw, zorder=5))
    for i, a in enumerate(list(ge)):
        dx = -0.11 if i == 0 else 0.11
        c = COULEUR_A if a == 'A' else COULEUR_a
        ec_a = 'gold' if (halo_allele is not None and i == halo_allele) else 'black'
        lw_a = 1.5 if (halo_allele is not None and i == halo_allele) else 0.4
        ax.add_patch(patches.Ellipse((x+dx, y), 0.16, 0.25, fc=c, ec=ec_a, lw=lw_a, zorder=6))
        ax.text(x+dx, y, a, ha='center', va='center', fontsize=6, fontweight='bold', zorder=7)

# --- MISE EN PAGE : GRAPHIQUE À GAUCHE, BOUTONS À DROITE ---
st.title("🧬 Transmission des allèles")
col_graph, col_btns = st.columns([4, 1])

with col_btns:
    st.write("### Actions")
    if st.button("👨 Père"):
        st.session_state.id_pere = random.randint(0, 19)
        st.session_state.enfant = None
        st.rerun()
    if st.button("👩 Mère"):
        st.session_state.id_mere = random.randint(0, 19)
        st.session_state.enfant = None
        st.rerun()
    desactive = (st.session_state.id_pere is None or st.session_state.id_mere is None)
    if st.button("🎲 Enfant", disabled=desactive):
        st.session_state.alleles_choisis = (random.randint(0, 1), random.randint(0, 1))
        p = st.session_state.males[st.session_state.id_pere][st.session_state.alleles_choisis[0]]
        m = st.session_state.femelles[st.session_state.id_mere][st.session_state.alleles_choisis[1]]
        st.session_state.enfant = "".join(sorted(p + m))
        st.rerun()
    if st.button("🔄 Reset"):
        st.session_state.id_pere = st.session_state.id_mere = st.session_state.enfant = st.session_state.alleles_choisis = None
        st.rerun()

with col_graph:
    # --- GRAPHIQUE COMPACTÉ ---
    fig, ax = plt.subplots(figsize=(9, 7), dpi=10)
    # Réduction des limites Y pour tasser le tout
    ax.set_xlim(-1, 11); ax.set_ylim(-2.5, 5.5); ax.axis('off')

    # 1. Population (Haut)
    dessiner_label(ax, 5, 5.2, "Population")
    for i in range(20):
        # Hommes
        mx, my = i%5, 4.4-(i//5)*0.65
        dessiner_indiv(ax, mx, my, st.session_state.males[i], souligne=(st.session_state.id_pere == i))
        if st.session_state.id_pere == i:
            ax.annotate("", xy=(2.5, 1.2), xytext=(mx, my-0.2), arrowprops=dict(arrowstyle="->", color="gold", lw=1.5, alpha=0.6, connectionstyle="arc3,rad=-0.1"))
        # Femmes
        fx, fy = 6+i%5, 4.4-(i//5)*0.65
        dessiner_indiv(ax, fx, fy, st.session_state.femelles[i], souligne=(st.session_state.id_mere == i))
        if st.session_state.id_mere == i:
            ax.annotate("", xy=(7.5, 1.2), xytext=(fx, fy-0.2), arrowprops=dict(arrowstyle="->", color="gold", lw=1.5, alpha=0.6, connectionstyle="arc3,rad=0.1"))

    # 2. Parents (Milieu - plus proche de la population)
    if st.session_state.id_pere is not None:
        dessiner_label(ax, 0.8, 1.2, "Père", align='right')
        dessiner_indiv(ax, 2.5, 1.2, st.session_state.males[st.session_state.id_pere], souligne=True, halo_allele=st.session_state.alleles_choisis[0] if st.session_state.enfant else None)
    if st.session_state.id_mere is not None:
        dessiner_label(ax, 9.2, 1.2, "Mère", align='left')
        dessiner_indiv(ax, 7.5, 1.2, st.session_state.femelles[st.session_state.id_mere], souligne=True, halo_allele=st.session_state.alleles_choisis[1] if st.session_state.enfant else None)

    # 3. Enfant (Bas - très proche des parents)
    if st.session_state.enfant:
        dessiner_label(ax, 3.8, -1.0, "Enfant", align='right')
        dessiner_indiv(ax, 5, -1.0, st.session_state.enfant)
        ax.annotate("", xy=(4.9, -0.7), xytext=(2.5, 0.9), arrowprops=dict(arrowstyle="->", color="#BEA19D", lw=1.2, ls="--"))
        ax.annotate("", xy=(5.1, -0.7), xytext=(7.5, 0.9), arrowprops=dict(arrowstyle="->", color="#BEA19D", lw=1.2, ls="--"))

    plt.tight_layout(pad=0)
    st.pyplot(fig)
