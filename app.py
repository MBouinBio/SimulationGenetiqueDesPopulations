# --- FONCTION ÉTIQUETTE (À placer avant le graphique) ---
def dessiner_label(ax, x, y, texte):
    ax.text(x, y, texte.upper(), ha='center', va='center', fontsize=9, fontweight='bold',
            bbox=dict(facecolor='white', edgecolor='#CCCCCC', boxstyle='round,pad=0.3', alpha=0.9), zorder=10)

# --- GRAPHIQUE UNIQUE (Remplacer la fin de votre code) ---
fig, ax = plt.subplots(figsize=(10, 8.5))
ax.set_xlim(-1, 11); ax.set_ylim(-3, 6.5); ax.axis('off')

# 1. ÉTIQUETTES DE POPULATION
dessiner_label(ax, 5, 6.2, "Population")
dessiner_label(ax, 2, 5.6, "Hommes")
dessiner_label(ax, 8, 5.6, "Femmes")

# Dessin Population
for i in range(20):
    mx, my = i%5, 4.8-(i//5)*0.8
    dessiner_indiv(ax, mx, my, st.session_state.males[i], souligne=(st.session_state.id_pere == i))
    if st.session_state.id_pere == i:
        ax.annotate("", xy=(2.5, 2.3), xytext=(mx, my-0.3), 
                    arrowprops=dict(arrowstyle="->", color="gold", lw=2, connectionstyle="arc3,rad=-0.2"))

    fx, fy = 6+i%5, 4.8-(i//5)*0.8
    dessiner_indiv(ax, fx, fy, st.session_state.femelles[i], souligne=(st.session_state.id_mere == i))
    if st.session_state.id_mere == i:
        ax.annotate("", xy=(7.5, 2.3), xytext=(fx, fy-0.3), 
                    arrowprops=dict(arrowstyle="->", color="gold", lw=2, connectionstyle="arc3,rad=0.2"))

# 2. PARENTS TIRÉS ET LEURS ÉTIQUETTES
if st.session_state.id_pere is not None:
    dessiner_label(ax, 2.5, 2.3, "Père tiré au hasard")
    dessiner_indiv(ax, 2.5, 1.2, st.session_state.males[st.session_state.id_pere], souligne=True, 
                   halo_allele=st.session_state.alleles_choisis[0] if st.session_state.enfant else None)

if st.session_state.id_mere is not None:
    dessiner_label(ax, 7.5, 2.3, "Mère tirée au hasard")
    dessiner_indiv(ax, 7.5, 1.2, st.session_state.femelles[st.session_state.id_mere], souligne=True, 
                   halo_allele=st.session_state.alleles_choisis[1] if st.session_state.enfant else None)

# 3. ENFANT ET SON ÉTIQUETTE
if st.session_state.enfant:
    dessiner_label(ax, 5, -0.4, "Enfant")
    dessiner_indiv(ax, 5, -1.5, st.session_state.enfant)
    
    # Flèches de transmission des allèles
    ax.annotate("", xy=(4.9, -1.1), xytext=(2.5, 0.8), arrowprops=dict(arrowstyle="->", color="#FF4D4D", lw=1.5, ls="--"))
    ax.annotate("", xy=(5.1, -1.1), xytext=(7.5, 0.8), arrowprops=dict(arrowstyle="->", color="#FF4D4D", lw=1.5, ls="--"))

plt.tight_layout()
st.pyplot(fig)
