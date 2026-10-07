import streamlit as st
import json
import plotly.graph_objects as go

# 1. Configuração da página
st.set_page_config(page_title="Insight Analysis | Scout Pro", layout="wide", initial_sidebar_state="expanded")

# 2. CSS Premium & Configuração de Impressão (PDF)
st.markdown("""
<style>
    .stApp { background-color: #111111; color: #e0e0e0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;}
    .match-header { background-color: #1a1a1a; border: 1px solid #333; border-radius: 12px; padding: 15px; margin-bottom: 20px; display: flex; flex-direction: column; align-items: center; justify-content: center;}
    .tournament-name { font-size: 12px; color: #888; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px; display: flex; align-items: center; gap: 5px;}
    .score-container { display: flex; align-items: center; justify-content: center; gap: 30px; width: 100%;}
    .team-name { font-size: 16px; font-weight: 500; text-align: center; width: 120px;}
    .score-box { font-size: 38px; font-weight: bold; color: white;}
    .match-meta { font-size: 11px; color: #666; margin-top: 10px; border-top: 1px solid #333; padding-top: 10px; width: 100%; text-align: center;}
    .player-header { background-color: #1a1a1a; border: 1px solid #333; border-radius: 12px; padding: 20px; margin-bottom: 20px; display: flex; align-items: center; justify-content: space-between;}
    .player-photo { border-radius: 50%; border: 3px solid #6f42c1; width: 90px; height: 90px; object-fit: cover;}
    .player-tags { display: flex; gap: 8px; margin-top: 8px; flex-wrap: wrap;}
    .tag { background-color: #333; color: #ccc; padding: 4px 12px; border-radius: 20px; font-size: 12px;}
    .tag-highlight { background-color: rgba(111, 66, 193, 0.15); color: #d8b4fe; border: 1px solid #6f42c1;}
    .nota-box { border: 2px solid #28a745; border-radius: 12px; padding: 10px 15px; text-align: center; min-width: 80px;}
    .nota-val { font-size: 32px; font-weight: bold; line-height: 1;}
    .stat-card { background-color: #1a1a1a; border: 1px solid #333; border-radius: 10px; padding: 15px; margin-bottom: 15px;}
    .stat-card-title { font-size: 14px; font-weight: bold; margin-bottom: 15px; color: #6f42c1; display: flex; align-items: center; gap: 8px;}
    .stat-row { margin-bottom: 12px;}
    .stat-text { display: flex; justify-content: space-between; font-size: 13px; color: #aaa; margin-bottom: 4px;}
    .stat-val { font-weight: bold; color: white;}
    .progress-bg { background-color: #333; height: 4px; border-radius: 2px; width: 100%;}
    .progress-fill { background-color: #6f42c1; height: 100%; border-radius: 2px;}
    
    @media print {
        section[data-testid="stSidebar"] { display: none !important; }
        header { display: none !important; }
        .stApp { background-color: #111111 !important; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
        .stat-card, .player-header, .match-header { page-break-inside: avoid; }
    }
</style>
""", unsafe_allow_html=True)

# 3. BARRA LATERAL
st.sidebar.markdown("<h2 style='color: #6f42c1; font-weight: 800; text-align: center;'>MOTOR DE SCOUT</h2>", unsafe_allow_html=True)
ficheiro_upload = st.sidebar.file_uploader("📥 Arraste o ficheiro JSON de Lineups:", type=['json'])

st.sidebar.divider()
st.sidebar.markdown("📝 **Detalhes da Partida**")
input_torneio = st.sidebar.text_input("Torneio:", "Amigável Internacional")
col_casa, col_fora = st.sidebar.columns(2)
with col_casa:
    input_casa = st.text_input("Equipa Casa:", "México")
    input_golos_casa = st.text_input("Golos Casa:", "3")
with col_fora:
    input_fora = st.text_input("Equipa Fora:", "Chile")
    input_golos_fora = st.text_input("Golos Fora:", "1")

st.sidebar.divider()
st.sidebar.markdown("""
    <button onclick="window.print()" style="width: 100%; background-color: #6f42c1; color: white; border: none; padding: 12px; border-radius: 8px; cursor: pointer; font-weight: bold; font-size: 14px; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
        🖨️ Gerar Relatório PDF
    </button>
""", unsafe_allow_html=True)

# 4. FUNÇÃO INTELIGENTE DE DADOS
@st.cache_data
def carregar_dados(ficheiro):
    jogadores_dict = {}
    try:
        if ficheiro is not None:
            dados_j = json.load(ficheiro) 
        else:
            with open('dados_jogadores.json', 'r', encoding='utf-8') as f:
                dados_j = json.load(f) 
        if 'home' in dados_j and 'players' in dados_j['home']:
            for p in dados_j['home']['players']: jogadores_dict[p['player']['name']] = p
        if 'away' in dados_j and 'players' in dados_j['away']:
            for p in dados_j['away']['players']: jogadores_dict[p['player']['name']] = p
    except: pass
    return jogadores_dict

jogadores = carregar_dados(ficheiro_upload)

# 5. CABEÇALHO DA EMPRESA
NOME_DO_FICHEIRO_DA_LOGO = "logo.png" 
col_logo, col_titulo = st.columns([1, 10])
with col_logo:
    try:
        st.image(NOME_DO_FICHEIRO_DA_LOGO, width=65)
    except: pass
with col_titulo:
    st.markdown("<h2 style='color: #6f42c1; font-weight: 800; letter-spacing: 1px; margin-top: 10px;'>INSIGHT ANALYSIS</h2>", unsafe_allow_html=True)

if not jogadores:
    st.info("👈 Por favor, carregue o ficheiro JSON ou garanta que 'dados_jogadores.json' está na pasta.")
    st.stop()

# 6. SELEÇÃO DE JOGADOR
st.sidebar.divider()
lista_nomes = sorted(list(jogadores.keys()))
indice_default = lista_nomes.index("Armando González") if "Armando González" in lista_nomes else 0
nome_escolhido = st.sidebar.selectbox("🎯 Escolha o Jogador:", lista_nomes, index=indice_default)

dados_atleta = jogadores[nome_escolhido]
info = dados_atleta.get('player', {})
stats = dados_atleta.get('statistics', {})

st.markdown(f"""
<div class="match-header">
    <div class="tournament-name">🏆 {input_torneio}</div>
    <div class="score-container">
        <div class="team-name">{input_casa}</div>
        <div class="score-box">{input_golos_casa} <span style='color:#555; font-size:24px; font-weight:normal; margin: 0 10px;'>-</span> {input_golos_fora}</div>
        <div class="team-name">{input_fora}</div>
    </div>
    <div class="match-meta">Dados processados em tempo real | Insight Scout Engine</div>
</div>
""", unsafe_allow_html=True)

# 7. PERFIL DO JOGADOR COM PROXY DE IMAGEM
posicao = info.get('position', 'Atacante')
camisola = dados_atleta.get('shirtNumber', '-')
nota = stats.get('rating', 'S/N')
minutos = stats.get('minutesPlayed', 0)

# Links de Proxy para contornar o bloqueio do Sofascore na nuvem
foto_original = f"https://api.sofascore.app/api/v1/player/{info.get('id')}/image"
foto_proxy_1 = f"https://wsrv.nl/?url=api.sofascore.app/api/v1/player/{info.get('id')}/image"
foto_proxy_2 = f"https://api.allorigins.win/raw?url={foto_original}"

try:
    n = float(nota)
    cor_nota = "#28a745" if n >= 7.0 else ("#ffcc00" if n >= 6.0 else "#dc3545")
except: cor_nota = "#888"

st.markdown(f"""
<div class="player-header">
    <div style="display:flex; align-items:center; gap:20px;">
        <img src="{foto_proxy_1}" onerror="this.onerror=null; this.src='{foto_proxy_2}';" class="player-photo" referrerpolicy="no-referrer">
        <div>
            <div style="color:#aaa; font-size:12px; margin-bottom:5px;">⚽ Equipa</div>
            <h2 style="margin:0; font-size:26px;">{nome_escolhido}</h2>
            <div class="player-tags">
                <span class="tag">{posicao}</span>
                <span class="tag">#{camisola}</span>
                <span class="tag">{minutos}'</span>
                <span class="tag tag-highlight">Titular</span>
            </div>
        </div>
    </div>
    <div class="nota-box" style="border-color:{cor_nota}; background-color: {cor_nota}15;">
        <div class="nota-val" style="color:{cor_nota};">{nota}</div>
        <div style="font-size:10px; color:#aaa; margin-top:4px; letter-spacing:1px;">NOTA</div>
    </div>
</div>
""", unsafe_allow_html=True)

# 8. GRÁFICO DE RADAR
st.markdown("<h4 style='color:#666; font-size:12px; text-transform:uppercase; letter-spacing:1px; margin-bottom:0;'>📈 Radar de Desempenho</h4>", unsafe_allow_html=True)
st.divider()
categorias = ['Finalização', 'Passe', 'Drible', 'Defesa', 'Duelos', 'Físico']
valores = [
    min(stats.get('onTargetScoringAttempt', 0) * 25, 100),
    min((stats.get('accuratePass', 0) / max(stats.get('totalPass', 1), 1)) * 100, 100),
    min(stats.get('wasFouled', 0) * 20, 100),
    min(stats.get('totalTackle', 0) * 20, 100),
    min((stats.get('duelWon', 0) / max(stats.get('duelTotal', 1), 1)) * 100, 100),
    min(stats.get('minutesPlayed', 0), 100)
]
fig = go.Figure(data=go.Scatterpolar(r=valores, theta=categorias, fill='toself', fillcolor='rgba(111, 66, 193, 0.4)', line=dict(color='#6f42c1', width=2), marker=dict(color='#d8b4fe', size=6)))
fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100], color='#333', gridcolor='#222', tickfont=dict(color='rgba(0,0,0,0)')), angularaxis=dict(color='#aaa', gridcolor='#222')), showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=40, r=40, t=30, b=30), height=350)
st.plotly_chart(fig, use_container_width=True)

# 9. ESTATÍSTICAS DETALHADAS
def mostrar_barra(label, valor, max_esperado=100):
    val_num = float(valor) if isinstance(valor, (int, float)) else 0
    percentagem = min((val_num / max_esperado) * 100, 100)
    return f"<div class='stat-row'><div class='stat-text'><span>{label}</span> <span class='stat-val'>{valor}</span></div><div class='progress-bg'><div class='progress-fill' style='width: {percentagem}%;'></div></div></div>"

c1, c2 = st.columns(2)
with c1:
    html_passes = "<div class='stat-card'><div class='stat-card-title'>➔ Passes</div>"
    html_passes += mostrar_barra("Total de Passes", stats.get('totalPass', 0), 60)
    html_passes += mostrar_barra("Passes Certos", stats.get('accuratePass', 0), 60)
    html_passes += mostrar_barra("Passes-Chave", stats.get('keyPass', 0), 5)
    precisao = round((stats.get('accuratePass', 0) / max(stats.get('totalPass', 1), 1)) * 100)
    html_passes += mostrar_barra("Precisão", f"{precisao}%", 100)
    st.markdown(html_passes + "</div>", unsafe_allow_html=True)
    html_duelos = "<div class='stat-card'><div class='stat-card-title'>⚔️ Duelos</div>"
    html_duelos += mostrar_barra("Total", stats.get('duelTotal', 0), 15)
    html_duelos += mostrar_barra("Ganhos", stats.get('duelWon', 0), 15)
    html_duelos += mostrar_barra("Duelos Aéreos Ganhos", stats.get('aerialWon', 0), 10)
    st.markdown(html_duelos + "</div>", unsafe_allow_html=True)
with c2:
    html_ataque = "<div class='stat-card'><div class='stat-card-title'>🎯 Ataque</div>"
    html_ataque += mostrar_barra("Golos", stats.get('goals', 0), 3)
    html_ataque += mostrar_barra("Finalizações", stats.get('totalScoringAttempt', 0), 5)
    html_ataque += mostrar_barra("Finalizações no Gol", stats.get('onTargetScoringAttempt', 0), 5)
    html_ataque += mostrar_barra("Toques na Bola", stats.get('touches', 0), 80)
    st.markdown(html_ataque + "</div>", unsafe_allow_html=True)
    html_defesa = "<div class='stat-card'><div class='stat-card-title'>🛡️ Defesa</div>"
    html_defesa += mostrar_barra("Desarmes", stats.get('totalTackle', 0), 5)
    html_defesa += mostrar_barra("Interceptações", stats.get('interceptionWon', 0), 5)
    html_defesa += mostrar_barra("Afastamentos", stats.get('totalClearance', 0), 8)
    st.markdown(html_defesa + "</div>", unsafe_allow_html=True)