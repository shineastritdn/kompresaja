from flask import Flask, render_template, request, jsonify, send_file
import os
from werkzeug.utils import secure_filename
import zipfile
import magic
from PIL import Image
import io
import tempfile
import traceback
import shutil

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'docx', 'csv'}

# Buat folder uploads jika belum ada
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def compress_file(file_path, file_type):
    try:
        if file_type.startswith('image/'):
            # Kompresi gambar
            img = Image.open(file_path)
            output = io.BytesIO()
            img.save(output, format=img.format, optimize=True, quality=85)
            return output.getvalue()
        else:
            # Kompresi file lain menggunakan zip
            output = io.BytesIO()
            with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Pastikan file masih ada sebelum dikompresi
                if os.path.exists(file_path):
                    zipf.write(file_path, os.path.basename(file_path))
                else:
                    raise FileNotFoundError(f"File tidak ditemukan: {file_path}")
            return output.getvalue()
    except Exception as e:
        print(f"Error compressing file: {str(e)}")
        raise

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    temp_file_path = None
    compressed_path = None
    
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Tidak ada file yang diunggah'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Tidak ada file yang dipilih'}), 400
        
        if file and allowed_file(file.filename):
            # Buat nama file yang aman
            filename = secure_filename(file.filename)
            temp_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            # Simpan file sementara
            file.save(temp_file_path)
            
            try:
                # Deteksi tipe file
                file_type = magic.from_file(temp_file_path, mime=True)
                
                # Dapatkan ukuran file asli
                original_size = os.path.getsize(temp_file_path)
                
                # Kompres file
                compressed_data = compress_file(temp_file_path, file_type)
                
                # Simpan file terkompresi
                compressed_filename = f"compressed_{filename}.zip"
                compressed_path = os.path.join(app.config['UPLOAD_FOLDER'], compressed_filename)
                
                with open(compressed_path, 'wb') as f:
                    f.write(compressed_data)
                
                # Hapus file asli setelah berhasil dikompresi
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)
                
                return jsonify({
                    'success': True,
                    'original_size': original_size,
                    'compressed_size': len(compressed_data),
                    'filename': compressed_filename
                })
            except Exception as e:
                # Hapus file sementara jika terjadi error
                if temp_file_path and os.path.exists(temp_file_path):
                    os.remove(temp_file_path)
                if compressed_path and os.path.exists(compressed_path):
                    os.remove(compressed_path)
                return jsonify({'error': f'Error saat kompresi: {str(e)}'}), 500
        
        return jsonify({'error': 'Tipe file tidak didukung'}), 400
    
    except Exception as e:
        # Hapus semua file sementara jika terjadi error
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        if compressed_path and os.path.exists(compressed_path):
            os.remove(compressed_path)
        print(f"Unexpected error: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': 'Terjadi kesalahan server'}), 500

@app.route('/download/<filename>')
def download_file(filename):
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if not os.path.exists(file_path):
            return jsonify({'error': 'File tidak ditemukan'}), 404
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({'error': f'Error saat download: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True) 