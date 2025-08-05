import streamlit as st
import pandas as pd
import textwrap
import plotly.express as px

# Configuración de la página
st.set_page_config(layout="wide", page_title="Dashboard de Medios", initial_sidebar_state="expanded")

st.title("📊 Dashboard de Medios")
st.markdown("<p style='font-size:16px;'>Visualización comparativa de rendimiento digital por red y medio.</p>", unsafe_allow_html=True)
st.divider()

# Menú lateral
menu = st.sidebar.radio("Selecciona una sección:", ["Comparativa", "Analitics EL DEBER", "Yo Elijo"])

# === Sección: COMPARATIVA ===
if menu == "Comparativa":
    st.markdown("### 📌 Resumen de publicaciones por medio")

    df_resumen = pd.read_csv('resumen_posts.csv')

    colores_tarjeta = {
        "EL DEBER": "#d0f2d0",
        "Red Uno": "#ffe5cc",
        "UNITEL": "#ffd6d6"
    }

    icons = {
        "EL DEBER": "📰",
        "Red Uno": "📺",
        "UNITEL": "📡"
    }

    cols = st.columns(len(df_resumen))
    for i, row in df_resumen.iterrows():
        medio = row["medio"]
        color = colores_tarjeta.get(medio, "#F5F5F5")
        icono = icons.get(medio, "📊")

        posts = f"{int(row['posts']):,}"
        delta = float(row["delta"])
        flecha = "▲" if delta >= 0 else "▼"
        color_delta = "green" if delta >= 0 else "red"

        with cols[i]:
            st.markdown(
                f"""
                <div style='background-color:{color};
                            padding:20px 25px;
                            border-radius:15px;
                            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                            margin-bottom:15px;
                            text-align:center'>
                    <h4 style='margin-bottom:5px; color:#333;'>{icono} {medio}</h4>
                    <p style='font-size:30px; margin:0; font-weight:bold;'>{posts}</p>
                    <p style='color:{color_delta}; font-size:16px; margin-top:5px;'>{flecha} {abs(delta)}%</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.divider()

    # === MÉTRICAS WEB (solo aquí) ===
    st.markdown("### 🌐 Métricas web por medio (SimilarWeb)")

    df_web = pd.read_csv("metricas_web.csv")

    colores_fondo = {
        "EL DEBER": "#d0f2d0",
        "Red Uno": "#ffe5cc",
        "UNITEL": "#ffd6d6"
    }

    iconos_web = {
        "EL DEBER": "📰",
        "Red Uno": "📺",
        "UNITEL": "📡"
    }

    def formatear_delta(valor, invertido=False):
        flecha = "▲" if (valor >= 0 and not invertido) or (valor < 0 and invertido) else "▼"
        color = "green" if flecha == "▲" else "red"
        return flecha, color

    for i in range(len(df_web)):
        row = df_web.iloc[i]
        medio = row["medio"]
        color = colores_fondo.get(medio, "#f0f0f0")
        icono = iconos_web.get(medio, "🌐")

        vistas = f"{int(row['vistas']):,}"
        sesiones = f"{int(row['sesiones']):,}"
        ranking = f"{int(row['ranking'])}"

        vistas_var = float(row["vistas_var"])
        sesiones_var = float(row["sesiones_var"])
        ranking_var = int(row["ranking_var"])

        flecha_v, color_v = formatear_delta(vistas_var)
        flecha_s, color_s = formatear_delta(sesiones_var)
        flecha_r, color_r = formatear_delta(ranking_var, invertido=True)

        st.markdown(
            f"""
            <div style='background-color:{color};
                        padding:25px;
                        border-radius:15px;
                        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                        margin-bottom:25px'>
                <h4 style='color:#1a1a1a; margin-bottom:10px;'>{icono} {medio}</h4>

                <div style='display: flex; justify-content: space-between;'>

                    <div style='text-align:center; width:32%'>
                        <p style='margin:0; font-weight:bold;'>Vistas</p>
                        <p style='font-size:24px; margin:5px 0;'>{vistas}</p>
                        <p style='color:{color_v}; margin:0'>{flecha_v} {abs(vistas_var)}%</p>
                    </div>

                    <div style='text-align:center; width:32%'>
                        <p style='margin:0; font-weight:bold;'>Sesiones</p>
                        <p style='font-size:24px; margin:5px 0;'>{sesiones}</p>
                        <p style='color:{color_s}; margin:0'>{flecha_s} {abs(sesiones_var)}%</p>
                    </div>

                    <div style='text-align:center; width:32%'>
                        <p style='margin:0; font-weight:bold;'>Ranking</p>
                        <p style='font-size:24px; margin:5px 0;'>{ranking}</p>
                        <p style='color:{color_r}; margin:0'>{flecha_r} {abs(ranking_var)}</p>
                    </div>

                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# === Sección: ANALYTICS EL DEBER ===
elif menu == "Analitics EL DEBER":
    st.markdown("### 📲 Análisis por red social")

    df_redes = pd.read_csv("redes_sociales_otros.csv")

    tabs = st.tabs(df_redes["red"].unique())
    for i, red in enumerate(df_redes["red"].unique()):
        with tabs[i]:
            df_red = df_redes[df_redes["red"] == red]

            st.markdown(f"#### {red}")
            st.dataframe(df_red.style
                         .format(subset=["posts", "posts_var", "seguidores", "seguidores_var"], formatter="{:,.0f}")
                         .applymap(lambda x: 'color: green;' if isinstance(x, str) and '+' in x else 'color: red;',
                                   subset=["posts_var", "seguidores_var"])
                         )

            fig_posts = px.bar(df_red, x="medio", y="posts", color="medio",
                               title=f"Cantidad de publicaciones en {red}", text="posts")
            st.plotly_chart(fig_posts, use_container_width=True, key=f"posts_{red}_{i}")

            fig_followers = px.bar(df_red, x="medio", y="seguidores", color="medio",
                                   title=f"Seguidores por medio en {red}", text="seguidores")
            st.plotly_chart(fig_followers, use_container_width=True, key=f"seguidores_{red}_{i}")

# === Sección: YO ELIJO ===
elif menu == "Yo Elijo":
    st.markdown("### ⚙️ Personalización del análisis")
    st.markdown("Aquí podrías permitir elegir un medio, una red o exportar el dashboard.")
