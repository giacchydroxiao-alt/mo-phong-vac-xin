import streamlit as st
import folium
from streamlit_folium import st_folium

# 1. Cấu hình trang
st.set_page_config(layout="wide")
st.title("Mô phỏng Định tuyến Vắc-xin")

# 2. Định nghĩa lộ trình (Bạn có thể thêm nhiều điểm hơn vào `coords` để đường đi uốn lượn đẹp hơn)
tuyen_duong = {
    "Lộ trình 1 (14km)": {
        "coords": [
            [10.803, 106.663], # Điểm đầu
            [10.810, 106.650], # Điểm giữa 1
            [10.815, 106.620], # Điểm giữa 2
            [10.825, 106.589]  # Điểm đích
        ],
        "color": "red"
    }
}

# 3. Tạo bản đồ
m = folium.Map(location=[10.815, 106.620], zoom_start=14)

# 4. Vẽ đường đi
chon_tuyen = st.selectbox("Chọn lộ trình:", list(tuyen_duong.keys()))
data = tuyen_duong[chon_tuyen]

folium.PolyLine(locations=data["coords"], color=data["color"], weight=6).add_to(m)

# 5. HIỂN THỊ CHUẨN (Dùng st_folium thay vì folium_static để tương tác được)
st_folium(m, width=800, height=500)