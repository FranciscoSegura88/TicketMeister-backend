const express = require('express');
const nodemailer = require('nodemailer');
const cors = require('cors');
const bodyParser = require('body-parser');

// Cargar variables de entorno
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;  // Usar el puerto desde .env o 3000 por defecto

// Middleware
app.use(cors());
app.use(bodyParser.json());

// Configuración de Nodemailer
const transporter = nodemailer.createTransport({
  service: 'gmail',  // Usar Gmail como servicio de correo
  auth: {
    user: process.env.EMAIL_USER,  // Correo desde .env
    pass: process.env.EMAIL_PASS   // Contraseña desde .env
  }
});

// Ruta para enviar el correo
app.post('/send-email', (req, res) => {
  const { nombre, apellidos, correo, cantidad, evento, posterUrl } = req.body;

  const mailOptions = {
    from: process.env.EMAIL_USER,  // Correo desde .env
    to: correo,  // Correo del comprador
    subject: 'Confirmación de compra',
    html:`
      <div style="font-family: Arial, sans-serif; color: #333; max-width: 600px; margin: 0 auto; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
        <!-- Encabezado con gradiente -->
        <div style="background: linear-gradient(135deg, #F22E52, #FF6B6B); padding: 20px; text-align: center;">
          <h1 style="color: white; margin: 0;">¡Gracias por tu compra, ${nombre} ${apellidos}!</h1>
        </div>

        <!-- Imagen del evento -->
        <div style="width: 100%;">
          <img src="${posterUrl}" alt="Poster del evento" style="width: 100%; display: block;">
        </div>

        <!-- Información del evento -->
        <div style="padding: 20px;">
          <h2 style="color: #F22E52; margin-bottom: 20px;">Detalles de tu compra:</h2>
          <div style="font-size: 18px;">
            <p style="margin: 15px 0;"><strong>Evento:</strong> ${evento}</p>
            <p style="margin: 15px 0;"><strong>Cantidad de boletos:</strong> ${cantidad}</p>
            <p style="margin: 15px 0;"><strong>Teléfono de contacto:</strong> ${correo}</p>
          </div>
          <p style="margin-top: 20px; font-size: 16px;">¡Esperamos que disfrutes el evento!</p>
        </div>

        <!-- Pie de página -->
        <div style="background: #f9f9f9; padding: 20px; text-align: center;">
          <p style="margin: 0; font-size: 14px; color: #666;">Si tienes alguna pregunta, no dudes en contactarnos.</p>
        </div>
      </div>
    `
  };

  transporter.sendMail(mailOptions, (error, info) => {
    if (error) {
      console.error('Error al enviar el correo:', error);
      res.status(500).json({ success: false, message: 'Error al enviar el correo' });
    } else {
      console.log('Correo enviado:', info.response);
      res.json({ success: true, message: 'Correo enviado correctamente' });
    }
  });
});

// Iniciar el servidor
app.listen(PORT, () => {
  console.log(`Servidor corriendo en http://localhost:${PORT}`);
});
