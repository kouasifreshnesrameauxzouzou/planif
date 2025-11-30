import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, date, timedelta
import plotly.express as px
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

# ==================== CSS MOBILE DARK ====================
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
        
        /* ==================== MOBILE HEADER ==================== */
        .mobile-header {{
            padding: 1.5rem 1.5rem 1rem 1.5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .header-icon {{
            width: 40px;
            height: 40px;
            background: {COLORS['bg_card']};
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2rem;
            cursor: pointer;
            transition: all 0.3s ease;
        }}
        
        .header-icon:hover {{
            background: {COLORS['bg_card_hover']};
            transform: scale(1.05);
        }}
        
        /* ==================== STATS CARDS ==================== */
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
        
        /* ==================== CHART CONTAINER ==================== */
        .chart-container {{
            padding: 0 1.5rem;
            margin-bottom: 2rem;
        }}
        
        /* ==================== CATEGORY LIST ==================== */
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
            cursor: pointer;
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
        
        /* ==================== BOTTOM NAV ==================== */
        .bottom-nav {{
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: {COLORS['bg_card']};
            border-top: 1px solid rgba(255,255,255,0.05);
            padding: 0.75rem 0.5rem;
            display: flex;
            justify-content: space-around;
            z-index: 1000;
        }}
        
        .nav-item {{
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 0.2rem;
            font-size: 0.65rem;
            color: {COLORS['text_secondary']};
            cursor: pointer;
            padding: 0.5rem;
            transition: all 0.3s ease;
        }}
        
        .nav-item.active {{
            color: {COLORS['accent_orange']};
        }}
        
        .nav-icon {{
            font-size: 1.3rem;
        }}
        
        /* ==================== INPUTS DARK ==================== */
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
        
        /* ==================== BUTTONS ==================== */
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
        
        /* ==================== TABS ==================== */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 0.5rem;
            background: transparent;
            border-bottom: none;
            padding: 0 1.5rem;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            background: {COLORS['bg_card']};
            border-radius: 12px;
            color: {COLORS['text_secondary']};
            font-weight: 600;
            padding: 0.875rem 1.5rem;
        }}
        
        .stTabs [aria-selected="true"] {{
            background: linear-gradient(135deg, {COLORS['accent_orange']}, {COLORS['accent_pink']});
            color: {COLORS['text_primary']};
        }}
        
        /* ==================== FORM CARD ==================== */
        .form-card {{
            background: {COLORS['bg_card']};
            border-radius: 20px;
            padding: 2rem;
            margin: 0 1.5rem 1.5rem 1.5rem;
        }}
        
        /* ==================== TITLES ==================== */
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
        
        /* ==================== CONTENT CONTAINER ==================== */
        .content-container {{
            padding-bottom: 6rem;
        }}
        
        /* ==================== DATAFRAME ==================== */
        .stDataFrame {{
            background: {COLORS['bg_card']};
            border-radius: 16px;
        }}
        
        /* ==================== METRICS ==================== */
        [data-testid="stMetricValue"] {{
            font-size: 2rem;
            font-weight: 900;
        }}
        
        [data-testid="stMetricLabel"] {{
            color: {COLORS['text_secondary']};
            font-size: 0.75rem;
            text-transform: uppercase;
        }}
        
        /* ==================== PROGRESS ==================== */
        .stProgress > div > div > div > div {{
            background: linear-gradient(90deg, {COLORS['accent_orange']}, {COLORS['accent_pink']});
        }}
        
        /* ==================== EXPANDER ==================== */
        .streamlit-expanderHeader {{
            background: {COLORS['bg_card']};
            border-radius: 12px;
            color: {COLORS['text_primary']};
            font-weight: 600;
        }}
        
        /* ==================== SIDEBAR ==================== */
        [data-testid="stSidebar"] {{
            background: {COLORS['bg_dark']};
            border-right: 1px solid rgba(255,255,255,0.05);
        }}
        
        /* ==================== HIDE BRANDING ==================== */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
        
        /* ==================== SCROLLBAR ==================== */
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

# ==================== BASE DE DONNÉES ====================
DB_PATH = "finance_complete_mobile.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS revenus (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            type_revenu TEXT NOT NULL,
            client TEXT,
            montant REAL NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS depenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            type_depense TEXT NOT NULL,
            montant REAL NOT NULL,
            fournisseur TEXT,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS epargne (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            montant_depose REAL NOT NULL,
            objectif TEXT,
            solde_actuel REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_pret TEXT NOT NULL,
            montant_total REAL NOT NULL,
            montant_rembourse REAL DEFAULT 0,
            echeance TEXT NOT NULL,
            prochaine_echeance TEXT,
            solde_restant REAL NOT NULL,
            statut TEXT DEFAULT 'actif',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS paiements_prets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pret_id INTEGER NOT NULL,
            montant REAL NOT NULL,
            date TEXT NOT NULL,
            note TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (pret_id) REFERENCES prets (id)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_projet TEXT NOT NULL,
            client TEXT,
            date_debut TEXT NOT NULL,
            date_fin TEXT,
            etat TEXT DEFAULT 'En cours',
            budget_estime REAL,
            responsable TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_client TEXT NOT NULL,
            contact TEXT,
            type_service TEXT,
            date_service TEXT,
            montant_paye REAL,
            commentaires TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()

def get_db_connection():
    return sqlite3.connect(DB_PATH)

# ==================== TYPES & CATÉGORIES ====================
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

TYPES_REVENUS = ["Vente", "Service", "Consultation", "Abonnement", "Commission", "Autre"]
TYPES_DEPENSES = list(CATEGORIES_INFO.keys()) + ["Loyer", "Équipement", "Maintenance", "Autre"]
ETATS_PROJET = ["En cours", "Terminé", "En attente", "Annulé"]

# ==================== FONCTIONS CRUD ====================

# --- REVENUS ---
def ajouter_revenu(date_rev, type_rev, client, montant, description):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO revenus (date, type_revenu, client, montant, description)
        VALUES (?, ?, ?, ?, ?)
    """, (date_rev, type_rev, client, montant, description))
    conn.commit()
    conn.close()

def get_revenus(mois=None, annee=None):
    conn = get_db_connection()
    query = "SELECT * FROM revenus"
    params = []
    if mois and annee:
        query += " WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ?"
        params = [f"{mois:02d}", str(annee)]
    query += " ORDER BY date DESC"
    df = pd.read_sql_query(query, conn, params=params if params else None)
    conn.close()
    return df

# --- DÉPENSES ---
def ajouter_depense(date_dep, type_dep, montant, fournisseur, description):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO depenses (date, type_depense, montant, fournisseur, description)
        VALUES (?, ?, ?, ?, ?)
    """, (date_dep, type_dep, montant, fournisseur, description))
    conn.commit()
    conn.close()

def get_depenses(mois=None, annee=None):
    conn = get_db_connection()
    query = "SELECT * FROM depenses"
    params = []
    if mois and annee:
        query += " WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ?"
        params = [f"{mois:02d}", str(annee)]
    query += " ORDER BY date DESC"
    df = pd.read_sql_query(query, conn, params=params if params else None)
    conn.close()
    return df

# --- ÉPARGNE ---
def ajouter_epargne(date_ep, montant_depose, objectif, solde_actuel):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO epargne (date, montant_depose, objectif, solde_actuel)
        VALUES (?, ?, ?, ?)
    """, (date_ep, montant_depose, objectif, solde_actuel))
    conn.commit()
    conn.close()

def get_epargne():
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM epargne ORDER BY date DESC", conn)
    conn.close()
    return df

def get_solde_epargne():
    df = get_epargne()
    return df['solde_actuel'].iloc[0] if not df.empty else 0

# --- PRÊTS ---
def ajouter_pret(nom_pret, montant_total, echeance, prochaine_echeance):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO prets (nom_pret, montant_total, echeance, prochaine_echeance, solde_restant)
        VALUES (?, ?, ?, ?, ?)
    """, (nom_pret, montant_total, echeance, prochaine_echeance, montant_total))
    conn.commit()
    conn.close()

def ajouter_paiement_pret(pret_id, montant, date_paiement, note):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO paiements_prets (pret_id, montant, date, note)
        VALUES (?, ?, ?, ?)
    """, (pret_id, montant, date_paiement, note))
    
    cursor.execute("""
        UPDATE prets 
        SET montant_rembourse = montant_rembourse + ?,
            solde_restant = montant_total - (montant_rembourse + ?)
        WHERE id = ?
    """, (montant, montant, pret_id))
    
    cursor.execute("SELECT montant_total, montant_rembourse FROM prets WHERE id = ?", (pret_id,))
    total, rembourse = cursor.fetchone()
    if rembourse >= total:
        cursor.execute("UPDATE prets SET statut = 'termine' WHERE id = ?", (pret_id,))
    
    conn.commit()
    conn.close()

def get_prets(statut=None):
    conn = get_db_connection()
    query = "SELECT * FROM prets"
    params = []
    if statut:
        query += " WHERE statut = ?"
        params.append(statut)
    query += " ORDER BY created_at DESC"
    df = pd.read_sql_query(query, conn, params=params if params else None)
    conn.close()
    return df

# --- PROJETS ---
def ajouter_projet(nom, client, date_debut, date_fin, etat, budget, responsable):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO projets (nom_projet, client, date_debut, date_fin, etat, budget_estime, responsable)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (nom, client, date_debut, date_fin, etat, budget, responsable))
    conn.commit()
    conn.close()

def get_projets(etat=None):
    conn = get_db_connection()
    query = "SELECT * FROM projets"
    params = []
    if etat:
        query += " WHERE etat = ?"
        params.append(etat)
    query += " ORDER BY date_debut DESC"
    df = pd.read_sql_query(query, conn, params=params if params else None)
    conn.close()
    return df

# --- CLIENTS ---
def ajouter_client(nom, contact, type_service, date_service, montant, commentaires):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO clients (nom_client, contact, type_service, date_service, montant_paye, commentaires)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (nom, contact, type_service, date_service, montant, commentaires))
    conn.commit()
    conn.close()

def get_clients():
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM clients ORDER BY date_service DESC", conn)
    conn.close()
    return df

# ==================== CALCULS ====================
def calculer_soldes(mois, annee):
    revenus_df = get_revenus(mois, annee)
    depenses_df = get_depenses(mois, annee)
    
    total_revenus = revenus_df['montant'].sum() if not revenus_df.empty else 0
    total_depenses = depenses_df['montant'].sum() if not depenses_df.empty else 0
    
    return {
        'revenus': total_revenus,
        'depenses': total_depenses,
        'benefice': total_revenus - total_depenses
    }

# ==================== COMPOSANTS UI ====================
def render_mobile_header():
    st.markdown("""
        <div class="mobile-header">
            <div class="header-icon">💎</div>
            <div style="display: flex; gap: 1rem;">
                <div class="header-icon">🔔</div>
                <div class="header-icon">👁️</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def render_month_selector():
    st.markdown('<div style="padding: 0 1.5rem 1rem 1.5rem;">', unsafe_allow_html=True)
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    months_options = []
    months_display = []
    for i in range(-2, 3):
        m = current_month + i
        y = current_year
        if m < 1:
            m += 12
            y -= 1
        elif m > 12:
            m -= 12
            y += 1
        months_options.append((m, y))
        months_display.append(f"{calendar.month_name[m][:3]}. {y}")
    
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        selected = st.selectbox(
            "Période",
            range(len(months_options)),
            index=2,
            format_func=lambda x: months_display[x],
            label_visibility="collapsed"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    return months_options[selected]

def render_stats_cards(soldes, epargne=0, prets=0):
    st.markdown(f"""
        <div class="stats-row">
            <div class="stat-card">
                <div class="stat-label">↙️ Dépenses</div>
                <div class="stat-value negative">-{soldes['depenses']:,.0f} FCFA</div>
                <div class="stat-underline"></div>
            </div>
            <div class="stat-card">
                <div class="stat-label">↗️ Revenus</div>
                <div class="stat-value positive">+{soldes['revenus']:,.0f} FCFA</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">💎 Épargne</div>
                <div class="stat-value neutral">{epargne:,.0f} FCFA</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">💳 Prêts</div>
                <div class="stat-value neutral">{prets:,.0f} FCFA</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def render_circular_chart(depenses_df, total_depenses):
    if depenses_df.empty:
        return
    
    cat_data = depenses_df.groupby('type_depense')['montant'].sum().reset_index()
    cat_data = cat_data.sort_values('montant', ascending=False)
    
    colors = ['#ff66cc', '#66ffcc', '#6699ff', '#ffcc66', '#cc66ff', '#ff9966', '#66ff99', '#ff6699']
    
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

def render_bottom_nav(active="dashboard"):
    """Bottom navigation avec état de session pour interaction"""
    # Note: La bottom nav est purement visuelle dans Streamlit
    # La navigation réelle se fait via la sidebar
    pass  # On désactive temporairement pour éviter l'affichage du code

# ==================== PAGES ====================

def page_dashboard():
    render_mobile_header()
    mois, annee = render_month_selector()
    
    soldes = calculer_soldes(mois, annee)
    epargne_total = get_solde_epargne()
    prets_actifs = get_prets(statut='actif')
    total_prets = prets_actifs['solde_restant'].sum() if not prets_actifs.empty else 0
    
    st.markdown('<div class="content-container">', unsafe_allow_html=True)
    
    render_stats_cards(soldes, epargne_total, total_prets)
    
    depenses_df = get_depenses(mois, annee)
    
    if not depenses_df.empty:
        render_circular_chart(depenses_df, soldes['depenses'])
        render_category_list(depenses_df, soldes['depenses'])
    else:
        st.markdown("""
            <div style="text-align: center; padding: 4rem 2rem; color: #8a8a8a;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">📊</div>
                <div style="font-size: 1.1rem;">Aucune dépense ce mois-ci</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    # render_bottom_nav("dashboard")  # Désactivé

def page_revenus():
    st.title("💰 Revenus")
    
    tab1, tab2 = st.tabs(["➕ Ajouter", "📋 Historique"])
    
    with tab1:
        st.markdown('<div class="form-card">', unsafe_allow_html=True)
        with st.form("form_revenu"):
            col1, col2 = st.columns(2)
            with col1:
                date_rev = st.date_input("Date", value=date.today())
                type_rev = st.selectbox("Type", TYPES_REVENUS)
                client = st.text_input("Client")
            with col2:
                montant = st.number_input("Montant (FCFA)", min_value=0.0, step=1000.0)
                description = st.text_area("Description")
            
            if st.form_submit_button("💾 Enregistrer"):
                if montant > 0:
                    ajouter_revenu(str(date_rev), type_rev, client, montant, description)
                    st.success("✅ Revenu enregistré!")
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        df = get_revenus()
        if not df.empty:
            st.metric("💵 Total", f"{df['montant'].sum():,.0f} FCFA")
            st.dataframe(df[['date', 'type_revenu', 'client', 'montant']], use_container_width=True)
        else:
            st.info("Aucun revenu")
    
    # Navigation via sidebar uniquement

def page_depenses():
    st.title("💸 Dépenses")
    
    tab1, tab2 = st.tabs(["➕ Ajouter", "📋 Historique"])
    
    with tab1:
        st.markdown('<div class="form-card">', unsafe_allow_html=True)
        with st.form("form_depense"):
            col1, col2 = st.columns(2)
            with col1:
                date_dep = st.date_input("Date", value=date.today())
                type_dep = st.selectbox("Type", TYPES_DEPENSES)
                montant = st.number_input("Montant (FCFA)", min_value=0.0, step=100.0)
            with col2:
                fournisseur = st.text_input("Fournisseur")
                description = st.text_area("Description")
            
            if st.form_submit_button("💾 Enregistrer"):
                if montant > 0:
                    ajouter_depense(str(date_dep), type_dep, montant, fournisseur, description)
                    st.success("✅ Dépense enregistrée!")
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        df = get_depenses()
        if not df.empty:
            st.metric("💸 Total", f"{df['montant'].sum():,.0f} FCFA")
            st.dataframe(df[['date', 'type_depense', 'fournisseur', 'montant']], use_container_width=True)
        else:
            st.info("Aucune dépense")
    
    # Navigation via sidebar

def page_epargne():
    st.title("💎 Épargne")
    
    tab1, tab2 = st.tabs(["➕ Ajouter", "📊 Suivi"])
    
    with tab1:
        st.markdown('<div class="form-card">', unsafe_allow_html=True)
        with st.form("form_epargne"):
            col1, col2 = st.columns(2)
            with col1:
                date_ep = st.date_input("Date", value=date.today())
                montant_depose = st.number_input("Montant (FCFA)", min_value=0.0, step=1000.0)
            with col2:
                objectif = st.text_input("Objectif")
                solde_actuel = st.number_input("Solde actuel (FCFA)", min_value=0.0, step=1000.0)
            
            if st.form_submit_button("💾 Enregistrer"):
                if montant_depose > 0:
                    ajouter_epargne(str(date_ep), montant_depose, objectif, solde_actuel)
                    st.success("✅ Dépôt enregistré!")
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        df = get_epargne()
        if not df.empty:
            solde = get_solde_epargne()
            st.metric("💰 Solde", f"{solde:,.0f} FCFA")
            st.dataframe(df[['date', 'montant_depose', 'objectif', 'solde_actuel']], use_container_width=True)
        else:
            st.info("Aucun dépôt")
    
    # Navigation via sidebar

def page_prets():
    st.title("💳 Prêts")
    
    tab1, tab2 = st.tabs(["➕ Nouveau", "📊 Suivi"])
    
    with tab1:
        st.markdown('<div class="form-card">', unsafe_allow_html=True)
        with st.form("form_pret"):
            nom_pret = st.text_input("Nom du prêt")
            col1, col2 = st.columns(2)
            with col1:
                montant_total = st.number_input("Montant (FCFA)", min_value=0.0, step=10000.0)
                echeance = st.date_input("Échéance")
            with col2:
                prochaine = st.date_input("Prochaine échéance")
            
            if st.form_submit_button("💾 Enregistrer"):
                if nom_pret and montant_total > 0:
                    ajouter_pret(nom_pret, montant_total, str(echeance), str(prochaine))
                    st.success("✅ Prêt enregistré!")
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        prets = get_prets(statut='actif')
        if not prets.empty:
            for _, pret in prets.iterrows():
                prog = (pret['montant_rembourse'] / pret['montant_total']) * 100
                with st.expander(f"💳 {pret['nom_pret']}"):
                    st.progress(prog / 100)
                    st.write(f"**Restant:** {pret['solde_restant']:,.0f} FCFA")
        else:
            st.info("Aucun prêt")
    
    # Navigation via sidebar

def page_projets():
    st.title("📋 Projets")
    
    tab1, tab2 = st.tabs(["➕ Nouveau", "📊 Liste"])
    
    with tab1:
        st.markdown('<div class="form-card">', unsafe_allow_html=True)
        with st.form("form_projet"):
            nom = st.text_input("Nom du projet")
            col1, col2 = st.columns(2)
            with col1:
                client = st.text_input("Client")
                debut = st.date_input("Début", value=date.today())
                fin = st.date_input("Fin")
            with col2:
                etat = st.selectbox("État", ETATS_PROJET)
                budget = st.number_input("Budget (FCFA)", min_value=0.0, step=10000.0)
                responsable = st.text_input("Responsable")
            
            if st.form_submit_button("💾 Créer"):
                if nom:
                    ajouter_projet(nom, client, str(debut), str(fin), etat, budget, responsable)
                    st.success("✅ Projet créé!")
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        df = get_projets()
        if not df.empty:
            st.dataframe(df[['nom_projet', 'client', 'etat', 'budget_estime']], use_container_width=True)
        else:
            st.info("Aucun projet")
    
    # Navigation via sidebar

def page_clients():
    st.title("👥 Clients")
    
    tab1, tab2 = st.tabs(["➕ Ajouter", "📋 Liste"])
    
    with tab1:
        st.markdown('<div class="form-card">', unsafe_allow_html=True)
        with st.form("form_client"):
            nom = st.text_input("Nom du client")
            col1, col2 = st.columns(2)
            with col1:
                contact = st.text_input("Contact")
                type_service = st.text_input("Service")
                date_service = st.date_input("Date", value=date.today())
            with col2:
                montant = st.number_input("Montant (FCFA)", min_value=0.0, step=1000.0)
                commentaires = st.text_area("Commentaires")
            
            if st.form_submit_button("💾 Enregistrer"):
                if nom:
                    ajouter_client(nom, contact, type_service, str(date_service), montant, commentaires)
                    st.success("✅ Client enregistré!")
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        df = get_clients()
        if not df.empty:
            st.metric("💰 Total CA", f"{df['montant_paye'].sum():,.0f} FCFA")
            st.dataframe(df[['nom_client', 'contact', 'type_service', 'montant_paye']], use_container_width=True)
        else:
            st.info("Aucun client")
    
    # Navigation via sidebar

# ==================== MAIN ====================
def main():
    init_db()
    load_mobile_dark_css()
    
    # Menu simple dans sidebar
    with st.sidebar:
        st.markdown("""
            <div style='text-align: center; padding: 2rem 1rem;'>
                <div style='font-size: 3rem;'>💎</div>
                <h2 style='color: #ff9966;'>Finance Pro</h2>
            </div>
        """, unsafe_allow_html=True)
        
        menu = st.radio(
            "Menu",
            ["📊 Dashboard", "💰 Revenus", "💸 Dépenses", "💎 Épargne", 
             "💳 Prêts", "📋 Projets", "👥 Clients"],
            label_visibility="collapsed"
        )
    
    if menu == "📊 Dashboard":
        page_dashboard()
    elif menu == "💰 Revenus":
        page_revenus()
    elif menu == "💸 Dépenses":
        page_depenses()
    elif menu == "💎 Épargne":
        page_epargne()
    elif menu == "💳 Prêts":
        page_prets()
    elif menu == "📋 Projets":
        page_projets()
    elif menu == "👥 Clients":
        page_clients()

if __name__ == "__main__":
    main()