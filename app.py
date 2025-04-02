import streamlit as st
import qrcode
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from io import BytesIO
from collections import Counter

# Función para detectar el color dominante
def detectar_color_dominante(imagen):
    imagen = imagen.convert("RGB")
    pixels = np.array(imagen).reshape(-1, 3)
    colores, conteo = np.unique(pixels, axis=0, return_counts=True)
    return tuple(colores[conteo.argmax()])

# Función para generar el QR
def generar_qr(texto, color, fondo, logo=None):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4
    )
    qr.add_data(texto)
    qr.make(fit=True)
    
    img_qr = qr.make_image(fill_color=color, back_color=fondo).convert("RGB")
    
    if logo:
        logo = Image.open(logo)
        logo.thumbnail((80, 80))
        pos = ((img_qr.size[0] - logo.size[0]) // 2, (img_qr.size[1] - logo.size[1]) // 2)
        img_qr.paste(logo, pos, mask=logo if logo.mode == 'RGBA' else None)
    
    return img_qr

# Función para suavizar el QR
def suavizar_qr(imagen):
    return imagen.filter(ImageFilter.SMOOTH_MORE)

# Diseño atractivo y elementos visuales
def main():
    # Establecer título y fondo
    st.markdown("""
    <style>
    .reportview-container {
        background: linear-gradient(135deg, #6c5ce7, #00b894);
        color: white;
    }
    .sidebar .sidebar-content {
        background: #2d3436;
    }
    h1 {
        font-family: 'Arial', sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Título de la aplicación
    st.title("**Generador de Códigos QR Personalizados con Procesamiento de Imágenes**")
    st.markdown("##### ¡Ten la libertad de generar tus QR's para tus enlaces, textos e imagenes! 🚀")

    # Entrada para texto o enlace
    texto = st.text_input("Ingresa el enlace o texto para el QR:")

    # Selección de color del QR
    color = st.color_picker("🎨 Elige el color del QR", "#000000")

    # Selección de color de fondo
    fondo = st.color_picker("🎨 Elige el color de fondo", "#FFFFFF")

    # Cargar logo (opcional)
    logo = st.file_uploader("🖼️ Cargar un logo o imagen (opcional)", type=["png", "jpg", "jpeg"])
    if logo:
        st.image(logo, caption="Logo cargado", width=100)
    
    # Detectar color dominante del logo
    if logo:
        logo_img = Image.open(logo)
        color_dominante = detectar_color_dominante(logo_img)
        color = f'#{color_dominante[0]:02x}{color_dominante[1]:02x}{color_dominante[2]:02x}'
        st.write(f"🎨 Color dominante detectado: {color}")
    
    # Botón para generar el QR
    if st.button("Generar QR"):
        if texto:
            # Generar QR con logo y colores personalizados
            qr_img = generar_qr(texto, color, fondo, logo)
            qr_img = suavizar_qr(qr_img)
            
            # Mostrar el QR generado
            st.image(qr_img, caption="Código QR generado", use_column_width=True)
            
            # Permitir la descarga del QR
            buf = BytesIO()
            qr_img.save(buf, format="PNG")
            st.download_button(
                label="📥 Descargar QR",
                data=buf.getvalue(),
                file_name="codigo_qr.png",
                mime="image/png"
            )
        else:
            st.warning("⚠️ Por favor, ingresa un texto o enlace.")
    
if __name__ == "__main__":
    main()
