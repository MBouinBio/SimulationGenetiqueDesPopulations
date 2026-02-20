import streamlit as st
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd

# --- CONFIGURATION ---
st.set_page_config(page_title="Simulateur Génétique SVT", layout="wide")

# --- CSS : TITRE ET COMPACTAGE ---
st.markdown("""
    <style>
    .block-container { padding-top: 0.5rem; padding-bottom: 0rem; }
    h1 { font-size: 1.0rem !important; margin-bottom: 0rem; padding-bottom: 0rem; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .stButton>button { width: 100%; height: 3rem; margin-bottom: 0.4rem; font-weight: bold; }
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

# --- FONCTIONS DE DESSIN ---
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

def dessiner_label(ax, x, y, texte, align='center'):
    ax.text(x, y, texte.upper(), ha=align, va='center', fontsize=7, fontweight='bold',
            bbox=dict(facecolor='white', edgecolor='#CCCCCC', boxstyle='round,pad=0.1', alpha=0.8), zorder=10)

# --- INTERFACE ---
st.title("🧬 Transmission des allèles")
col_graph, col_btns = st.columns([4, 1])

with col_btns:
    st.write("### Actions")
    dis_p = st.session_state.id_pere is not None
    dis_m = st.session_state.id_mere is not None
    if st.button("👨 Père", disabled=dis_p):
        st.session_state.id_pere = random.randint(0, 19)
        st.rerun()
    if st.button("👩 Mère", disabled=dis_m):
        st.session_state.id_mere = random.randint(0, 19)
        st.rerun()
    dis_e = (st.session_state.id_pere is None or st.session_state.id_mere is None or st.session_state.enfant is not None)
    if st.button("👶 Enfant", disabled=dis_e):
        st.session_state.alleles_choisis = (random.randint(0, 1), random.randint(0, 1))
        p = st.session_state.males[st.session_state.id_pere][st.session_state.alleles_choisis[0]]
        m = st.session_state.femelles[st.session_state.id_mere][st.session_state.alleles_choisis[1]]
        st.session_state.enfant = "".join(sorted(p + m))
        st.rerun()
    if st.button("🔄 Reset"):
        st.session_state.id_pere = st.session_state.id_mere = st.session_state.enfant = st.session_state.alleles_choisis = None
        st.rerun()

with col_graph:
    # Figure compactée
    fig, ax = plt.subplots(figsize=(9, 4.5), dpi=100)
    # On réduit encore le plafond (Ymax=4.5) et le plancher (Ymin=-1.2)
    ax.set_xlim(-1, 11); ax.set_ylim(-1.2, 4.5); ax.axis('off')

    # 1. Population (Encore plus proche du haut)
    dessiner_label(ax, 5, 4.3, "Population") 
    for i in range(20):
        # Ecart vertical réduit de 0.65 à 0.48
        # Hommes
        mx, my = i%5, 3.9-(i//5)*0.48
        dessiner_indiv(ax, mx, my, st.session_state.males[i], souligne=(st.session_state.id_pere == i))
        if st.session_state.id_pere == i:
            ax.annotate("", xy=(2.5, 1.1), xytext=(mx, my-0.2), arrowprops=dict(arrowstyle="->", color="gold", lw=1.5, alpha=0.6))
        
        # Femmes
        fx, fy = 6+i%5, 3.9-(i//5)*0.48
        dessiner_indiv(ax, fx, fy, st.session_state.femelles[i], souligne=(st.session_state.id_mere == i))
        if st.session_state.id_mere == i:
            ax.annotate("", xy=(7.5, 1.1), xytext=(fx, fy-0.2), arrowprops=dict(arrowstyle="->", color="gold", lw=1.5, alpha=0.6))

    # 2. Parents (Positionnés juste sous la population compactée)
    if st.session_state.id_pere is not None:
        dessiner_label(ax, 0.8, 1.1, "Père", align='right')
        dessiner_indiv(ax, 2.5, 1.1, st.session_state.males[st.session_state.id_pere], souligne=True, 
                       halo_allele=st.session_state.alleles_choisis[0] if st.session_state.enfant else None)
    if st.session_state.id_mere is not None:
        dessiner_label(ax, 9.2, 1.1, "Mère", align='left')
        dessiner_indiv(ax, 7.5, 1.1, st.session_state.femelles[st.session_state.id_mere], souligne=True, 
                       halo_allele=st.session_state.alleles_choisis[1] if st.session_state.enfant else None)

    # 3. Enfant (Remonté au maximum)
    if st.session_state.enfant:
        dessiner_label(ax, 3.8, -0.4, "Enfant", align='right')
        dessiner_indiv(ax, 5, -0.4, st.session_state.enfant)
        ax.annotate("", xy=(4.9, -0.2), xytext=(2.5, 0.85), arrowprops=dict(arrowstyle="->", color="#BEA19D", lw=1.2, ls="--"))
        ax.annotate("", xy=(5.1, -0.2), xytext=(7.5, 0.85), arrowprops=dict(arrowstyle="->", color="#BEA19D", lw=1.2, ls="--"))

    plt.tight_layout(pad=0)
    st.pyplot(fig)

# --- STATISTIQUES ---
st.markdown("---")
if st.button("🚀 Lancer 40 tirages rapides"):
    res = ["".join(sorted(random.choice(list(random.choice(st.session_state.males))) + random.choice(list(random.choice(st.session_state.femelles))))) for _ in range(40)]
    c = {g: res.count(g) for g in ['AA', 'Aa', 'aa']}
    df = pd.DataFrame({'Génotype': ['AA', 'Aa', 'aa', 'Total'], 'Nombre': [c['AA'], c['Aa'], c['aa'], 40], 'Fréquence (%)': [c['AA']/0.4, c['Aa']/0.4, c['aa']/0.4, 100.0]})
    st.table(df)
