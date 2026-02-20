import streamlit as st
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math
import time

st.set_page_config(page_title="Simulateur SVT", layout="centered")

# --- Configuration ultra-compacte ---
st.markdown("""
    <style>
    /* Réduction drastique des espaces entre les blocs */
    .block-container { padding-top: 1rem; padding-bottom: 0rem; }
    .stPlotlyChart { margin-bottom: -2rem; }
    div[data-testid="stVerticalBlock"] > div { padding-top: 0rem; padding-bottom: 0rem; }
    
    /* Titre plus petit */
    h1 { font-size: 1.4rem !important; margin-bottom: 0rem; }
    h3 { font-size: 1.1rem !important; margin-top: 0rem; margin-bottom: 0.5rem; }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)


# --- CONSTANTES ---
BEIGE = '#F5F5DC'
MARRON = '#5D3A1A'
COULEURS_INDIV = {'AA': '#F5F5DC', 'Aa': '#D2B48C', 'aa': '#5D3A1A'}

# --- INITIALISATION ---
if 'pop_init' not in st.session_state:
    # 10 Aa, 5 aa, 5 AA = 20 individus
    base = ['Aa']*10 + ['aa']*5 + ['AA']*5
    st.session_state.males = list(base)
    random.shuffle(st.session_state.males)
    st.session_state.femelles = list(base)
    random.shuffle(st.session_state.femelles)
    st.session_state.id_pere = None
    st.session_state.id_mere = None
    st.session_state.enfant = None
    st.session_state.alleles_choisis = None
    st.session_state.pop_init = True

# --- FONCTIONS DE DESSIN ---
def style_label(ax, x, y, texte, couleur='black'):
    ax.text(x, y, texte, ha='center', va='center', fontsize=9, fontweight='bold', 
            color=couleur, bbox=dict(facecolor='white', edgecolor='#CCCCCC', boxstyle='round,pad=0.3', alpha=0.9))

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
        # Surbrillance de l'allèle spécifique si tiré
        ec_a = 'gold' if (halo_allele is not None and i == halo_allele) else 'black'
        lw_a = 3 if (halo_allele is not None and i == halo_allele) else 0.5
        ax.add_patch(patches.Ellipse((x + dx, y), r*0.5, r*0.8, fc=c, ec=ec_a, lw=lw_a, zorder=3))
        txt_c = 'black' if a == 'A' else 'white'
        ax.text(x+dx, y, a, ha='center', va='center', fontsize=7, fontweight='bold', color=txt_c, zorder=4)

# --- INTERFACE ---
st.title("🧬 Étude de la transmission des allèles")

# Affichage des Populations
fig, ax = plt.subplots(figsize=(10, 5))
ax.set_xlim(-1, 11); ax.set_ylim(-1, 6); ax.axis('off')

style_label(ax, 5, 5.5, "POPULATION")
style_label(ax, 2, 4.8, "Hommes")
style_label(ax, 8, 4.8, "Femmes")

for i in range(20):
    # Hommes à gauche
    dessiner_indiv(ax, i%4, 4-(i//4)*0.8, st.session_state.males[i], souligne=(st.session_state.id_pere == i))
    # Femmes à droite
    dessiner_indiv(ax, 7+i%4, 4-(i//4)*0.8, st.session_state.femelles[i], souligne=(st.session_state.id_mere == i))
plt.tight_layout()
st.pyplot(fig)

# --- BOUTONS ---
col1, col2 = st.columns(2)

with col1:
    if st.button("👨 Tirer le père au hasard"):
        st.session_state.id_pere = random.randint(0, 19)
        st.session_state.enfant = None # Reset enfant si nouveau parent
        st.rerun()

with col2:
    if st.button("👩 Tirer la mère au hasard"):
        st.session_state.id_mere = random.randint(0, 19)
        st.session_state.enfant = None
        st.rerun()

# --- AFFICHAGE PARENTS TIRÉS ---
if st.session_state.id_pere is not None or st.session_state.id_mere is not None:
    fig2, ax2 = plt.subplots(figsize=(10, 3))
    ax2.set_xlim(-1, 11); ax2.set_ylim(0, 3); ax2.axis('off')
    
    if st.session_state.id_pere is not None:
        style_label(ax2, 2.5, 2.5, "père tiré au hasard")
        dessiner_indiv(ax2, 2.5, 1.2, st.session_state.males[st.session_state.id_pere], 
                       souligne=True, halo_allele=st.session_state.alleles_choisis[0] if st.session_state.enfant else None)
        
    if st.session_state.id_mere is not None:
        style_label(ax2, 7.5, 2.5, "mère tirée au hasard")
        dessiner_indiv(ax2, 7.5, 1.2, st.session_state.femelles[st.session_state.id_mere], 
                       souligne=True, halo_allele=st.session_state.alleles_choisis[1] if st.session_state.enfant else None)
    plt.tight_layout()
    st.pyplot(fig2)

# --- ÉTAPE ENFANT ---
if st.session_state.id_pere is not None and st.session_state.id_mere is not None:
    if st.button("🎲 Tirer les allèles au hasard"):
        with st.spinner('Méiose et fécondation...'):
            time.sleep(0.5)
            # On tire l'index de l'allèle (0 ou 1) chez chaque parent
            idx_p, idx_m = random.randint(0, 1), random.randint(0, 1)
            p_ge = st.session_state.males[st.session_state.id_pere]
            m_ge = st.session_state.femelles[st.session_state.id_mere]
            
            st.session_state.alleles_choisis = (idx_p, idx_m)
            st.session_state.enfant = "".join(sorted(p_ge[idx_p] + m_ge[idx_m]))
            st.rerun()

if st.session_state.enfant:
    fig3, ax3 = plt.subplots(figsize=(10, 2))
    ax3.set_xlim(-1, 11); ax3.set_ylim(0, 2); ax3.axis('off')
    style_label(ax3, 5, 1.5, "enfant")
    dessiner_indiv(ax3, 5, 0.5, st.session_state.enfant)
    plt.tight_layout()
    st.pyplot(fig3)
    
    if st.button("🔄 Recommencer"):
        st.session_state.id_pere = None
        st.session_state.id_mere = None
        st.session_state.enfant = None
        st.session_state.alleles_choisis = None
        st.rerun()
