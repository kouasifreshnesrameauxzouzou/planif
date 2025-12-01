import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, date, timedelta
import plotly.express as px
import plotly.graph_objects as go
import calendar
import hashlib

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
        
        /* ==================== MOBILE HEADER ==================== */
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
        
        .user-badge {{
            font-size: 0.85rem;
            color: {COLORS['text_secondary']};
            margin-top: 0.25rem;
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
        
        /* ==================== LOGIN/REGISTER CARD ==================== */
        .auth-card {{
            max-width: 400px;
            margin: 4rem auto;
            background: {COLORS['bg_card']};
            border-radius: 24px;
            padding: 3rem 2rem;
            box-shadow: 0 12px 48px rgba(0,0,0,0.5);
        }}
        
        .auth-title {{
            text-align: center;
            font-size: 2.5rem;
            font-weight: 900;
            margin-bottom: 2rem;
            background: linear-gradient(135deg, {COLORS['accent_orange']}, {COLORS['accent_pink']});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        
        .auth-logo {{
            text-align: center;
            font-size: 4rem;
            margin-bottom: 1rem;
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
            padding-bottom: 2rem;
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
        
        /* ==================== SIDEBAR HIDDEN ==================== */
        [data-testid="stSidebar"] {{
            display: none !important;
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
    
    # Table utilisateurs
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            nom_complet TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS revenus (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            type_revenu TEXT NOT NULL,
            client TEXT,
            montant REAL NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS depenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            type_depense TEXT NOT NULL,
            montant REAL NOT NULL,
            fournisseur TEXT,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS epargne (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            montant_depose REAL NOT NULL,
            objectif TEXT,
            solde_actuel REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            nom_pret TEXT NOT NULL,
            montant_total REAL NOT NULL,
            montant_rembourse REAL DEFAULT 0,
            echeance TEXT NOT NULL,
            prochaine_echeance TEXT,
            solde_restant REAL NOT NULL,
            statut TEXT DEFAULT 'actif',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS paiements_prets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            pret_id INTEGER NOT NULL,
            montant REAL NOT NULL,
            date TEXT NOT NULL,
            note TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (pret_id) REFERENCES prets (id)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            nom_projet TEXT NOT NULL,
            client TEXT,
            date_debut TEXT NOT NULL,
            date_fin TEXT,
            etat TEXT DEFAULT 'En cours',
            budget_estime REAL,
            responsable TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            nom_client TEXT NOT NULL,
            contact TEXT,
            type_service TEXT,
            date_service TEXT,
            montant_paye REAL,
            commentaires TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    
    conn.commit()
    conn.close()

def get_db_connection():
    return sqlite3.connect(DB_PATH)

# ==================== AUTHENTIFICATION ====================
def hash_password(password):
    """Hash un mot de passe avec SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, password, nom_complet):
    """Créer un nouvel utilisateur"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        password_hash = hash_password(password)
        cursor.execute("""
            INSERT INTO users (username, password_hash, nom_complet)
            VALUES (?, ?, ?)
        """, (username, password_hash, nom_complet))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False

def verify_user(username, password):
    """Vérifier les identifiants d'un utilisateur"""
    conn = get_db_connection()
    cursor = conn.cursor()
    password_hash = hash_password(password)
    cursor.execute("""
        SELECT id, nom_complet FROM users 
        WHERE username = ? AND password_hash = ?
    """, (username, password_hash))
    result = cursor.fetchone()
    conn.close()
    return result

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

# ==================== FONCTIONS CRUD (avec user_id) ====================

# --- REVENUS ---
def ajouter_revenu(user_id, date_rev, type_rev, client, montant, description):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO revenus (user_id, date, type_revenu, client, montant, description)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, date_rev, type_rev, client, montant, description))
    conn.commit()
    conn.close()

def get_revenus(user_id, mois=None, annee=None):
    conn = get_db_connection()
    if mois and annee:
        query = "SELECT * FROM revenus WHERE user_id = ? AND strftime('%m', date) = ? AND strftime('%Y', date) = ? ORDER BY date DESC"
        params = (user_id, f"{mois:02d}", str(annee))
    else:
        query = "SELECT * FROM revenus WHERE user_id = ? ORDER BY date DESC"
        params = (user_id,)
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

# --- DÉPENSES ---
def ajouter_depense(user_id, date_dep, type_dep, montant, fournisseur, description):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO depenses (user_id, date, type_depense, montant, fournisseur, description)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, date_dep, type_dep, montant, fournisseur, description))
    conn.commit()
    conn.close()

def get_depenses(user_id, mois=None, annee=None):
    conn = get_db_connection()
    if mois and annee:
        query = "SELECT * FROM depenses WHERE user_id = ? AND strftime('%m', date) = ? AND strftime('%Y', date) = ? ORDER BY date DESC"
        params = (user_id, f"{mois:02d}", str(annee))
    else:
        query = "SELECT * FROM depenses WHERE user_id = ? ORDER BY date DESC"
        params = (user_id,)
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

# --- ÉPARGNE ---
def ajouter_epargne(user_id, date_ep, montant_depose, objectif, solde_actuel):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO epargne (user_id, date, montant_depose, objectif, solde_actuel)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, date_ep, montant_depose, objectif, solde_actuel))
    conn.commit()
    conn.close()

def get_epargne(user_id):
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM epargne WHERE user_id = ? ORDER BY date DESC", conn, params=(user_id,))
    conn.close()
    return df

def get_solde_epargne(user_id):
    df = get_epargne(user_id)
    return df['solde_actuel'].iloc[0] if not df.empty else 0

# --- PRÊTS ---
def ajouter_pret(user_id, nom_pret, montant_total, echeance, prochaine_echeance):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO prets (user_id, nom_pret, montant_total, echeance, prochaine_echeance, solde_restant)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, nom_pret, montant_total, echeance, prochaine_echeance, montant_total))
    conn.commit()
    conn.close()

def get_prets(user_id, statut=None):
    conn = get_db_connection()
    if statut:
        query = "SELECT * FROM prets WHERE user_id = ? AND statut = ? ORDER BY created_at DESC"
        params = (user_id, statut)
    else:
        query = "SELECT * FROM prets WHERE user_id = ? ORDER BY created_at DESC"
        params = (user_id,)
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

# --- PROJETS ---
def ajouter_projet(user_id, nom, client, date_debut, date_fin, etat, budget, responsable):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO projets (user_id, nom_projet, client, date_debut, date_fin, etat, budget_estime, responsable)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (user_id, nom, client, date_debut, date_fin, etat, budget, responsable))
    conn.commit()
    conn.close()

def get_projets(user_id, etat=None):
    conn = get_db_connection()
    if etat:
        query = "SELECT * FROM projets WHERE user_id = ? AND etat = ? ORDER BY date_debut DESC"
        params = (user_id, etat)
    else:
        query = "SELECT * FROM projets WHERE user_id = ? ORDER BY date_debut DESC"
        params = (user_id,)
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

# --- CLIENTS ---
def ajouter_client(user_id, nom, contact, type_service, date_service, montant, commentaires):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO clients (user_id, nom_client, contact, type_service, date_service, montant_paye, commentaires)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (user_id, nom, contact, type_service, date_service, montant, commentaires))
    conn.commit()
    conn.close()

def get_clients(user_id):
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM clients WHERE user_id = ? ORDER BY date_service DESC", conn, params=(user_id,))
    conn.close()
    return df

# ==================== CALCULS ====================
def calculer_soldes(user_id, mois, annee):
    """Calcul du solde = Revenus - Dépenses pour un utilisateur"""
    revenus_df = get_revenus(user_id, mois, annee)
    depenses_df = get_depenses(user_id, mois, annee)
    
    total_revenus = revenus_df['montant'].sum() if not revenus_df.empty else 0
    total_depenses = depenses_df['montant'].sum() if not depenses_df.empty else 0
    solde = total_revenus - total_depenses
    
    return {
        'revenus': total_revenus,
        'depenses': total_depenses,
        'solde': solde
    }

# ==================== COMPOSANTS UI ====================
def render_mobile_header(nom_utilisateur):
    st.markdown(f"""
        <div class="mobile-header">
            <div class="header-left">
                <div class="header-icon">💎</div>
                <div>
                    <div class="app-title">Finance Pro</div>
                    <div class="user-badge">👤 {nom_utilisateur}</div>
                </div>
            </div>
            <div style="display: flex; gap: 0.75rem;">
                <div class="header-icon" style="background: {COLORS['bg_card']}; width: 40px; height: 40px; font-size: 1.2rem;">🔔</div>
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

def render_stats_cards(soldes, epargne=0):
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
                <div class="stat-value neutral">{epargne:,.0f} FCFA</div>
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

# ==================== PAGE LOGIN/REGISTER ====================
def page_auth():
    st.markdown('<div class="auth-card">', unsafe_allow_html=True)
    st.markdown('<div class="auth-logo">💎</div>', unsafe_allow_html=True)
    st.markdown('<div class="auth-title">Finance Pro</div>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔐 Connexion", "✨ Inscription"])
    
    with tab1:
        with st.form("login_form"):
            username = st.text_input("Nom d'utilisateur", key="login_username")
            password = st.text_input("Mot de passe", type="password", key="login_password")
            
            if st.form_submit_button("Se connecter", use_container_width=True):
                if username and password:
                    result = verify_user(username, password)
                    if result:
                        st.session_state.logged_in = True
                        st.session_state.user_id = result[0]
                        st.session_state.nom_utilisateur = result[1] or username
                        st.success(f"✅ Bienvenue {st.session_state.nom_utilisateur} !")
                        st.rerun()
                    else:
                        st.error("❌ Identifiants incorrects !")
                else:
                    st.warning("⚠️ Veuillez remplir tous les champs")
    
    with tab2:
        with st.form("register_form"):
            nom_complet = st.text_input("Nom complet", key="reg_nom")
            username = st.text_input("Nom d'utilisateur", key="reg_username")
            password = st.text_input("Mot de passe", type="password", key="reg_password")
            password_confirm = st.text_input("Confirmer le mot de passe", type="password", key="reg_password_confirm")
            
            if st.form_submit_button("S'inscrire", use_container_width=True):
                if nom_complet and username and password and password_confirm:
                    if password != password_confirm:
                        st.error("❌ Les mots de passe ne correspondent pas !")
                    elif len(password) < 6:
                        st.error("❌ Le mot de passe doit contenir au moins 6 caractères")
                    else:
                        if create_user(username, password, nom_complet):
                            st.success("✅ Compte créé ! Vous pouvez vous connecter.")
                        else:
                            st.error("❌ Ce nom d'utilisateur existe déjà !")
                else:
                    st.warning("⚠️ Veuillez remplir tous les champs")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== PAGES PRINCIPALES ====================

def page_dashboard():
    user_id = st.session_state.user_id
    nom_utilisateur = st.session_state.nom_utilisateur
    
    render_mobile_header(nom_utilisateur)
    
    mois, annee = render_month_selector()
    
    soldes = calculer_soldes(user_id, mois, annee)
    epargne_total = get_solde_epargne(user_id)
    
    st.markdown('<div class="content-container">', unsafe_allow_html=True)
    
    render_stats_cards(soldes, epargne_total)
    
    depenses_df = get_depenses(user_id, mois, annee)
    
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

def page_revenus():
    user_id = st.session_state.user_id
    nom_utilisateur = st.session_state.nom_utilisateur
    
    render_mobile_header(nom_utilisateur)
    
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
                    ajouter_revenu(user_id, str(date_rev), type_rev, client, montant, description)
                    st.success("✅ Revenu enregistré!")
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        df = get_revenus(user_id)
        if not df.empty:
            st.metric("💵 Total", f"{df['montant'].sum():,.0f} FCFA")
            st.dataframe(df[['date', 'type_revenu', 'client', 'montant']], use_container_width=True)
        else:
            st.info("Aucun revenu")

def page_depenses():
    user_id = st.session_state.user_id
    nom_utilisateur = st.session_state.nom_utilisateur
    
    render_mobile_header(nom_utilisateur)
    
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
                    ajouter_depense(user_id, str(date_dep), type_dep, montant, fournisseur, description)
                    st.success("✅ Dépense enregistrée!")
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        df = get_depenses(user_id)
        if not df.empty:
            st.metric("💸 Total", f"{df['montant'].sum():,.0f} FCFA")
            st.dataframe(df[['date', 'type_depense', 'fournisseur', 'montant']], use_container_width=True)
        else:
            st.info("Aucune dépense")

def page_epargne():
    user_id = st.session_state.user_id
    nom_utilisateur = st.session_state.nom_utilisateur
    
    render_mobile_header(nom_utilisateur)
    
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
                    ajouter_epargne(user_id, str(date_ep), montant_depose, objectif, solde_actuel)
                    st.success("✅ Dépôt enregistré!")
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        df = get_epargne(user_id)
        if not df.empty:
            solde = get_solde_epargne(user_id)
            st.metric("💰 Solde", f"{solde:,.0f} FCFA")
            st.dataframe(df[['date', 'montant_depose', 'objectif', 'solde_actuel']], use_container_width=True)
        else:
            st.info("Aucun dépôt")

def page_prets():
    user_id = st.session_state.user_id
    nom_utilisateur = st.session_state.nom_utilisateur
    
    render_mobile_header(nom_utilisateur)
    
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
                    ajouter_pret(user_id, nom_pret, montant_total, str(echeance), str(prochaine))
                    st.success("✅ Prêt enregistré!")
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        prets = get_prets(user_id, statut='actif')
        if not prets.empty:
            for _, pret in prets.iterrows():
                prog = (pret['montant_rembourse'] / pret['montant_total']) * 100
                with st.expander(f"💳 {pret['nom_pret']}"):
                    st.progress(prog / 100)
                    st.write(f"**Restant:** {pret['solde_restant']:,.0f} FCFA")
        else:
            st.info("Aucun prêt")

def page_projets():
    user_id = st.session_state.user_id
    nom_utilisateur = st.session_state.nom_utilisateur
    
    render_mobile_header(nom_utilisateur)
    
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
                    ajouter_projet(user_id, nom, client, str(debut), str(fin), etat, budget, responsable)
                    st.success("✅ Projet créé!")
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        df = get_projets(user_id)
        if not df.empty:
            st.dataframe(df[['nom_projet', 'client', 'etat', 'budget_estime']], use_container_width=True)
        else:
            st.info("Aucun projet")

def page_clients():
    user_id = st.session_state.user_id
    nom_utilisateur = st.session_state.nom_utilisateur
    
    render_mobile_header(nom_utilisateur)
    
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
                    ajouter_client(user_id, nom, contact, type_service, str(date_service), montant, commentaires)
                    st.success("✅ Client enregistré!")
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        df = get_clients(user_id)
        if not df.empty:
            st.metric("💰 Total CA", f"{df['montant_paye'].sum():,.0f} FCFA")
            st.dataframe(df[['nom_client', 'contact', 'type_service', 'montant_paye']], use_container_width=True)
        else:
            st.info("Aucun client")

# ==================== NAVIGATION TABS ====================
def render_nav_tabs():
    """Navigation par tabs Streamlit (propre, sans duplication)"""
    tabs = st.tabs(["📊 Dashboard", "💰 Revenus", "💸 Dépenses", "💎 Épargne", "💳 Prêts", "📋 Projets", "👥 Clients", "🚪 Déconnexion"])
    
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
    with tabs[5]:
        page_projets()
    with tabs[6]:
        page_clients()
    with tabs[7]:
        st.markdown('<div style="padding: 2rem;">', unsafe_allow_html=True)
        if st.button("🚪 Se déconnecter", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.session_state.nom_utilisateur = None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ==================== MAIN ====================
def main():
    init_db()
    load_mobile_dark_css()
    
    # Initialiser les variables de session
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    if 'nom_utilisateur' not in st.session_state:
        st.session_state.nom_utilisateur = None
    
    # Router
    if not st.session_state.logged_in:
        page_auth()
    else:
        render_nav_tabs()

if __name__ == "__main__":
    main()
