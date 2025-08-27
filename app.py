import streamlit as st
from PIL import Image

# ========================
# إعدادات الصفحة
# ========================
st.set_page_config(
    page_title="Profit Calculator",
    page_icon="logo.png",
    layout="centered"
)

# ========================
# اختيار Light Mode (لو المستخدم في Dark Mode)
# ========================
light_mode = st.checkbox("تفعيل Light Mode")

if light_mode:
    bg_color = "#FFFFFF"
    logo = Image.open("logo_dark.png")        # نسخة سوداء
    signature = Image.open("signature_dark.png")
else:
    bg_color = "#000000"
    logo = Image.open("logo_light.png")       # نسخة بيضاء
    signature = Image.open("signature_light.png")

# تغيير خلفية الصفحة
st.markdown(
    f"""
    <style>
    .reportview-container {{
        background-color: {bg_color};
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ========================
# نص مساعد فوق اللوجو
# ========================
st.markdown(
    "<div style='text-align:center; font-size:16px; font-weight:bold; color:#333; margin-bottom:10px;'>ابعتلي هنا لو محتاج مساعدة</div>",
    unsafe_allow_html=True
)

# ========================
# اللوجو مع خلفية دائرية 3D
# ========================
st.markdown(
    """
    <div style='display:flex; justify-content:center;'>
        <div style='background-color:white; border-radius:30px; padding:20px; max-width:300px; 
                    box-shadow: 0 8px 16px rgba(0,0,0,0.2); text-align:center;'>
    """,
    unsafe_allow_html=True
)
st.image(logo, width=200)
st.markdown("</div></div>", unsafe_allow_html=True)

st.markdown("<h3 style='text-align:center; color:#003366;'>Profit Calculator</h3>", unsafe_allow_html=True)

# ========================
# إدخال البيانات
# ========================
st.markdown("### أدخل تفاصيل مشروعك لحساب الربح والخسارة:")

col1, col2 = st.columns(2)

with col1:
    selling_price = st.number_input("سعر البيع للمنتج الواحد", min_value=0, value=0, step=10)
    units_sold = st.number_input("عدد الوحدات المباعة", min_value=0, value=0, step=1)
    manufacturing_cost = st.number_input("تكلفة التصنيع (للوحدة)", min_value=0, value=0, step=10)
    packaging_cost = st.number_input("تكلفة التغليف (للوحدة)", min_value=0, value=0, step=10)

with col2:
    ads_sales = st.number_input("تكلفة الإعلانات (مبيعات)", min_value=0, value=0, step=100)
    ads_awareness = st.number_input("تكلفة الإعلانات (وعي)", min_value=0, value=0, step=100)
    photography_cost = st.number_input("تكلفة التصوير", min_value=0, value=0, step=100)
    marketing_team = st.number_input("تكلفة فريق التسويق", min_value=0, value=0, step=100)

# ========================
# تكاليف إضافية اختيارية
# ========================
st.markdown("### تفاصيل إضافية (اختياري)")
col3, col4 = st.columns(2)

with col3:
    shipping_cost = st.number_input(
        "تكلفة الشحن (للوحدة، اختياري)", min_value=0, value=0, step=10
    )
    return_cost_per_unit = st.number_input(
        "تكلفة المرتجعات لكل وحدة (اختياري)", min_value=0, value=0, step=10
    )

with col4:
    delivery_rate = st.slider("نسبة التسليمات الناجحة (%)", min_value=0, max_value=100, value=100, step=1)
    return_rate = 100 - delivery_rate

# ========================
# الحسابات
# ========================
if st.button("احسب النتيجة"):
    gross_revenue = selling_price * units_sold
    total_manufacturing = manufacturing_cost * units_sold
    total_packaging = packaging_cost * units_sold
    total_shipping = shipping_cost * units_sold if shipping_cost > 0 else 0
    ads_total = ads_sales + ads_awareness
    total_fixed = ads_total + photography_cost + marketing_team
    units_returned = (return_rate / 100) * units_sold
    returns_cost = units_returned * return_cost_per_unit if return_cost_per_unit > 0 else 0
    total_costs = total_manufacturing + total_packaging + total_shipping + total_fixed + returns_cost
    net_profit = gross_revenue - total_costs

    st.markdown("---")
    st.subheader("نتائج الحساب:")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("إجمالي الإيرادات", f"{gross_revenue:,.0f} جنيه")
        st.metric("إجمالي التكاليف", f"{total_costs:,.0f} جنيه")
        st.metric("صافي الربح", f"{net_profit:,.0f} جنيه")

    with col2:
        st.metric("نسبة المرتجعات (%)", f"{return_rate:.1f}%")
        st.metric("عدد الوحدات المرتجعة", f"{units_returned:,.0f} وحدة")
        st.metric("تكلفة المرتجعات", f"{returns_cost:,.0f} جنيه")

# ========================
# قسم الاستشارة
# ========================
st.markdown("---")
st.subheader("لو محتاج استشارة من المتخصص")
st.markdown(
    "<p style='color:#444; text-align:center;'>ابعتلي دلوقتي مشكلتك أو استفسارك، وأنا هكون معاك على واتساب علشان نلاقي الحل سوا</p>",
    unsafe_allow_html=True
)
user_msg = st.text_area("✉️ اكتب رسالتك هنا:", placeholder="مثلاً: عندي مشروع بس مش عارف أبدأ تسويقه...", height=120)
if st.button("ابعت رسالتك دلوقتي"):
    if user_msg.strip():
        whatsapp_url = f"https://wa.me/201001753411?text={user_msg.replace(' ', '%20')}"
        st.info("تم تجهيز رسالتك. هتتبعت دلوقتي على واتساب 👇")
        st.markdown(
            f"<a href='{whatsapp_url}' target='_blank' "
            "style='display:inline-block; background:#25D366; color:white; padding:10px 20px; "
            "border-radius:8px; text-decoration:none; font-weight:bold;'>افتح واتساب وأرسل الرسالة</a>",
            unsafe_allow_html=True
        )
    else:
        st.warning("من فضلك اكتب رسالتك الأول قبل ما تبعتها.")

# ========================
# توقيع مع خلفية دائرية 3D + نص Made By
# ========================
st.markdown(
    """
    <div style='display:flex; justify-content:center; margin-top:20px;'>
        <div style='background-color:white; border-radius:30px; padding:15px; max-width:250px; 
                    box-shadow: 0 8px 16px rgba(0,0,0,0.2); text-align:center;'>
    """,
    unsafe_allow_html=True
)
st.image(signature, width=180)
st.markdown("<p style='text-align:center; color:#555; margin-top:10px; font-size:16px;'>Made By <b>Mohamed.A Marketing</b></p>", unsafe_allow_html=True)
st.markdown("</div></div>", unsafe_allow_html=True)

# ========================
# الفوتر (أيقونات فيسبوك وواتساب مرة واحدة فقط)
# ========================
st.markdown("---")
st.markdown(
    """
    <div style='text-align:center; display:flex; justify-content:center; gap:10px; margin-bottom:20px;'>
        <a href='https://www.facebook.com/1mohamed.abdo.97' target='_blank'>
            <img src='https://cdn-icons-png.flaticon.com/512/733/733547.png' width='30'/>
        </a>
        <a href='https://wa.me/201001753411' target='_blank'>
            <img src='https://cdn-icons-png.flaticon.com/512/733/733585.png' width='30'/>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)
