import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
import datetime

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    st.error('DATABASE_URL não encontrada no .env')
    st.stop()

engine = create_engine(DATABASE_URL)

st.set_page_config(page_title='Clima DF — Dashboard', layout='wide')

# Minimal styling for a cleaner UI
st.markdown("""
<style>
 .stApp { background-color: #f7fafc; }
 .big-title { font-size:28px; font-weight:600; }
 .subtitle { color: #6b7280; }
 .metric { background: white; padding: 12px; border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="big-title">Clima DF — Painel</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">KPIs e análises por região e mês — selecione filtros no painel lateral.</div>', unsafe_allow_html=True)

@st.cache_data
def load_data():
    # preferir a view base se existir
    try:
        query = text('SELECT regiao, data, temperatura_maxima, temperatura_minima, precipitacao_total, amplitude_termica FROM weather_db.vw_weather_base')
        with engine.connect() as conn:
            df = pd.read_sql(query, conn)
    except Exception:
        query = text('SELECT regiao, data, temperatura_maxima, temperatura_minima, precipitacao_total, amplitude_termica FROM weather_daily')
        with engine.connect() as conn:
            df = pd.read_sql(query, conn)
    # normalizar nomes de colunas para lowercase (unifica views e tabela)
    df.columns = [c.lower() for c in df.columns]
    df['data'] = pd.to_datetime(df['data'])
    df['year'] = df['data'].dt.year
    df['month'] = df['data'].dt.month
    df['month_name'] = df['data'].dt.strftime('%Y-%m')
    return df

df = load_data()

# Sidebar filters
st.sidebar.header('Filtros')
regions = sorted(df['regiao'].unique())
if 'selected_regions' not in st.session_state:
    st.session_state.selected_regions = regions[:3]

selected_regions = st.sidebar.multiselect('Região', regions, key='selected_regions')
if st.sidebar.button('Selecionar todas'):
    st.session_state.selected_regions = regions

years = sorted(df['year'].unique())
selected_year = st.sidebar.selectbox('Ano', years, index=len(years)-1)

# usar month_name único (ano-mês) para evitar ambiguidade
month_options = sorted(df[df['year']==selected_year]['month_name'].unique())
selected_month_name = st.sidebar.selectbox('Mês (Ano-Mês)', month_options, index=len(month_options)-1)

# filtrar
filtered = df[(df['regiao'].isin(selected_regions)) & (df['month_name'] == selected_month_name)]

if filtered.empty:
    st.warning('Nenhum dado para os filtros selecionados.')
else:
    # Se um único bairro selecionado, buscar KPIs nas views pré-calculadas
    single_region = len(selected_regions) == 1
    kpi_from_views = None
    if single_region:
        reg = selected_regions[0]
        ano = int(selected_month_name.split('-')[0])
        mes = int(selected_month_name.split('-')[1])
        try:
            with engine.connect() as conn:
                kv = conn.execute(text('SELECT * FROM weather_db.vw_kpi_dias_extremos WHERE regiao = :r AND ano = :a'), {'r': reg, 'a': ano}).fetchone()
                ka = conn.execute(text('SELECT * FROM weather_db.vw_kpi_amplitude_media WHERE regiao = :r AND ano = :a AND mes = :m'), {'r': reg, 'a': ano, 'm': mes}).fetchone()
                kt = conn.execute(text('SELECT * FROM weather_db.vw_kpi_temp_media_mensal WHERE regiao = :r AND ano = :a AND mes = :m'), {'r': reg, 'a': ano, 'm': mes}).fetchone()
                kp = conn.execute(text('SELECT * FROM weather_db.vw_kpi_precipitacao_mensal WHERE regiao = :r AND ano = :a AND mes = :m'), {'r': reg, 'a': ano, 'm': mes}).fetchone()
                kpi_from_views = {'dias_extremos': kv, 'amplitude_media': ka, 'temp_media_mensal': kt, 'precipitacao_mensal': kp}
        except Exception:
            kpi_from_views = None

    # calcular KPIs preferindo views quando disponíveis
    def first_numeric_from_row(row):
        if not row:
            return None
        try:
            d = dict(row.items())
        except Exception:
            return None
        for v in d.values():
            if isinstance(v, (int, float)):
                return float(v)
        return None

    if kpi_from_views and kpi_from_views.get('temp_media_mensal'):
        temp_val = first_numeric_from_row(kpi_from_views['temp_media_mensal'])
        temp_med = temp_val if temp_val is not None else filtered.get('temperatura_maxima', filtered.get('temperatura_maximo', filtered.columns)).mean() if False else filtered['temperatura_maxima'].mean()
    else:
        temp_med = filtered['temperatura_maxima'].mean()

    if kpi_from_views and kpi_from_views.get('precipitacao_mensal'):
        precip_val = first_numeric_from_row(kpi_from_views['precipitacao_mensal'])
        precip_total = precip_val if precip_val is not None else filtered['precipitacao_total'].sum()
    else:
        precip_total = filtered['precipitacao_total'].sum()

    # KPIs estilizados
    k1, k2, k3, k4 = st.columns([1.5,1,1,1])
    with k1:
        st.markdown('**Resumo — ' + selected_month_name + '**')
        st.markdown(f"**{int(filtered['data'].nunique())} dias**")
    k2.metric('Temp Máx (média)', f"{temp_med:.1f} °C")
    k3.metric('Temp Mín (média)', f"{filtered['temperatura_minima'].mean():.1f} °C")
    k4.metric('Precipitação (total)', f"{precip_total:.1f} mm")

    # Layout para gráficos principais
    st.markdown('---')
    col1, col2 = st.columns([2,1])
    with col1:
        st.subheader('Séries temporais — Temperatura Máxima')
        fig_ts = px.line(filtered, x='data', y='temperatura_maxima', color='regiao', labels={'data':'Data','temperatura_maxima':'Temp Máx (°C)'}, template='plotly_white')
        fig_ts.update_layout(legend_title_text='Região')
        st.plotly_chart(fig_ts, use_container_width=True)

        st.subheader('Precipitação diária por região')
        fig_bar = px.bar(filtered, x='data', y='precipitacao_total', color='regiao', labels={'precipitacao_total':'Precipitação (mm)'}, template='plotly_white')
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        st.subheader('Distribuição de Temperaturas')
        fig_box = px.box(filtered, x='regiao', y='temperatura_maxima', points='outliers', labels={'temperatura_maxima':'Temp Máx (°C)'}, template='plotly_white')
        st.plotly_chart(fig_box, use_container_width=True)

        st.subheader('Resumo por Região')
        summary = filtered.groupby('regiao').agg(
            dias=('data','nunique'),
            temp_max_media=('temperatura_maxima','mean'),
            temp_min_media=('temperatura_minima','mean'),
            precipitacao_total=('precipitacao_total','sum'),
            amplitude_media=('amplitude_termica','mean')
        ).reset_index()
        st.dataframe(summary.style.format({
            'temp_max_media':'{:.1f}',
            'temp_min_media':'{:.1f}',
            'precipitacao_total':'{:.1f}',
            'amplitude_media':'{:.1f}'
        }))

    # Export
    csv = filtered.to_csv(index=False)
    st.download_button('Exportar CSV (filtro atual)', csv, file_name=f'clima_{selected_month_name}.csv')
