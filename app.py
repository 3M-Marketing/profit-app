import streamlit as st
import pandas as pd

# =====================
# إعدادات الصفحة
# =====================
st.set_page_config(page_title="3M - Digital Marketing", layout="centered")

# =====================
# اللوجو واسم الشركة
# =====================
st.image("logo.png", width=200)  # تأكد إن صورة اللوجو محفوظة بنفس اسم الملف "logo.png" جنب app.py
st.markdown("<h1 style='text-align: center; color: #2E86C1;'>3M - Digital Marketing</h1>", unsafe_allow_html=True)
st.markdown("---")

# =====================
# إدخال البيانات
# =====================
st.sidebar.header(" إدخال البيانات")

orders = st.sidebar.number_input("عدد الأوردرات الشهرية", min_value=1, value=100, step=1)
unit_cost = st.sidebar.number_input(" تكلفة التصنيع للوحدة (جنيه)", min_value=0, value=1220, step=10)
packaging_cost = st.sidebar.number_input(" تكلفة التغليف للوحدة (جنيه)", min_value=0, value=100, step=10)
marketing_cost_per_order = st.sidebar.number_input("📢 تكلفة الحصول على عميل (جنيه)", min_value=0, value=150, step=10)
selling_price = st.sidebar.number_input(" سعر البيع للوحدة", min_value=0, value=3000, step=100)

delivery_rates = [0.25, 0.50, 0.75, 1.0]

# =====================
# الحسابات
# =====================
rows = []
for rate in delivery_rates:
    delivered_orders = int(orders * rate)
    revenue = delivered_orders * selling_price
    total_costs = delivered_orders * (unit_cost + packaging_cost + marketing_cost_per_order)
    profit = revenue - total_costs
    rows.append([f"{int(rate*100)}%", delivered_orders, revenue, total_costs, profit])

df = pd.DataFrame(rows, columns=["نسبة التسليم", "الأوردرات المستلمة", "الإيرادات", "إجمالي التكاليف", "الربح"])

# =====================
# عرض النتائج
# =====================
st.subheader(" النتائج حسب السيناريوهات")
st.table(df)

# =====================
# الإمضاء
# =====================
st.markdown("---")
st.image("signature.png", width=200)  # لازم تحفظ الإمضاء كـ signature.png جنب app.py
st.markdown("<p style='text-align: center; color: gray;'>Made by Mohamed.A Marketing</p>", unsafe_allow_html=True)
