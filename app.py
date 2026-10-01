# ==============================
# APP QUẢN LÝ HÓA ĐƠN TRÀ SỮA
# File: app.py
# Chạy:
# pip install streamlit pillow
# streamlit run app.py
# ==============================

import streamlit as st
from PIL import Image
from datetime import datetime
from io import BytesIO
import os

# ==============================
# CẤU HÌNH TRANG
# ==============================
st.set_page_config(
    page_title="Milk Tea Shop",
    page_icon="🧋",
    layout="centered"
)

# ==============================
# LOGO QUÁN
# ==============================
if os.path.exists("logo.png"):
    logo = Image.open("logo.png")

    col1, col2 = st.columns([1, 4])

    with col1:
        st.image(logo, width=100)

    with col2:
        st.title("🧋 MILK TEA SHOP")
        st.caption("Hệ thống thanh toán và xuất hóa đơn")
else:
    st.title("🧋 MILK TEA SHOP")
    st.caption("Hệ thống thanh toán và xuất hóa đơn")

st.markdown("---")

# ==============================
# MENU ĐỒ UỐNG
# ==============================
MENU = {
    "Trà sữa truyền thống": 30000,
    "Trà sữa trân châu đường đen": 35000,
    "Trà sữa matcha": 38000,
    "Trà đào": 28000,
    "Trà vải": 28000,
    "Trà chanh": 25000,
    "Matcha Latte": 42000,
    "Matcha Latte Kem Cheese": 48000
}

# ==============================
# TOPPING
# ==============================
TOPPINGS = {
    "Trân châu đen": 5000,
    "Trân châu trắng": 5000,
    "Thạch trái cây": 7000,
    "Pudding": 8000,
    "Kem cheese": 10000
}

# ==============================
# THÔNG TIN KHÁCH HÀNG
# ==============================
st.subheader("📋 Thông tin khách hàng")

phone = st.text_input(
    "📱 Số điện thoại tích điểm",
    placeholder="Nhập số điện thoại"
)

# ==============================
# CHỌN THỨC UỐNG
# ==============================
st.subheader("🥤 Chọn đồ uống")

drink = st.selectbox(
    "Loại thức uống",
    list(MENU.keys())
)

quantity = st.number_input(
    "Số lượng",
    min_value=1,
    value=1,
    step=1
)

# ==============================
# CHỌN ĐƯỜNG - ĐÁ
# ==============================
col1, col2 = st.columns(2)

with col1:
    sugar = st.selectbox(
        "🍬 Mức đường",
        ["100%", "70%", "50%", "0%"]
    )

with col2:
    ice = st.selectbox(
        "🧊 Mức đá",
        ["Đá riêng", "Không đá"]
    )

# ==============================
# CHỌN TOPPING
# ==============================
st.subheader("➕ Topping")

selected_toppings = st.multiselect(
    "Chọn topping",
    list(TOPPINGS.keys())
)

# ==============================
# TÍNH TIỀN
# ==============================
drink_price = MENU[drink]

topping_price = sum(
    TOPPINGS[item]
    for item in selected_toppings
)

unit_price = drink_price + topping_price
total_amount = unit_price * quantity

# ==============================
# TÍCH ĐIỂM
# 1 điểm = 10.000 VNĐ
# ==============================
reward_points = total_amount // 10000

# ==============================
# HIỂN THỊ HÓA ĐƠN TẠM TÍNH
# ==============================
st.markdown("---")
st.subheader("🧾 Hóa đơn tạm tính")

st.write(f"**Khách hàng:** {phone if phone else 'Chưa nhập'}")
st.write(f"**Thức uống:** {drink}")
st.write(f"**Số lượng:** {quantity}")
st.write(f"**Mức đường:** {sugar}")
st.write(f"**Mức đá:** {ice}")

if selected_toppings:
    topping_text = ", ".join(selected_toppings)
else:
    topping_text = "Không"

st.write(f"**Topping:** {topping_text}")

st.write(f"**Đơn giá:** {unit_price:,.0f} VNĐ")

st.success(
    f"💰 Tổng thanh toán: {total_amount:,.0f} VNĐ"
)

if phone:
    st.info(
        f"⭐ Điểm tích lũy nhận được: {reward_points} điểm"
    )

# ==============================
# TẠO NỘI DUNG HÓA ĐƠN
# ==============================
invoice_time = datetime.now().strftime(
    "%d/%m/%Y %H:%M:%S"
)

invoice_content = f"""
==========================================
            MILK TEA SHOP
==========================================

THỜI GIAN:
{invoice_time}

SỐ ĐIỆN THOẠI:
{phone}

THỨC UỐNG:
{drink}

SỐ LƯỢNG:
{quantity}

MỨC ĐƯỜNG:
{sugar}

MỨC ĐÁ:
{ice}

TOPPING:
{topping_text}

ĐƠN GIÁ:
{unit_price:,.0f} VNĐ

TỔNG THANH TOÁN:
{total_amount:,.0f} VNĐ

ĐIỂM TÍCH LŨY:
{reward_points}

==========================================
CẢM ƠN QUÝ KHÁCH!
==========================================
"""

# ==============================
# THANH TOÁN
# ==============================
st.markdown("---")

if st.button("💳 THANH TOÁN"):

    st.success("✅ Thanh toán thành công!")

    invoice_file = BytesIO()
    invoice_file.write(
        invoice_content.encode("utf-8")
    )
    invoice_file.seek(0)

    st.download_button(
        label="📄 Tải hóa đơn",
        data=invoice_file,
        file_name=f"HoaDon_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
        mime="text/plain"
    )

    st.balloons()
