import streamlit as st
import qrcode
from PIL import Image
import io
import os
from datetime import datetime

def generate_qr_code(data, fill_color="black", back_color="white", size=10):
    """
    Gera um QR code a partir dos dados fornecidos
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=size,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    return img

def save_qr_code(img, filename):
    """
    Salva a imagem do QR code
    """
    img.save(filename)

def main():
    st.title("🔍 Gerador de QR Code")
    st.write("Insira os dados abaixo para gerar seu QR Code personalizado")

    # Formulário para entrada de dados
    with st.form("qr_form"):
        data = st.text_area("Dados para codificar no QR Code:", 
                           placeholder="Texto, URL, ou qualquer informação...")
        
        col1, col2 = st.columns(2)
        with col1:
            fill_color = st.color_picker("Cor do QR Code", "#000000")
        with col2:
            back_color = st.color_picker("Cor de fundo", "#FFFFFF")
        
        size = st.slider("Tamanho do QR Code", 5, 20, 10)
        
        custom_name = st.text_input("Nome personalizado para o arquivo (opcional):")
        
        submitted = st.form_submit_button("Gerar QR Code")
    
    if submitted and data:
        try:
            # Gerar QR code
            img = generate_qr_code(data, fill_color, back_color, size)
            
            # Mostrar o QR code
            st.success("QR Code gerado com sucesso!")
            st.image(img.get_image(), caption="Seu QR Code")
            
            # Criar buffer para download
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            byte_im = buf.getvalue()
            
            # Sugerir nome do arquivo
            if not custom_name:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                custom_name = f"qr_code_{timestamp}"
            
            # Botão de download
            st.download_button(
                label="Baixar QR Code",
                data=byte_im,
                file_name=f"{custom_name}.png",
                mime="image/png"
            )
            
        except Exception as e:
            st.error(f"Ocorreu um erro ao gerar o QR Code: {e}")
    elif submitted and not data:
        st.warning("Por favor, insira algum dado para gerar o QR Code")

if __name__ == "__main__":
    main()