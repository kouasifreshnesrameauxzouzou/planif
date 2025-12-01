import streamlit as st
import pandas as pd
from datetime import datetime, date
import plotly.graph_objects as go
import calendar

# ==================== CONFIGURATION ====================
st.set_page_config(
    page_title="Finance Pro",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== DARK THEME COLORS ====================
COLORS = {
    'bg_dark': '#0a0a0a',
    'bg_card': '#1a1a1a',
    'bg_card_hover': '#252525',
    'text_primary': '#ffffff',
    'text_secondary': '#8a8a8a',
    'accent_orange': '#ff9966',
    'accent_green': '#66ffcc',
    'accent_blue': '#6699ff',
    'accent_purple': '#cc66ff',
    'accent_pink': '#ff66cc',
    'accent_yellow': '#ffcc66',
    'success': '#00ff88',
    'danger': '#ff4466',
    'warning': '#ffaa00',
}

# ==================== CSS MOBILE ====================
def load_mobile_dark_css():
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
        
        * {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        .stApp {{
            background-color: {COLORS['bg_dark']};
            color: {COLORS['text_primary']};
        }}
        
        .mobile-header {{
            padding: 1.5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: {COLORS['bg_dark']};
            border-bottom: 1px solid rgba(255,255,255,0.05);
            margin-bottom: 1rem;
        }}
        
        .header-left {{
            display: flex;
            align-items: center;
            gap: 1rem;
        }}
        
        .header-icon {{
            width: 48px;
            height: 48px;
            background: linear-gradient(135deg, {COLORS['accent_orange']}, {COLORS['accent_pink']});
            border-radius: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
        }}
        
        .app-title {{
            font-size: 1.5rem;
            font-weight: 900;
            color: {COLORS['text_primary']};
        }}
        
        .stats-row {{
            display: flex;
            gap: 1rem;
            padding: 0 1.5rem;
            margin-bottom: 2rem;
            overflow-x: auto;
        }}
        
        .stat-card {{
            flex: 1;
            min-width: 140px;
            background: {COLORS['bg_card']};
            border-radius: 16px;
            padding: 1.25rem;
            transition: all 0.3s ease;
        }}
        
        .stat-card:hover {{
            background: {COLORS['bg_card_hover']};
            transform: translateY(-2px);
        }}
        
        .stat-label {{
            font-size: 0.75rem;
            color: {COLORS['text_secondary']};
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 0.5rem;
        }}
        
        .stat-value {{
            font-size: 1.5rem;
            font-weight: 800;
        }}
        
        .stat-value.positive {{ color: {COLORS['success']}; }}
        .stat-value.negative {{ color: {COLORS['danger']}; }}
        .stat-value.neutral {{ color: {COLORS['text_primary']}; }}
        
        .stat-underline {{
            width: 50%;
            height: 2px;
            background: linear-gradient(90deg, {COLORS['accent_orange']}, transparent);
            margin-top: 0.5rem;
        }}
        
        .chart-container {{
            padding: 0 1.5rem;
            margin-bottom: 2rem;
        }}
        
        .category-list {{
            padding: 0 1.5rem;
        }}
        
        .category-item {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: {COLORS['bg_card']};
            border-radius: 16px;
            padding: 1.25rem;
            margin-bottom: 0.75rem;
            transition: all 0.3s ease;
        }}
        
        .category-item:hover {{
            background: {COLORS['bg_card_hover']};
            transform: translateX(4px);
        }}
        
        .category-left {{
            display: flex;
            align-items: center;
            gap: 1rem;
        }}
        
        .category-icon {{
            width: 48px;
            height: 48px;
            border-radius: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
        }}
        
        .category-name {{
            font-size: 1rem;
            font-weight: 600;
        }}
        
        .category-right {{
            text-align: right;
        }}
        
        .category-amount {{
            font-size: 1.1rem;
            font-weight: 700;
        }}
        
        .category-percent {{
            font-size: 0.8rem;
            color: {COLORS['text_secondary']};
            margin-top: 0.2rem;
        }}
        
        .stTextInput>div>div>input,
        .stNumberInput>div>div>input,
        .stSelectbox>div>div>select,
        .stTextArea>div>div>textarea,
        .stDateInput>div>div>input {{
            background: {COLORS['bg_card']} !important;
            color: {COLORS['text_primary']} !important;
            border: 1px solid rgba(255,255,255,0.1) !important;
            border-radius: 12px !important;
            padding: 0.875rem 1rem !important;
        }}
        
        .stTextInput>div>div>input:focus,
        .stNumberInput>div>div>input:focus,
        .stSelectbox>div>div>select:focus {{
            border-color: {COLORS['accent_orange']} !important;
            box-shadow: 0 0 0 2px rgba(255, 153, 102, 0.2) !important;
        }}
        
        .stTextInput>label,
        .stNumberInput>label,
        .stSelectbox>label,
        .stTextArea>label,
        .stDateInput>label {{
            color: {COLORS['text_secondary']} !important;
            font-weight: 600 !important;
            font-size: 0.85rem !important;
            text-transform: uppercase !important;
        }}
        
        .stButton>button {{
            background: linear-gradient(135deg, {COLORS['accent_orange']}, {COLORS['accent_pink']});
            color: {COLORS['text_primary']};
            border: none;
            border-radius: 16px;
            padding: 1rem 2rem;
            font-weight: 700;
            transition: all 0.3s ease;
            box-shadow: 0 8px 24px rgba(255, 153, 102, 0.3);
            width: 100%;
        }}
        
        .stButton>button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 12px 32px rgba(255, 153, 102, 0.4);
        }}
        
        .stTabs [data-baseweb="tab-list"] {{
            gap: 0.5rem;
            background: transparent;
            border-bottom: none;
            padding: 0 1.5rem;
            margin-bottom: 1.5rem;
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            background: {COLORS['bg_card']};
            border-radius: 12px;
            color: {COLORS['text_secondary']};
            font-weight: 600;
            padding: 0.875rem 1.25rem;
            white-space: nowrap;
            flex-shrink: 0;
        }}
        
        .stTabs [aria-selected="true"] {{
            background: linear-gradient(135deg, {COLORS['accent_orange']}, {COLORS['accent_pink']});
            color: {COLORS['text_primary']};
            box-shadow: 0 4px 12px rgba(255, 153, 102, 0.4);
        }}
        
        .form-card {{
            background: {COLORS['bg_card']};
            border-radius: 20px;
            padding: 2rem;
            margin: 0 1.5rem 1.5rem 1.5rem;
        }}
        
        h1 {{
            color: {COLORS['text_primary']};
            font-weight: 900;
            font-size: 2rem;
            margin-bottom: 1.5rem;
            padding: 0 1.5rem;
        }}
        
        h2, h3 {{
            color: {COLORS['text_primary']};
            font-weight: 700;
            padding: 0 1.5rem;
        }}
        
        .content-container {{
            padding-bottom: 2rem;
        }}
        
        .stDataFrame {{
            background: {COLORS['bg_card']};
            border-radius: 16px;
        }}
        
        [data-testid="stMetricValue"] {{
            font-size: 2rem;
            font-weight: 900;
        }}
        
        [data-testid="stMetricLabel"] {{
            color: {COLORS['text_secondary']};
            font-size: 0.75rem;
            text-transform: uppercase;
        }}
        
        .stProgress > div > div > div > div {{
            background: linear-gradient(90deg, {COLORS['accent_orange']}, {COLORS['accent_pink']});
        }}
        
        .streamlit-expanderHeader {{
            background: {COLORS['bg_card']};
            border-radius: 12px;
            color: {COLORS['text_primary']};
            font-weight: 600;
        }}
        
        [data-testid="stSidebar"] {{
            display: none !important;
        }}
        
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
        
        ::-webkit-scrollbar {{
            width: 6px;
            height: 6px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: {COLORS['bg_card']};
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: {COLORS['accent_orange']};
            border-radius: 10px;
        }}
    </style>
    """, unsafe_allow_html=True)

# ==================== INITIALISATION ====================
def init_session_data():
    if 'revenus' not in st.session_state:
        st.session_state.revenus = []
    if 'depenses' not in st.session_state:
        st.session_state.depenses = []
    if 'epargne' not in st.session_state:
        st.session_state.epargne = []
    if 'prets' not in st.session_state:
        st.session_state.prets = []
    if 'projets' not in st.session_state:
        st.session_state.projets = []
    if 'clients' not in st.session_state:
        st.session_state.clients = []

# ==================== CATÉGORIES ====================
CATEGORIES_INFO = {
    "Virements": {"icon": "💸", "color": "#66ffcc"},
    "Transport": {"icon": "🚗", "color": "#6699ff"},
    "Nourriture": {"icon": "🍔", "color": "#ffcc66"},
    "Factures": {"icon": "📄", "color": "#ff9966"},
    "Shopping": {"icon": "🛍️", "color": "#ff66cc"},
    "Santé": {"icon": "⚕️", "color": "#cc66ff"},
    "Loisirs": {"icon": "🎮", "color": "#66ff99"},
    "Restaurant": {"icon": "🍽️", "color": "#ff6699"},
    "Salaires": {"icon": "💼", "color": "#6699ff"},
    "Marketing": {"icon": "📢", "color": "#ff9966"},
}

TYPES_REVENUS = ["Vente", "Service", "Consultation", "Abonnement", "Commission", "Salaire", "Encaissement de devis", "Maintenance", "Dons", "Autre"]
TYPES_DEPENSES = list(CATEGORIES_INFO.keys()) + ["Loyer", "Équipement", "Maintenance", "Dîme", "Offrande", "Promesse", "Sortie entre amis", "Salaire des employés", "WiFi", "Crédit téléphonique", "Vêtement", "Engagement", "Autre"]
ETATS_PROJET = ["En cours", "Terminé", "En attente", "Annulé"]

# ==================== FONCTIONS ====================
def get_revenus_df(mois=None, annee=None):
    if not st.session_state.revenus:
        return pd.DataFrame(columns=['date', 'type_revenu', 'client', 'montant', 'description'])
    
    df = pd.DataFrame(st.session_state.revenus)
    df['date'] = pd.to_datetime(df['date'])
    
    if mois and annee:
        df = df[(df['date'].dt.month == mois) & (df['date'].dt.year == annee)]
    
    return df.sort_values('date', ascending=False)

def get_depenses_df(mois=None, annee=None):
    if not st.session_state.depenses:
        return pd.DataFrame(columns=['date', 'type_depense', 'montant', 'fournisseur', 'description'])
    
    df = pd.DataFrame(st.session_state.depenses)
    df['date'] = pd.to_datetime(df['date'])
    
    if mois and annee:
        df = df[(df['date'].dt.month == mois) & (df['date'].dt.year == annee)]
    
    return df.sort_values('date', ascending=False)

def get_epargne_df():
    if not st.session_state.epargne:
        return pd.DataFrame(columns=['date', 'montant_depose', 'objectif', 'solde_actuel'])
    
    df = pd.DataFrame(st.session_state.epargne)
    df['date'] = pd.to_datetime(df['date'])
    return df.sort_values('date', ascending=False)

def get_solde_epargne():
    df = get_epargne_df()
    return df['solde_actuel'].iloc[0] if not df.empty else 0

def get_prets_df(statut=None):
    if not st.session_state.prets:
        return pd.DataFrame(columns=['nom_pret', 'montant_total', 'montant_rembourse', 'echeance', 'prochaine_echeance', 'solde_restant', 'statut'])
    
    df = pd.DataFrame(st.session_state.prets)
    if statut:
        df = df[df['statut'] == statut]
    return df

def calculer_soldes_periode(periode_type, param1, param2):
    """Calcule les soldes selon la période sélectionnée"""
    revenus_df = pd.DataFrame(st.session_state.revenus) if st.session_state.revenus else pd.DataFrame()
    depenses_df = pd.DataFrame(st.session_state.depenses) if st.session_state.depenses else pd.DataFrame()
    
    if not revenus_df.empty:
        revenus_df['date'] = pd.to_datetime(revenus_df['date'])
    if not depenses_df.empty:
        depenses_df['date'] = pd.to_datetime(depenses_df['date'])
    
    if periode_type == 'jour':
        # param1 = date sélectionnée
        if not revenus_df.empty:
            revenus_df = revenus_df[revenus_df['date'].dt.date == param1]
        if not depenses_df.empty:
            depenses_df = depenses_df[depenses_df['date'].dt.date == param1]
            
    elif periode_type == 'semaine':
        # param1 = date de début de semaine
        debut_semaine = param1 - pd.Timedelta(days=param1.weekday())
        fin_semaine = debut_semaine + pd.Timedelta(days=6)
        
        if not revenus_df.empty:
            revenus_df = revenus_df[(revenus_df['date'].dt.date >= debut_semaine) & 
                                   (revenus_df['date'].dt.date <= fin_semaine)]
        if not depenses_df.empty:
            depenses_df = depenses_df[(depenses_df['date'].dt.date >= debut_semaine) & 
                                     (depenses_df['date'].dt.date <= fin_semaine)]
            
    elif periode_type == 'mois':
        # param1 = mois, param2 = année
        if not revenus_df.empty:
            revenus_df = revenus_df[(revenus_df['date'].dt.month == param1) & 
                                   (revenus_df['date'].dt.year == param2)]
        if not depenses_df.empty:
            depenses_df = depenses_df[(depenses_df['date'].dt.month == param1) & 
                                     (depenses_df['date'].dt.year == param2)]
            
    elif periode_type == 'annee':
        # param2 = année
        if not revenus_df.empty:
            revenus_df = revenus_df[revenus_df['date'].dt.year == param2]
        if not depenses_df.empty:
            depenses_df = depenses_df[depenses_df['date'].dt.year == param2]
    
    total_revenus = revenus_df['montant'].sum() if not revenus_df.empty else 0
    total_depenses = depenses_df['montant'].sum() if not depenses_df.empty else 0
    
    return {
        'revenus': total_revenus,
        'depenses': total_depenses,
        'solde': total_revenus - total_depenses,
        'epargne': get_solde_epargne(),
        'depenses_df': depenses_df
    }

def calculer_soldes(mois, annee):
    revenus_df = get_revenus_df(mois, annee)
    depenses_df = get_depenses_df(mois, annee)
    
    total_revenus = revenus_df['montant'].sum() if not revenus_df.empty else 0
    total_depenses = depenses_df['montant'].sum() if not depenses_df.empty else 0
    
    return {
        'revenus': total_revenus,
        'depenses': total_depenses,
        'solde': total_revenus - total_depenses,
        'epargne': get_solde_epargne()
    }

# ==================== UI ====================
def render_mobile_header():
    st.markdown(f"""
        <div class="mobile-header">
            <div class="header-left">
                <div class="header-icon">💎</div>
                <div class="app-title">Finance Pro</div>
            </div>
            <div style="display: flex; gap: 0.75rem;">
                <div class="header-icon" style="background: {COLORS['bg_card']}; width: 40px; height: 40px; font-size: 1.2rem;">🔔</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def render_period_selector():
    st.markdown('<div style="padding: 0 1.5rem 1rem 1.5rem;">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        periode = st.selectbox(
            "Période",
            ["Jour", "Semaine", "Mois", "Année"],
            index=2,
            label_visibility="collapsed"
        )
    
    with col2:
        if periode == "Jour":
            date_selectionnee = st.date_input(
                "Date",
                value=date.today(),
                min_value=date(2020, 1, 1),
                max_value=date(2030, 12, 31),
                format="DD/MM/YYYY",
                label_visibility="collapsed"
            )
            st.markdown('</div>', unsafe_allow_html=True)
            return ('jour', date_selectionnee, None)
            
        elif periode == "Semaine":
            date_selectionnee = st.date_input(
                "Semaine de",
                value=date.today(),
                min_value=date(2020, 1, 1),
                max_value=date(2030, 12, 31),
                format="DD/MM/YYYY",
                label_visibility="collapsed"
            )
            st.markdown('</div>', unsafe_allow_html=True)
            return ('semaine', date_selectionnee, None)
            
        elif periode == "Mois":
            current_month = datetime.now().month
            current_year = datetime.now().year
            
            months_options = []
            months_display = []
            for i in range(-6, 7):
                m = current_month + i
                y = current_year
                if m < 1:
                    m += 12
                    y -= 1
                elif m > 12:
                    m -= 12
                    y += 1
                months_options.append((m, y))
                months_display.append(f"{calendar.month_name[m]} {y}")
            
            selected = st.selectbox(
                "Mois",
                range(len(months_options)),
                index=6,
                format_func=lambda x: months_display[x],
                label_visibility="collapsed"
            )
            st.markdown('</div>', unsafe_allow_html=True)
            return ('mois', months_options[selected][0], months_options[selected][1])
            
        else:  # Année
            annee = st.selectbox(
                "Année",
                range(2020, 2031),
                index=datetime.now().year - 2020,
                label_visibility="collapsed"
            )
            st.markdown('</div>', unsafe_allow_html=True)
            return ('annee', None, annee)

def render_stats_cards(soldes):
    st.markdown(f"""
        <div class="stats-row">
            <div class="stat-card">
                <div class="stat-label">💰 Revenus</div>
                <div class="stat-value positive">+{soldes['revenus']:,.0f} FCFA</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">💸 Dépenses</div>
                <div class="stat-value negative">-{soldes['depenses']:,.0f} FCFA</div>
                <div class="stat-underline"></div>
            </div>
            <div class="stat-card">
                <div class="stat-label">💵 Solde</div>
                <div class="stat-value {'positive' if soldes['solde'] >= 0 else 'negative'}">{soldes['solde']:+,.0f} FCFA</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">💎 Épargne</div>
                <div class="stat-value neutral">{soldes['epargne']:,.0f} FCFA</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def render_circular_chart(depenses_df, total_depenses):
    if depenses_df.empty:
        return
    
    cat_data = depenses_df.groupby('type_depense')['montant'].sum().reset_index()
    cat_data = cat_data.sort_values('montant', ascending=False)
    
    colors = ['#ff66cc', '#66ffcc', '#6699ff', '#ffcc66', '#cc66ff', '#ff9966']
    
    fig = go.Figure(data=[go.Pie(
        labels=cat_data['type_depense'],
        values=cat_data['montant'],
        hole=0.75,
        marker=dict(colors=colors[:len(cat_data)]),
        textinfo='none',
        hovertemplate='<b>%{label}</b><br>%{value:,.0f} FCFA<br>%{percent}<extra></extra>'
    )])
    
    fig.update_layout(
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=20, b=20, l=20, r=20),
        height=350,
        annotations=[{
            'text': f'<b>{total_depenses:,.0f} FCFA</b><br><span style="font-size:12px; color:#8a8a8a">Dépenses totales</span>',
            'x': 0.5,
            'y': 0.5,
            'font': {'size': 24, 'color': '#ffffff'},
            'showarrow': False
        }]
    )
    
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

def render_category_list(depenses_df, total_depenses):
    if depenses_df.empty:
        return
    
    cat_data = depenses_df.groupby('type_depense')['montant'].sum().reset_index()
    cat_data = cat_data.sort_values('montant', ascending=False)
    
    st.markdown('<div class="category-list">', unsafe_allow_html=True)
    
    for _, row in cat_data.iterrows():
        cat_name = row['type_depense']
        montant = row['montant']
        pourcentage = (montant / total_depenses * 100) if total_depenses > 0 else 0
        
        cat_info = CATEGORIES_INFO.get(cat_name, {"icon": "📦", "color": "#8a8a8a"})
        
        st.markdown(f"""
            <div class="category-item">
                <div class="category-left">
                    <div class="category-icon" style="background: {cat_info['color']}20;">
                        {cat_info['icon']}
                    </div>
                    <div class="category-name">{cat_name}</div>
                </div>
                <div class="category-right">
                    <div class="category-amount">-{montant:,.0f} FCFA</div>
                    <div class="category-percent">{pourcentage:.0f}%</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== PAGES ====================
def page_dashboard():
    render_mobile_header()
    
    periode_type, param1, param2 = render_period_selector()
    
    soldes = calculer_soldes_periode(periode_type, param1, param2)
    
    st.markdown('<div class="content-container">', unsafe_allow_html=True)
    
    render_stats_cards(soldes)
    
    depenses_df = soldes['depenses_df']
    
    if not depenses_df.empty:
        render_circular_chart(depenses_df, soldes['depenses'])
        render_category_list(depenses_df, soldes['depenses'])
    else:
        st.markdown("""
            <div style="text-align: center; padding: 4rem 2rem; color: #8a8a8a;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">📊</div>
                <div style="font-size: 1.1rem;">Aucune dépense pour cette période</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def page_revenus():
    render_mobile_header()
    st.title("💰 Revenus")
    
    tab1, tab2 = st.tabs(["➕ Ajouter", "📋 Historique"])
    
    with tab1:
        st.markdown('<div class="form-card">', unsafe_allow_html=True)
        with st.form("form_revenu"):
            col1, col2 = st.columns(2)
            with col1:
                date_rev = st.date_input(
                    "Date",
                    value=date.today(),
                    min_value=date(2020, 1, 1),
                    max_value=date(2030, 12, 31),
                    format="DD/MM/YYYY"
                )
                type_rev = st.selectbox("Type", TYPES_REVENUS)
                client = st.text_input("Client")
            with col2:
                montant = st.number_input("Montant (FCFA)", min_value=0.0, step=1000.0)
                description = st.text_area("Description")
            
            submitted = st.form_submit_button("💾 Enregistrer", use_container_width=True)
            
        if submitted:
            if montant > 0:
                st.session_state.revenus.append({
                    'date': str(date_rev),
                    'type_revenu': type_rev,
                    'client': client,
                    'montant': montant,
                    'description': description
                })
                st.success("✅ Revenu enregistré avec succès !", icon="✅")
                st.balloons()
                st.rerun()
            else:
                st.error("❌ Le montant doit être supérieur à 0", icon="❌")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        df = get_revenus_df()
        if not df.empty:
            st.metric("💵 Total", f"{df['montant'].sum():,.0f} FCFA")
            display_df = df[['date', 'type_revenu', 'client', 'montant']].copy()
            display_df['date'] = display_df['date'].dt.strftime('%Y-%m-%d')
            st.dataframe(display_df, use_container_width=True, hide_index=True)
        else:
            st.info("Aucun revenu")

def page_depenses():
    render_mobile_header()
    st.title("💸 Dépenses")
    
    tab1, tab2 = st.tabs(["➕ Ajouter", "📋 Historique"])
    
    with tab1:
        st.markdown('<div class="form-card">', unsafe_allow_html=True)
        with st.form("form_depense"):
            col1, col2 = st.columns(2)
            with col1:
                date_dep = st.date_input(
                    "Date",
                    value=date.today(),
                    min_value=date(2020, 1, 1),
                    max_value=date(2030, 12, 31),
                    format="DD/MM/YYYY"
                )
                type_dep = st.selectbox("Type", TYPES_DEPENSES)
                montant = st.number_input("Montant (FCFA)", min_value=0.0, step=100.0)
            with col2:
                fournisseur = st.text_input("Fournisseur")
                description = st.text_area("Description")
            
            submitted = st.form_submit_button("💾 Enregistrer", use_container_width=True)
            
        if submitted:
            if montant > 0:
                st.session_state.depenses.append({
                    'date': str(date_dep),
                    'type_depense': type_dep,
                    'montant': montant,
                    'fournisseur': fournisseur,
                    'description': description
                })
                st.success("✅ Dépense enregistrée avec succès !", icon="✅")
                st.balloons()
                st.rerun()
            else:
                st.error("❌ Le montant doit être supérieur à 0", icon="❌")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        df = get_depenses_df()
        if not df.empty:
            st.metric("💸 Total", f"{df['montant'].sum():,.0f} FCFA")
            display_df = df[['date', 'type_depense', 'fournisseur', 'montant']].copy()
            display_df['date'] = display_df['date'].dt.strftime('%Y-%m-%d')
            st.dataframe(display_df, use_container_width=True, hide_index=True)
        else:
            st.info("Aucune dépense")

def page_epargne():
    render_mobile_header()
    st.title("💎 Épargne")
    
    tab1, tab2 = st.tabs(["➕ Ajouter", "📊 Suivi"])
    
    with tab1:
        st.markdown('<div class="form-card">', unsafe_allow_html=True)
        
        # Afficher le solde actuel avant le formulaire
        solde_actuel_display = get_solde_epargne()
        st.info(f"💰 Solde actuel d'épargne : **{solde_actuel_display:,.0f} FCFA**")
        
        with st.form("form_epargne"):
            col1, col2 = st.columns(2)
            with col1:
                date_ep = st.date_input(
                    "Date",
                    value=date.today(),
                    min_value=date(2020, 1, 1),
                    max_value=date(2030, 12, 31),
                    format="DD/MM/YYYY"
                )
                montant_depose = st.number_input("Montant à déposer (FCFA)", min_value=0.0, step=1000.0)
            with col2:
                objectif = st.text_input("Objectif (ex: Voyage, Maison...)")
            
            submitted = st.form_submit_button("💾 Déposer", use_container_width=True)
            
        if submitted:
            if montant_depose > 0:
                # Calculer le nouveau solde
                nouveau_solde = solde_actuel_display + montant_depose
                
                st.session_state.epargne.append({
                    'date': str(date_ep),
                    'montant_depose': montant_depose,
                    'objectif': objectif,
                    'solde_actuel': nouveau_solde
                })
                st.success(f"✅ Dépôt de {montant_depose:,.0f} FCFA enregistré ! Nouveau solde : {nouveau_solde:,.0f} FCFA", icon="✅")
                st.balloons()
                st.rerun()
            else:
                st.error("❌ Le montant doit être supérieur à 0", icon="❌")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        df = get_epargne_df()
        if not df.empty:
            solde = get_solde_epargne()
            total_depose = df['montant_depose'].sum()
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("💰 Solde actuel", f"{solde:,.0f} FCFA")
            with col2:
                st.metric("📊 Total déposé", f"{total_depose:,.0f} FCFA")
            
            st.markdown("### 📈 Historique des dépôts")
            display_df = df[['date', 'montant_depose', 'objectif', 'solde_actuel']].copy()
            display_df['date'] = display_df['date'].dt.strftime('%Y-%m-%d')
            display_df.columns = ['Date', 'Montant déposé', 'Objectif', 'Solde']
            st.dataframe(display_df, use_container_width=True, hide_index=True)
        else:
            st.info("Aucun dépôt d'épargne")

def page_prets():
    render_mobile_header()
    st.title("💳 Suivi des Prêts")
    
    tab1, tab2, tab3 = st.tabs(["➕ Nouveau Prêt", "💰 Rembourser", "📊 Prêts Actifs"])
    
    with tab1:
        st.markdown('<div class="form-card">', unsafe_allow_html=True)
        with st.form("form_pret"):
            nom_pret = st.text_input("Nom du prêt")
            col1, col2 = st.columns(2)
            with col1:
                montant_total = st.number_input("Montant total (FCFA)", min_value=0.0, step=10000.0)
                echeance = st.date_input(
                    "Échéance finale",
                    value=date.today(),
                    min_value=date(2020, 1, 1),
                    max_value=date(2030, 12, 31),
                    format="DD/MM/YYYY"
                )
            with col2:
                prochaine = st.date_input(
                    "Prochaine échéance",
                    value=date.today(),
                    min_value=date(2020, 1, 1),
                    max_value=date(2030, 12, 31),
                    format="DD/MM/YYYY"
                )
            
            submitted = st.form_submit_button("💾 Enregistrer", use_container_width=True)
            
        if submitted:
            if nom_pret and montant_total > 0:
                st.session_state.prets.append({
                    'nom_pret': nom_pret,
                    'montant_total': montant_total,
                    'montant_rembourse': 0,
                    'echeance': str(echeance),
                    'prochaine_echeance': str(prochaine),
                    'solde_restant': montant_total,
                    'statut': 'actif'
                })
                st.success(f"✅ Prêt '{nom_pret}' enregistré avec succès !", icon="✅")
                st.balloons()
                st.rerun()
            else:
                st.error("❌ Veuillez remplir tous les champs", icon="❌")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="form-card">', unsafe_allow_html=True)
        
        prets_actifs = get_prets_df(statut='actif')
        
        if not prets_actifs.empty:
            # Sélectionner le prêt à rembourser
            pret_names = prets_actifs['nom_pret'].tolist()
            pret_selectionne = st.selectbox("Sélectionner le prêt à rembourser", pret_names)
            
            # Trouver le prêt sélectionné
            pret_idx = prets_actifs[prets_actifs['nom_pret'] == pret_selectionne].index[0]
            pret = st.session_state.prets[pret_idx]
            
            # Afficher les infos du prêt
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Montant total", f"{pret['montant_total']:,.0f} FCFA")
            with col2:
                st.metric("Déjà remboursé", f"{pret['montant_rembourse']:,.0f} FCFA")
            with col3:
                st.metric("Restant", f"{pret['solde_restant']:,.0f} FCFA")
            
            # Formulaire de remboursement
            with st.form("form_remboursement"):
                col1, col2 = st.columns(2)
                with col1:
                    date_remb = st.date_input(
                        "Date de remboursement",
                        value=date.today(),
                        min_value=date(2020, 1, 1),
                        max_value=date(2030, 12, 31),
                        format="DD/MM/YYYY"
                    )
                with col2:
                    montant_remb = st.number_input(
                        f"Montant à rembourser (Max: {pret['solde_restant']:,.0f} FCFA)",
                        min_value=0.0,
                        max_value=float(pret['solde_restant']),
                        step=1000.0
                    )
                
                note = st.text_area("Note (optionnel)")
                
                submitted_remb = st.form_submit_button("💰 Rembourser", use_container_width=True)
                
            if submitted_remb:
                if montant_remb > 0:
                    # Mettre à jour le prêt
                    st.session_state.prets[pret_idx]['montant_rembourse'] += montant_remb
                    st.session_state.prets[pret_idx]['solde_restant'] -= montant_remb
                    
                    # Si complètement remboursé, changer le statut
                    if st.session_state.prets[pret_idx]['solde_restant'] <= 0:
                        st.session_state.prets[pret_idx]['statut'] = 'soldé'
                        st.success(f"🎉 Prêt '{pret_selectionne}' entièrement remboursé !", icon="🎉")
                        st.balloons()
                    else:
                        st.success(f"✅ Remboursement de {montant_remb:,.0f} FCFA enregistré !", icon="✅")
                    
                    st.rerun()
                else:
                    st.error("❌ Le montant doit être supérieur à 0", icon="❌")
        else:
            st.info("Aucun prêt actif à rembourser")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        prets = get_prets_df(statut='actif')
        if not prets.empty:
            st.markdown("### 📋 Liste des prêts actifs")
            
            for idx, pret in prets.iterrows():
                prog = (pret['montant_rembourse'] / pret['montant_total']) * 100 if pret['montant_total'] > 0 else 0
                
                with st.expander(f"💳 {pret['nom_pret']}", expanded=True):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Montant total", f"{pret['montant_total']:,.0f} FCFA")
                    with col2:
                        st.metric("Remboursé", f"{pret['montant_rembourse']:,.0f} FCFA")
                    with col3:
                        st.metric("Restant", f"{pret['solde_restant']:,.0f} FCFA")
                    
                    st.progress(prog / 100, text=f"Progression: {prog:.1f}%")
                    
                    st.markdown(f"**Échéance finale:** {pret['echeance']}")
                    st.markdown(f"**Prochaine échéance:** {pret['prochaine_echeance']}")
        else:
            st.info("Aucun prêt actif")
        else:
            st.info("Aucun prêt actif")

# ==================== NAVIGATION ====================
def render_nav_tabs():
    tabs = st.tabs(["📊 Dashboard", "💰 Revenus", "💸 Dépenses", "💎 Épargne", "💳 Prêts"])
    
    with tabs[0]:
        page_dashboard()
    with tabs[1]:
        page_revenus()
    with tabs[2]:
        page_depenses()
    with tabs[3]:
        page_epargne()
    with tabs[4]:
        page_prets()

# ==================== MAIN ====================
def main():
    init_session_data()
    load_mobile_dark_css()
    render_nav_tabs()

if __name__ == "__main__":
    main()
