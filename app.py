import streamlit as st
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd

# --- CONFIGURATION ---
st.set_page_config(page_title="Simulateur SVT Rapide", layout="wide")

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

# --- FONCTION DE DESSIN ---
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

# --- BLOC 1 : POPULATION (MIS EN CACHE) ---
@st.cache_data
def afficher_population(males, femelles, id_pere, id_mere):
    fig, ax = plt.subplots(figsize=(10, 3), dpi=90)
    ax.set_xlim(-0.5, 11.5); ax.set_ylim(2.5, 5.5); ax.axis('off')
    
    for i in range(20):
        # Hommes
        mx, my = i%5, 4.8-(i//5)*0.7
        dessiner_indiv(ax, mx, my, males[i], souligne=(id_pere == i))
        # Femmes
        fx, fy = 6+i%5, 4.8-(i//5)*0.7
        dessiner_indiv(ax, fx, fy, femelles[i], souligne=(id_mere == i))
    
    plt.tight_layout(pad=0)
    return fig

# --- INTERFACE ---
st.title("🧬 Transmission des allèles")
col_graph, col_btns = st.columns([4, 1])

with col_btns:
    st.write("### Actions")
    # Verrouillage : Père et Mère désactivés si déjà choisis
    dis_p = st.session_state.id_pere is not None
    dis_m = st.session_state.id_mere is not None
    
    if st.button("👨 Père", disabled=dis_p):
        st.session_state.id_pere = random.randint(0, 19)
        st.rerun()
    if st.button("👩 Mère", disabled=dis_m):
        st.session_state.id_mere = random.randint(0, 19)
        st.rerun()
    
    dis_e = (st.session_state.id_pere is None or st.session_state.id_mere is None or st.session_state.enfant is not None)
    if st.button("🎲 Enfant", disabled=dis_e):
        st.session_state.alleles_choisis = (random.randint(0, 1), random.randint(0, 1))
        p = st.session_state.males[st.session_state.id_pere][st.session_state.alleles_choisis[0]]
        m = st.session_state.femelles[st.session_state.id_mere][st.session_state.alleles_choisis[1]]
        st.session_state.enfant = "".join(sorted(p + m))
        st.rerun()
    
    if st.button("🔄 Reset"):
        st.session_state.id_pere = st.session_state.id_mere = st.session_state.enfant = st.session_state.alleles_choisis = None
        st.rerun()

with col_graph:
    # 1. Le bloc de la population (Utilise le cache)
    fig_pop = afficher_population(tuple(st.session_state.males), tuple(st.session_state.femelles), st.session_state.id_pere, st.session_state.id_mere)
    st.pyplot(fig_pop)

    # 2. Le bloc des parents choisis (Recalculé car très léger)
    if st.session_state.id_pere is not None or st.session_state.id_mere is not None:
        fig_par, ax_par = plt.subplots(figsize=(10, 1.2), dpi=90)
        ax_par.set_xlim(-0.5, 11.5); ax_par.set_ylim(0.5, 1.5); ax_par.axis('off')
        
        if st.session_state.id_pere is not None:
            dessiner_indiv(ax_par, 2.5, 1, st.session_state.males[st.session_state.id_pere], souligne=True, 
                           halo_allele=st.session_state.alleles_choisis[0] if st.session_state.enfant else None)
        if st.session_state.id_mere is not None:
            dessiner_indiv(ax_par, 7.5, 1, st.session_state.femelles[st.session_state.id_mere], souligne=True, 
                           halo_allele=st.session_state.alleles_choisis[1] if st.session_state.enfant else None)
        st.pyplot(fig_par)

    # 3. Le bloc de l'enfant
    if st.session_state.enfant:
        fig_enf, ax_enf = plt.subplots(figsize=(10, 1.2), dpi=90)
        ax_enf.set_xlim(-0.5, 11.5); ax_enf.set_ylim(-0.5, 0.5); ax_enf.axis('off')
        dessiner_indiv(ax_enf, 5, 0, st.session_state.enfant)
        st.pyplot(fig_enf)

# --- STATISTIQUES (PANDAS) ---
st.markdown("---")
if st.button("🚀 Lancer 40 tirages rapides"):
    res = ["".join(sorted(random.choice(list(random.choice(st.session_state.males))) + random.choice(list(random.choice(st.session_state.femelles))))) for _ in range(40)]
    df = pd.DataFrame({'Génotype': ['AA', 'Aa', 'aa', 'Total'], 'Nombre': [res.count('AA'), res.count('Aa'), res.count('aa'), 40]})
    st.table(df)
