import streamlit as st
from datetime import datetime
from io import BytesIO

# Hiển thị ảnh trà sữa
st.image("logo1 .JPG")

# =====================================
# CẤU HÌNH TRANG
# =====================================

st.set_page_config(
    page_title="Milk Tea Shop",
    page_icon="🧋",
    layout="centered"
)

# =====================================
# TIÊU ĐỀ
# =====================================

st.title("🧋 MILK TEA SHOP")
st.subheader("Hệ thống tính hóa đơn quán trà sữa")

st.markdown("---")

# =====================================
# MENU THỨC UỐNG
# =====================================

MENU = {
    "Trà sữa truyền thống": 30000,
    "Trà sữa trân châu đường đen": 35000,
    "Trà đào": 28000,
    "Trà vải": 28000,
    "Matcha Latte": 42000
}

TOPPINGS = {
    "Trân châu đen": 5000,
    "Trân châu trắng": 5000,
    "Thạch trái cây": 7000,
    "Pudding": 8000,
    "Kem cheese": 10000
}

# =====================================
# THÔNG TIN KHÁCH HÀNG
# =====================================

phone = st.text_input(
    "📱 Số điện thoại khách hàng"
)

drink = st.selectbox(
    "🥤 Chọn thức uống",
    list(MENU.keys())
)

quantity = st.number_input(
    "🔢 Số lượng",
    min_value=1,
    value=1
)

sugar = st.selectbox(
    "🍬 Mức độ đường",
    ["100%", "70%", "50%", "0%"]
)

ice = st.selectbox(
    "🧊 Mức độ đá",
    ["Đá riêng", "Không đá"]
)

selected_toppings = st.multiselect(
    "➕ Chọn topping",
    list(TOPPINGS.keys())
)

# =====================================
# TÍNH TIỀN
# =====================================

drink_price = MENU[drink]

topping_price = sum(
    TOPPINGS[t]
    for t in selected_toppings
)

total = (drink_price + topping_price) * quantity

points = total // 10000

# =====================================
# HIỂN THỊ HÓA ĐƠN
# =====================================

st.markdown("---")
st.subheader("🧾 Hóa đơn")

st.write("**Số điện thoại:**", phone)
st.write("**Thức uống:**", drink)
st.write("**Số lượng:**", quantity)
st.write("**Mức đường:**", sugar)
st.write("**Mức đá:**", ice)

if selected_toppings:
    st.write(
        "**Topping:**",
        ", ".join(selected_toppings)
    )
else:
    st.write("**Topping:** Không")

st.write(
    "**Tổng tiền:**",
    f"{total:,.0f} VNĐ"
)

if phone:
    st.write(
        f"⭐ Điểm tích lũy: {points} điểm"
    )

# =====================================
# THANH TOÁN
# =====================================

if st.button("💳 THANH TOÁN"):

    invoice = f"""
MILK TEA SHOP

Thời gian: {datetime.now()}

SĐT: {phone}

Thức uống: {drink}
Số lượng: {quantity}

Mức đường: {sugar}
Mức đá: {ice}

Topping:
{', '.join(selected_toppings) if selected_toppings else 'Không'}

Tổng tiền: {total:,.0f} VNĐ

Điểm tích lũy: {points}
"""

    file = BytesIO()
    file.write(invoice.encode("utf-8"))
    file.seek(0)

    st.success("Thanh toán thành công!")

    st.download_button(
        "📄 Tải hóa đơn",
        data=file,
        file_name="HoaDon.txt",
        mime="text/plain"
    )
