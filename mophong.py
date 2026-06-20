import streamlit as st
import folium
from streamlit_folium import st_folium

# 1. CẤU HÌNH GIAO DIỆN WEB
st.set_page_config(page_title="Mô phỏng Định tuyến Vắc-xin", layout="wide")
st.title("Chương 5: Mô phỏng AI Định tuyến & Cảnh báo Nhiệt độ Vắc-xin")

# 2. KHAI BÁO THÔNG SỐ (Số liệu thực tế từ Google My Maps)
temp_start = 2.0  # Nhiệt độ xuất phát an toàn
tuyen_duong = {
    "Lộ trình 1 (14km - Đường thẳng, Kẹt xe, Nắng nóng)": {
        "km": 14, 
        "thoi_gian_phut": 38, 
        "tang_nhiet": 0.3, # Hệ số rủi ro nhiệt cao
        "color": "red",
        "coords": [[10.803, 106.663], [10.808, 106.640], [10.825, 106.589]] # Tọa độ vẽ đường tượng trưng
    },
    "Lộ trình 2 (17km - AI điều hướng đi vòng, Râm mát)": {
        "km": 17, 
        "thoi_gian_phut": 46, 
        "tang_nhiet": 0.1, # Hệ số rủi ro nhiệt thấp
        "color": "green",
        "coords": [[10.803, 106.663], [10.820, 106.650], [10.830, 106.610], [10.825, 106.589]] 
    }
}

# 3. THANH ĐIỀU KHIỂN (Bên trái)
st.sidebar.header("🕹️ Bảng điều khiển")
chon_tuyen = st.sidebar.selectbox("Chọn kịch bản định tuyến:", list(tuyen_duong.keys()))

# 4. TÍNH TOÁN LOGIC TỪ EXCEL
thong_so = tuyen_duong[chon_tuyen]
nhiet_do_cuoi = temp_start + (thong_so["thoi_gian_phut"] * thong_so["tang_nhiet"])

# Xét luật của AI (Ngưỡng 8°C)
if nhiet_do_cuoi > 8.0:
    trang_thai = "🔴 CẢNH BÁO: VẮC-XIN HỎNG (> 8°C)"
else:
    trang_thai = "🟢 AN TOÀN: ĐẠT CHUẨN (2-8°C)"

# 5. HIỂN THỊ KẾT QUẢ RA MÀN HÌNH CHÍNH
col1, col2, col3 = st.columns(3)
col1.metric("Quãng đường", f"{thong_so['km']} km")
col2.metric("Thời gian di chuyển", f"{thong_so['thoi_gian_phut']} phút")
col3.metric("Nhiệt độ dự báo lúc đến", f"{round(nhiet_do_cuoi, 1)} °C", trang_thai)

# 6. VẼ BẢN ĐỒ MINH HỌA LÊN WEB
st.subheader("🗺️ Bản đồ mô phỏng định tuyến động")
m = folium.Map(location=[10.815, 106.620], zoom_start=13)

# Vẽ đường đi trên bản đồ
folium.PolyLine(
    locations=thong_so["coords"],
    color=thong_so["color"],
    weight=6,
    tooltip=chon_tuyen
).add_to(m)

# Đánh dấu Điểm đi và Điểm đến
folium.Marker(thong_so["coords"][0], popup="Kho VNVC Phú Nhuận (Điểm đi)").add_to(m)
folium.Marker(thong_so["coords"][-1], popup="Trạm Y tế Vĩnh Lộc A (Điểm đến)").add_to(m)

# Hiển thị
st_folium(m, width=900, height=450)