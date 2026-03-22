import os
from dotenv import load_dotenv
from google import genai # Thư viện mới đây Minh nhé

load_dotenv()

# Khởi tạo Client theo chuẩn mới
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

try:
    print("--- 🚀 Đang kết nối bằng thư viện GENAI mới... ---")
    # Cách gọi model của thư viện mới
    response = client.models.generate_content(
        model="gemini-3-flash-preview", 
        contents="Chào bạn, tôi là Minh từ HUST. Hãy xác nhận kết nối thành công!"
    )
    print("\n✅ KẾT QUẢ:")
    print(response.text)
except Exception as e:
    print(f"Lỗi: {e}")