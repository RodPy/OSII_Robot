import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Datos del remitente
email_sender = 'rodpy1@gmail.com'
email_password = '00.793793'

# Datos del destinatario
email_receiver = 'rodney.rojas@cjp.edu.py'

# Crear el mensaje
subject = 'Asunto del correo'
body = 'Este es el cuerpo del correo.'

msg = MIMEMultipart()
msg['From'] = email_sender
msg['To'] = email_receiver
msg['Subject'] = subject

msg.attach(MIMEText(body, 'plain'))

# Conectar al servidor SMTP
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()

# Iniciar sesión en el servidor
server.login(email_sender, email_password)

# Enviar el correo
text = msg.as_string()
server.sendmail(email_sender, email_receiver, text)

# Cerrar la conexión
server.quit()

print("Correo enviado con éxito")
