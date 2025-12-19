from flask import Flask, request, send_file, jsonify
from weasyprint import HTML
import io

app = Flask(__name__)

@app.route('/convertir', methods=['POST'])
def html_to_pdf():
    # 1. Validar que el archivo esté en la petición
    if 'archivo' not in request.files:
        return jsonify({"error": "No se proporcionó el archivo 'archivo'"}), 400
    
    file = request.files['archivo']

    if file.filename == '':
        return jsonify({"error": "Nombre de archivo vacío"}), 400

    if not file.filename.endswith('.html'):
        return jsonify({"error": "El archivo debe ser de extensión .html"}), 400

    try:
        # 2. Leer el contenido del archivo HTML
        html_content = file.read().decode('utf-8')

        # 3. Convertir HTML a PDF usando WeasyPrint
        # Generamos el PDF directamente en un buffer de memoria
        pdf_buffer = io.BytesIO()
        
        # HTML(string=...) permite pasar el código HTML directamente
        # Si el HTML tuviera estilos externos o imágenes, se puede configurar 'base_url'
        HTML(string=html_content).write_pdf(pdf_buffer)
        
        # Volver al inicio del buffer para que Flask pueda leerlo
        pdf_buffer.seek(0)

        # 4. Enviar el archivo PDF de vuelta
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name='documento.pdf'
        )

    except Exception as e:
        return jsonify({"error": f"Error al procesar el PDF: {str(e)}"}), 500

if __name__ == '__main__':
    # Ejecutar en modo debug para desarrollo
    app.run(host='0.0.0.0', port=5000)
