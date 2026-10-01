import streamlit as st
from datetime import datetime
from io import BytesIO

st.image("logo1.JPG")

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

st.write("📍 Địa chỉ quán: 1119B Đại lộ Bình Dương")

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

# =====================================
# GIÁ SIZE
# =====================================

SIZE_PRICE = {
    "S": 0,
    "M": 5000,
    "L": 10000
}

# =====================================
# TOPPING
# =====================================

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

phone = st.text_input("📱 Số điện thoại khách hàng")

# =====================================
# CHỌN NHIỀU MÓN
# =====================================

selected_drinks = st.multiselect(
    "🥤 Chọn thức uống",
    list(MENU.keys())
)

drink_quantities = {}
drink_sizes = {}

for drink in selected_drinks:

    drink_quantities[drink] = st.number_input(
        f"Số lượng {drink}",
        min_value=1,
        value=1,
        key=f"qty_{drink}"
    )

    drink_sizes[drink] = st.selectbox(
        f"Size {drink}",
        ["S", "M", "L"],
        key=f"size_{drink}"
    )

# =====================================
# ĐƯỜNG - ĐÁ
# =====================================

sugar = st.selectbox(
    "🍬 Mức độ đường",
    ["100%", "70%", "50%", "0%"]
)

ice = st.selectbox(
    "🧊 Mức độ đá",
    ["Đá riêng", "Không đá"]
)

# =====================================
# TOPPING
# =====================================

selected_toppings = st.multiselect(
    "➕ Chọn topping",
    list(TOPPINGS.keys())
)

# =====================================
# TÍNH TIỀN
# =====================================

total = 0

for drink in selected_drinks:

    size = drink_sizes[drink]

    unit_price = MENU[drink] + SIZE_PRICE[size]

    total += unit_price * drink_quantities[drink]

topping_price = sum(
    TOPPINGS[t]
    for t in selected_toppings
)

total += topping_price

points = total // 10000

# =====================================
# HÓA ĐƠN
# =====================================

st.markdown("---")
st.subheader("🧾 Hóa đơn")

st.write("📱 Số điện thoại:", phone)

for drink in selected_drinks:

    size = drink_sizes[drink]

    subtotal = (
        MENU[drink] + SIZE_PRICE[size]
    ) * drink_quantities[drink]

    st.write(
        f"• {drink} | Size {size} | "
        f"{drink_quantities[drink]} ly = "
        f"{subtotal:,.0f} VNĐ"
    )

st.write("🍬 Mức đường:", sugar)
st.write("🧊 Mức đá:", ice)

if selected_toppings:
    st.write(
        "➕ Topping:",
        ", ".join(selected_toppings)
    )
else:
    st.write("➕ Topping: Không")

st.success(
    f"💰 Tổng tiền: {total:,.0f} VNĐ"
)

st.info(
    f"⭐ Điểm tích lũy: {points} điểm"
)

# =====================================
# CHATBOT
# =====================================

st.markdown("---")
st.subheader("🤖 Chatbot hỗ trợ")

question = st.text_input(
    "Nhập câu hỏi của bạn"
)

if question:

    q = question.lower()

    if "địa chỉ" in q:
        st.success(
            "📍 Quán ở 1119B Đại lộ Bình Dương."
        )

    elif "giờ mở cửa" in q:
        st.success(
            "⏰ Quán mở cửa từ 07:00 đến 22:00."
        )

    elif "size" in q:
        st.success(
            "🥤 Quán có size S, M và L."
        )

    elif "topping" in q:
        st.success(
            "➕ Topping gồm: Trân châu đen, Trân châu trắng, Thạch trái cây, Pudding, Kem cheese."
        )

    else:
        st.info(
            "Xin lỗi, tôi chưa hiểu câu hỏi."
        )

# =====================================
# THANH TOÁN
# =====================================

if st.button("💳 THANH TOÁN"):

    invoice = f"""
MILK TEA SHOP
Địa chỉ: 1119B Đại lộ Bình Dương

Thời gian:
{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

SĐT:
{phone}

DANH SÁCH MÓN:
"""

    for drink in selected_drinks:

        size = drink_sizes[drink]

        subtotal = (
            MENU[drink] + SIZE_PRICE[size]
        ) * drink_quantities[drink]

        invoice += (
            f"\n- {drink}"
            f" | Size {size}"
            f" | {drink_quantities[drink]} ly"
            f" = {subtotal:,.0f} VNĐ"
        )

    invoice += f"""

Mức đường: {sugar}
Mức đá: {ice}

Topping:
{', '.join(selected_toppings) if selected_toppings else 'Không'}

Tổng tiền:
{total:,.0f} VNĐ

Điểm tích lũy:
{points} điểm

Cảm ơn quý khách!
"""

    file = BytesIO()
    file.write(invoice.encode("utf-8"))
    file.seek(0)

    st.success("✅ Thanh toán thành công!")

    st.download_button(
        "📄 Tải hóa đơn",
        data=file,
        file_name="HoaDon.txt",
        mime="text/plain"
    )
