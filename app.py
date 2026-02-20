import streamlit as st
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# --- CONFIGURATION ---
st.set_page_config(page_title="Simulateur SVT", layout="centered")

# --- COULEURS ---
C_AA = '#FFFFFF' # Blanc
C_aa = '#FF4D4D' # Rouge clair
C_Aa = '#FFCCCC' # Rouge très clair
COULEURS_INDIV = {'AA': C_AA, 'aa': C_aa, 'Aa': C_Aa}
COULEUR_A = '#FFFFFF'
COULEUR_a = '#FF4D4D'

# --- INITIALISATION ---
if 'males' not in st.session_state:
    base = ['Aa']*10 + ['aa']*5 + ['AA']*5
    st.session_state.males = list(base); random.shuffle(st.session_state.males)
    st.session_state.femelles = list(base); random.shuffle(st.session_state.femelles)
    st.session_state.id_pere = None
    st.session_state.id_mere = None
    st.session_state.enfant = None
    st.session_state.alleles_choisis = None

# --- FONCTION DE DESSIN ---
def dessiner_indiv(ax, x, y, ge, souligne=False, halo_allele=None):
    r = 0.3
    ec = 'gold' if souligne else 'black'
    lw = 3 if souligne else 1
    ax.add_patch(patches.Ellipse((x, y), r*2.2, r*1.5, fc=COULEURS_INDIV[ge], ec=ec, lw=lw, zorder=5))
    for i, a in enumerate(list(ge)):
        dx = -0.1 if i == 0 else 0.1
        c = COULEUR_A if a == 'A' else COULEUR_a
        ec_a = 'gold' if (halo_allele is not None and i == halo_allele) else 'black'
        lw_a = 2 if (halo_allele is not None and i == halo_allele) else 0.5
        ax.add_patch(patches.Ellipse((x+dx, y), 0.15, 0.25, fc=c, ec=ec_a, lw=lw_a, zorder=6))
        ax.text(x+dx, y, a, ha='center', va='center', fontsize=6, fontweight='bold', zorder=7)

# --- INTERFACE ---
st.title("🧬 Simulation de transmission")

# Boutons
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
    if st.button("🔄 Reset"): st.session_state.id_pere = st.session_state.id_mere = st.session_state.enfant = st.session_state.alleles_choisis = None; st.rerun()

# --- GRAPHIQUE UNIQUE ---
fig, ax = plt.subplots(figsize=(10, 8))
ax.set_xlim(-1, 11); ax.set_ylim(-3, 6); ax.axis('off')

# Dessin Population
for i in range(20):
    # Hommes
    mx, my = i%5, 5-(i//5)*0.8
    dessiner_indiv(ax, mx, my, st.session_state.males[i], souligne=(st.session_state.id_pere == i))
    if st.session_state.id_pere == i:
        ax.annotate("", xy=(2.5, 1.5), xytext=(mx, my-0.3), arrowprops=dict(arrowstyle="->", color="gold", lw=2, connectionstyle="arc3,rad=-0.2"))

    # Femmes
    fx, fy = 6+i%5, 5-(i//5)*0.8
    dessiner_indiv(ax, fx, fy, st.session_state.femelles[i], souligne=(st.session_state.id_mere == i))
    if st.session_state.id_mere == i:
        ax.annotate("", xy=(7.5, 1.5), xytext=(fx, fy-0.3), arrowprops=dict(arrowstyle="->", color="gold", lw=2, connectionstyle="arc3,rad=0.2"))

# Dessin Parents tirés
if st.session_state.id_pere is not None:
    dessiner_indiv(ax, 2.5, 1, st.session_state.males[st.session_state.id_pere], souligne=True, 
                   halo_allele=st.session_state.alleles_choisis[0] if st.session_state.enfant else None)
if st.session_state.id_mere is not None:
    dessiner_indiv(ax, 7.5, 1, st.session_state.femelles[st.session_state.id_mere], souligne=True, 
                   halo_allele=st.session_state.alleles_choisis[1] if st.session_state.enfant else None)

# Dessin Enfant et flèches d'allèles
if st.session_state.enfant:
    dessiner_indiv(ax, 5, -1.5, st.session_state.enfant)
    # Flèches des allèles
    ax.annotate("", xy=(4.9, -1.2), xytext=(2.5, 0.7), arrowprops=dict(arrowstyle="->", color="red", lw=1.5, ls="--"))
    ax.annotate("", xy=(5.1, -1.2), xytext=(7.5, 0.7), arrowprops=dict(arrowstyle="->", color="red", lw=1.5, ls="--"))

st.pyplot(fig)
