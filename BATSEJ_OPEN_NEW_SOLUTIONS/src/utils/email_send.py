import smtplib
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Configuración de Mailtrap
MAILTRAP_SERVER = "smtp.mailtrap.io"
MAILTRAP_PORT = 2525
MAILTRAP_USERNAME = "c2de57f0dc8cd8"
MAILTRAP_PASSWORD = "c2afab0d7e9cc6"

def enviar_resumen_facturas(facturas_resumidas, destinatario):
    if not facturas_resumidas:
        print("⚠️ No hay facturas para enviar.")
        return

    # Crear tabla HTML con los datos
    df_comercios = pd.DataFrame(facturas_resumidas, columns=[
        "Fecha-Mes", "Nombre", "NIT", "Valor Comisión", "Valor IVA", "Valor Total", "Correo"
    ])
    tabla_html = df_comercios.to_html(index=False, header=True)

    # Configurar el correo
    mensaje = MIMEMultipart()
    mensaje["From"] = "noreply@pruebas.com"  # Mailtrap no requiere un email real
    mensaje["To"] = destinatario
    mensaje["Subject"] = "Resumen de Facturas - Open Finance"

    # Contenido del correo en HTML
    cuerpo_msj = f"""
    <html>
    <body>
        <p>A quien pueda interesar,</p>
        <p>Adjunto los resultados de las facturas generadas:</p>
        {tabla_html}
        <p>Saludos,<br><b>BATSEJ OPEN FINANCE S.A</b></p>
    </body>
    </html>
    """
    mensaje.attach(MIMEText(cuerpo_msj, "html", _charset="utf-8"))

    # Enviar correo
    try:
        with smtplib.SMTP(MAILTRAP_SERVER, MAILTRAP_PORT) as server:
            server.starttls()  # Seguridad TLS
            server.login(MAILTRAP_USERNAME, MAILTRAP_PASSWORD)
            server.sendmail(mensaje["From"], destinatario, mensaje.as_string())
        print(f"📧 Enviando correo a {destinatario}")

    except smtplib.SMTPAuthenticationError:
        print("❌ Error de autenticación. Verifica tu usuario/contraseña en Mailtrap.")

    except smtplib.SMTPException as e:
        print(f"❌ Error al enviar el correo: {e}")

    except Exception as e:
        print(f"❌ Error inesperado: {e}")


