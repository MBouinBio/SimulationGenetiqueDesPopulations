import streamlit as st
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Simulateur Génétique SVT", layout="centered")

# --- CSS ULTRA-COMPACT ---
st.markdown("""
    <style>
    /* Supprime les marges inutiles en haut et entre les blocs */
    .block-container { padding-top: 1rem; padding-bottom: 0rem; max-width: 900px; }
    div[data-testid="stVerticalBlock"] > div { padding-top: 0rem; padding-bottom: 0.2rem; }
    
    /* Titre et sous-titres compacts */
    h1 { font-size: 1.4rem !important; margin-bottom: 0.5rem; text-align: center; }
    
    /* Cache le header et le footer Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Style des boutons pour qu'ils soient moins hauts */
    .stButton>button { width: 100%; padding: 0px; height: 2.5rem; }
    </style>
    """, unsafe_allow_html=True)

# --- CONSTANTES ---
BEIGE = '#F5F5DC'
MARRON = '#5D3A1A'
COULEURS_INDIV = {'AA': 'ad902528', 'Aa': '#ad00001b', 'aa': '#ad00004e'}

# --- INITIALISATION DE LA SESSION ---
if 'pop_init' not in st.session_state:
    # Population fixe : 10 Aa, 5 aa, 5 AA
    base = ['Aa']*10 + ['aa']*5 + ['AA']*5
    st.session_state.males = list(base)
    random.shuffle(st.session_state.males)
    st.session_state.femelles = list(base)
    random.shuffle(st.session_state.femelles)
    
    # États des tirages
    st.session_state.id_pere = None
    st.session_state.id_mere = None
    st.session_state.enfant = None
    st.session_state.alleles_choisis = None
    st.session_state.pop_init = True

# --- FONCTIONS DE DESSIN ---
def style_label(ax, x, y, texte, couleur='black'):
    ax.text(x, y, texte.upper(), ha='center', va='center', fontsize=8, fontweight='bold', 
            color=couleur, bbox=dict(facecolor='white', edgecolor='#CCCCCC', boxstyle='round,pad=0.2', alpha=0.8))

def dessiner_indiv(ax, x, y, ge, souligne=False, halo_allele=None):
    r = 0.35
    ec = 'gold' if souligne else 'black'
    lw = 4 if souligne else 1
    # Corps
    ax.add_patch(patches.Ellipse((x, y), r*2.2, r*1.5, fc=COULEURS_INDIV[ge], ec=ec, lw=lw, zorder=2))
    # Allèles
    for i, a in enumerate(list(ge)):
        dx = -0.3 * r if i == 0 else 0.3 * r
        c = BEIGE if a == 'A' else MARRON
        ec_a = 'gold' if (halo_allele is not None and i == halo_allele) else 'black'
        lw_a = 3 if (halo_allele is not None and i == halo_allele) else 0.5
        ax.add_patch(patches.Ellipse((x + dx, y), r*0.5, r*0.8, fc=c, ec=ec_a, lw=lw_a, zorder=3))
        txt_c = 'black' if a == 'A' else 'white'
        ax.text(x+dx, y, a, ha='center', va='center', fontsize=7, fontweight='bold', color=txt_c, zorder=4)

# --- CORPS DE L'APPLICATION ---
st.title("🧬 Étude de la transmission des allèles")

# 1. GRAPHIQUE POPULATION (Toujours visible)
fig1, ax1 = plt.subplots(figsize=(10, 3.5))
ax1.set_xlim(-1, 11); ax1.set_ylim(-0.5, 5); ax1.axis('off')

style_label(ax1, 5, 4.8, "Population")
style_label(ax1, 2, 4.2, "Hommes")
style_label(ax1, 8, 4.2, "Femmes")

for i in range(20):
    # Hommes à gauche (5 colonnes x 4 lignes)
    dessiner_indiv(ax1, i%5, 3.2-(i//5)*0.8, st.session_state.males[i], souligne=(st.session_state.id_pere == i))
    # Femmes à droite
    dessiner_indiv(ax1, 6+i%5, 3.2-(i//5)*0.8, st.session_state.femelles[i], souligne=(st.session_state.id_mere == i))

plt.tight_layout()
st.pyplot(fig1)

# 2. BOUTONS D'ACTION (Sur une ligne)
c1, c2, c3, c4 = st.columns(4)
with c1:
    if st.button("👨 Père"):
        st.session_state.id_pere = random.randint(0, 19)
        st.session_state.enfant = None
        st.rerun()
with c2:
    if st.button("👩 Mère"):
        st.session_state.id_mere = random.randint(0, 19)
        st.session_state.enfant = None
        st.rerun()
with c3:
    # Désactivé si parents non choisis
    desactive = (st.session_state.id_pere is None or st.session_state.id_mere is None)
    if st.button("🎲 Enfant", disabled=desactive):
        idx_p, idx_m = random.randint(0, 1), random.randint(0, 1)
        p_ge = st.session_state.males[st.session_state.id_pere]
        m_ge = st.session_state.femelles[st.session_state.id_mere]
        st.session_state.alleles_choisis = (idx_p, idx_m)
        st.session_state.enfant = "".join(sorted(p_ge[idx_p] + m_ge[idx_m]))
        st.rerun()
with c4:
    if st.button("🔄 Reset"):
        st.session_state.id_pere = None
        st.session_state.id_mere = None
        st.session_state.enfant = None
        st.session_state.alleles_choisis = None
        st.rerun()

# 3. GRAPHIQUE RÉSULTAT (Fusionné Parents + Enfant)
if st.session_state.id_pere is not None or st.session_state.id_mere is not None:
    fig2, ax2 = plt.subplots(figsize=(10, 3.2))
    ax2.set_xlim(-1, 11); ax2.set_ylim(-1.5, 3); ax2.axis('off')

    if st.session_state.id_pere is not None:
        style_label(ax2, 2.5, 2.6, "père tiré au hasard")
        dessiner_indiv(ax2, 2.5, 1.4, st.session_state.males[st.session_state.id_pere], 
                       souligne=True, halo_allele=st.session_state.alleles_choisis[0] if st.session_state.enfant else None)
        
    if st.session_state.id_mere is not None:
        style_label(ax2, 7.5, 2.6, "mère tirée au hasard")
        dessiner_indiv(ax2, 7.5, 1.4, st.session_state.femelles[st.session_state.id_mere], 
                       souligne=True, halo_allele=st.session_state.alleles_choisis[1] if st.session_state.enfant else None)

    if st.session_state.enfant:
        style_label(ax2, 5, 0.2, "enfant")
        dessiner_indiv(ax2, 5, -0.6, st.session_state.enfant)
    
    plt.tight_layout()
    st.pyplot(fig2)
else:
    st.info("Utilisez les boutons ci-dessus pour simuler un croisement.")
