from flask import Flask, jsonify, request
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)  # Áp dụng CORS cho toàn bộ ứng dụng

# Biến để lưu trạng thái hệ thống (bật/tắt)
system_active = False

# API để bật/tắt hệ thống
@app.route('/toggle', methods=['POST', 'GET'])
def toggle_system():
    global system_active
    if request.method == 'POST':
        system_active = not system_active  # Đảo trạng thái hệ thống
    status = "Bật" if system_active else "Tắt"
    return jsonify({"message": f"Hệ thống đã {status}", "status": system_active})

# API để lấy trạng thái hiện tại của hệ thống
@app.route('/status', methods=['GET'])
def get_status():
    status = "Bật" if system_active else "Tắt"
    return jsonify({"status": system_active, "message": f"Hệ thống đang {status}"})

if __name__ == '__main__':
    app.run(debug=True)
