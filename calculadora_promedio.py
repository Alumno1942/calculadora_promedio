"""
Calculadora de calificación necesaria - diseño propio, pensado para celular.
Autor: Gadiel
"""

import streamlit as st

st.set_page_config(page_title="¿Qué necesito sacar?", layout="centered")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:wght@600;700&family=Work+Sans:wght@400;500;600&display=swap');

    html, body, [class*="st-"], .stApp {
        font-family: 'Work Sans', sans-serif;
    }
    .stApp {
        background-color: #F7F5F0;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 560px;
    }
    h1 {
        font-family: 'Fraunces', serif;
        font-size: 1.9rem;
        font-weight: 700;
        color: #2F3B33;
        margin-bottom: 0.2rem;
    }
    .subtitulo {
        color: #6B7568;
        font-size: 0.95rem;
        margin-bottom: 1.6rem;
    }
    .tarjeta {
        background-color: #FFFFFF;
        border: 1px solid #E3E0D6;
        border-radius: 14px;
        padding: 0.9rem 1rem;
        margin-bottom: 0.7rem;
    }
    .resultado {
        background-color: #E7EFE6;
        border: 1px solid #B9CDB3;
        border-radius: 14px;
        padding: 1.2rem;
        text-align: center;
        margin-top: 1rem;
    }
    .resultado-numero {
        font-family: 'Fraunces', serif;
        font-size: 2.3rem;
        font-weight: 700;
        color: #3C5A3E;
    }
    .resultado-texto {
        color: #44524A;
        font-size: 0.95rem;
        margin-top: 0.3rem;
    }
    div[data-testid="stFormSubmitButton"] button {
        background-color: #3C5A3E;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 0.5rem 0;
        width: 100%;
        font-weight: 600;
    }
    .badge {
        display: inline-block;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.03em;
        text-transform: uppercase;
        padding: 0.25rem 0.7rem;
        border-radius: 999px;
        margin-bottom: 0.6rem;
    }
    .badge-ok { background-color: #DDEBDA; color: #2F5C33; }
    .badge-warn { background-color: #F3E6C4; color: #7A5B14; }
    .badge-hard { background-color: #F3DCC9; color: #8A4A1E; }
    .badge-bad { background-color: #F2D6D4; color: #8C2C25; }
    .seccion-titulo {
        font-family: 'Fraunces', serif;
        font-size: 1.15rem;
        font-weight: 600;
        color: #2F3B33;
        margin-top: 1.8rem;
        margin-bottom: 0.2rem;
    }
    .fila-escenario {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: #FFFFFF;
        border: 1px solid #E3E0D6;
        border-radius: 12px;
        padding: 0.7rem 1rem;
        margin-bottom: 0.5rem;
    }
    .fila-escenario .izq { color: #44524A; font-size: 0.9rem; }
    .fila-escenario .der { font-weight: 700; color: #2F3B33; font-size: 0.95rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("¿Qué necesito sacar?")
st.markdown('<p class="subtitulo">Pon tus porcentajes y calificaciones, y te digo qué te falta.</p>', unsafe_allow_html=True)

num_evaluaciones = st.slider("Número de evaluaciones de tu materia", min_value=1, max_value=10, value=3)

with st.form("formulario_calculadora"):
    st.write("")
    pesos = []
    calificaciones = []
    pendientes = []

    peso_sugerido = float(round(100 / num_evaluaciones))

    for i in range(num_evaluaciones):
        st.markdown(f'<div class="tarjeta">', unsafe_allow_html=True)
        st.markdown(f"**Evaluación {i + 1}**")
        col1, col2 = st.columns(2)
        with col1:
            peso = st.number_input("Peso %", min_value=0.0, max_value=100.0, value=peso_sugerido, step=1.0, format="%.1f", key=f"peso_{i}")
        with col2:
            pendiente = st.checkbox("Aún no la tengo", key=f"pend_{i}")
            if not pendiente:
                calificacion = st.number_input("Calificación", min_value=0.0, max_value=10.0, value=8.0, step=0.1, format="%.1f", key=f"calif_{i}")
            else:
                calificacion = 0.0
        st.markdown("</div>", unsafe_allow_html=True)

        pesos.append(peso)
        calificaciones.append(calificacion)
        pendientes.append(pendiente)

    meta = st.number_input("Calificación que quieres obtener", min_value=0.0, max_value=10.0, value=8.0, step=0.1, format="%.1f")

    calcular = st.form_submit_button("Calcular")

if calcular:
    suma_pesos = sum(pesos)

    if abs(suma_pesos - 100) > 0.5:
        st.markdown(
            f'<div class="resultado"><div class="resultado-texto">'
            f'Tus porcentajes suman {suma_pesos:.1f}%. Deben sumar 100% para calcular bien.'
            f'</div></div>',
            unsafe_allow_html=True,
        )
    else:
        peso_pendiente = sum(p for p, pend in zip(pesos, pendientes) if pend)
        suma_ya_obtenida = sum((p / 100) * c for p, c, pend in zip(pesos, calificaciones, pendientes) if not pend)

        if peso_pendiente == 0:
            st.markdown(
                f'<div class="resultado">'
                f'<div class="badge badge-ok">Calificación final</div>'
                f'<div class="resultado-numero">{suma_ya_obtenida:.1f}</div>'
                f'<div class="resultado-texto">Ya no te falta nada, esa sería tu calificación.</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
        else:
            necesario = (meta - suma_ya_obtenida) / (peso_pendiente / 100)

            if necesario > 10:
                maximo_posible = suma_ya_obtenida + (peso_pendiente / 100) * 10
                st.markdown(
                    f'<div class="resultado">'
                    f'<div class="badge badge-bad">No alcanzable</div>'
                    f'<div class="resultado-numero">{maximo_posible:.1f}</div>'
                    f'<div class="resultado-texto">Es lo más alto a lo que puedes llegar, incluso con 10 en todo '
                    f'lo que falta — por debajo de tu meta de {meta:.1f}.<br><br>'
                    f'Conviene hablar con tu profesor sobre un trabajo extra o el examen a título de suficiencia.</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
            elif necesario <= 0:
                st.markdown(
                    f'<div class="resultado">'
                    f'<div class="badge badge-ok">Meta asegurada</div>'
                    f'<div class="resultado-numero">0.0</div>'
                    f'<div class="resultado-texto">Ya la tienes ganada. Puedes ir tranquilo a lo que falta.</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
            elif necesario <= 6:
                st.markdown(
                    f'<div class="resultado">'
                    f'<div class="badge badge-ok">Vas bien</div>'
                    f'<div class="resultado-numero">{necesario:.1f}</div>'
                    f'<div class="resultado-texto">Con un repaso normal de lo visto en clase te alcanza.</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
            elif necesario <= 8.5:
                st.markdown(
                    f'<div class="resultado">'
                    f'<div class="badge badge-warn">Alcanzable</div>'
                    f'<div class="resultado-numero">{necesario:.1f}</div>'
                    f'<div class="resultado-texto">No te confíes. Dedica un par de sesiones de estudio enfocadas '
                    f'en lo que menos domines.</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f'<div class="resultado">'
                    f'<div class="badge badge-hard">Esfuerzo alto</div>'
                    f'<div class="resultado-numero">{necesario:.1f}</div>'
                    f'<div class="resultado-texto">Empieza desde ahora: repasa todos los temas y pide '
                    f'retroalimentación al profesor antes de la evaluación final.</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

            # Si quedan 2 o más evaluaciones pendientes, mostrar caminos alternativos
            pendientes_idx = [i for i, p in enumerate(pendientes) if p]

            if len(pendientes_idx) >= 2 and 0 < necesario <= 10:
                st.markdown('<p class="seccion-titulo">Otros caminos</p>', unsafe_allow_html=True)
                st.caption(
                    f"No tienes que sacar lo mismo en tus {len(pendientes_idx)} evaluaciones pendientes. "
                    f"Esto cambia si varías la Evaluación {pendientes_idx[0] + 1}:"
                )

                primer_idx = pendientes_idx[0]
                peso_primero = pesos[primer_idx]
                peso_resto = sum(pesos[j] for j in pendientes_idx[1:])

                for escenario in [6.0, 7.0, 8.0, 9.0, 10.0]:
                    aporte = (peso_primero / 100) * escenario
                    falta = meta - suma_ya_obtenida - aporte
                    necesario_resto = falta / (peso_resto / 100) if peso_resto > 0 else None

                    if necesario_resto is None:
                        continue
                    elif necesario_resto > 10:
                        texto_resto = "no alcanzable"
                    elif necesario_resto <= 0:
                        texto_resto = "ya no necesitas más"
                    else:
                        texto_resto = f"{necesario_resto:.1f} en el resto"

                    st.markdown(
                        f'<div class="fila-escenario">'
                        f'<span class="izq">Si sacas {escenario:.1f} en Evaluación {primer_idx + 1}</span>'
                        f'<span class="der">{texto_resto}</span>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )