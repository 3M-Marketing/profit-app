import streamlit as st
from PIL import Image
from fpdf import FPDF
import os

# ========================
# إعدادات الصفحة
# ========================
st.set_page_config(
    page_title="Profit Calculator",
    page_icon="logo.png",
    layout="centered"
)

# ========================
# تحميل الصور (لوغو وتوقيع)
# ========================
try:
    logo = Image.open("logo.png")
    signature = Image.open("signature.png")
except Exception as e:
    st.error(f"Error loading images: {e}")

# ========================
# عرض اللوجو في الواجهة
# ========================
st.image(logo, width=200)

# ========================
# اختيار اللغة
# ========================
lang = st.selectbox("Select Language / اختر اللغة", ["English", "العربية"], index=0)

# ========================
# النصوص حسب اللغة
# ========================
if lang == "English":
    texts = {
        "brand_status": "Select Brand Status",
        "existing_brand": "Existing Brand",
        "new_project": "New Project / Forecast",
        "enter_details": "Enter your project details to calculate profit and loss:",
        "selling_price": "Selling Price",
        "units_sold": "Units Sold",
        "manufacturing_cost": "Manufacturing Cost (per unit)",
        "packaging_cost": "Packaging Cost (per unit)",
        "ads_sales": "Ads Cost (Sales)",
        "ads_awareness": "Ads Cost (Awareness)",
        "photography_cost": "Photography Cost",
        "marketing_team": "Marketing Team Cost",
        "additional_details": "Additional Details (Optional)",
        "shipping_cost": "Shipping Cost (per unit, optional)",
        "return_cost": "Return Cost per Unit (optional)",
        "delivery_rate": "Successful Delivery Rate (%)",
        "calculate": "Calculate Results",
        "results": "Calculation Results:",
        "gross_revenue": "Gross Revenue",
        "total_costs": "Total Costs",
        "net_profit": "Net Profit",
        "return_rate": "Return Rate (%)",
        "units_returned": "Units Returned",
        "returns_cost": "Returns Cost",
        "cac": "Customer Acquisition Cost",
        "project_success": "Your project looks successful! Keep going!",
        "project_warning": "Warning! The project is not profitable. Revise your plan.",
        "consult": "Consult a Specialist",
        "consult_text": "Send your issue or inquiry and I'll help you via WhatsApp.",
        "send_message": "Send your message",
        "placeholder": "e.g., I have a project but don't know how to market it...",
        "developed": "Developed by Mohamed.A Marketing",
        "client_name": "Enter Client Name"
    }
else:
    texts = {
        "brand_status": "اختر نوع المشروع",
        "existing_brand": "براند شغال",
        "new_project": "مشروع جديد / توقع",
        "enter_details": "أدخل تفاصيل مشروعك لحساب الربح والخسارة:",
        "selling_price": "سعر البيع للمنتج الواحد",
        "units_sold": "عدد الوحدات المباعة",
        "manufacturing_cost": "تكلفة التصنيع (للوحدة)",
        "packaging_cost": "تكلفة التغليف (للوحدة)",
        "ads_sales": "تكلفة الإعلانات (مبيعات)",
        "ads_awareness": "تكلفة الإعلانات (وعي)",
        "photography_cost": "تكلفة التصوير",
        "marketing_team": "تكلفة فريق التسويق",
        "additional_details": "تفاصيل إضافية (اختياري)",
        "shipping_cost": "تكلفة الشحن (للوحدة، اختياري)",
        "return_cost": "تكلفة المرتجعات لكل وحدة (اختياري)",
        "delivery_rate": "نسبة التسليمات الناجحة (%)",
        "calculate": "احسب النتيجة",
        "results": "نتائج الحساب:",
        "gross_revenue": "إجمالي الإيرادات",
        "total_costs": "إجمالي التكاليف",
        "net_profit": "صافي الربح",
        "return_rate": "نسبة المرتجعات (%)",
        "units_returned": "عدد الوحدات المرتجعة",
        "returns_cost": "تكلفة المرتجعات",
        "cac": "تكلفة الحصول على العميل",
        "project_success": "المشروع ناجح! استمر!",
        "project_warning": "تحذير! المشروع خاسر. يجب مراجعة الخطة.",
        "consult": "استشارة متخصص",
        "consult_text": "ابعتلي مشكلتك أو استفسارك وأنا هساعدك على واتساب.",
        "send_message": "ابعت رسالتك",
        "placeholder": "مثلاً: عندي مشروع بس مش عارف أبدأ تسويقه...",
        "developed": "تم التطوير بواسطة Mohamed.A Marketing",
        "client_name": "ادخل اسم العميل"
    }

# ========================
# اسم العميل
# ========================
client_name = st.text_input(texts["client_name"], "")

# ========================
# اختيار نوع المشروع
# ========================
brand_status = st.radio(
    texts["brand_status"],
    [texts["existing_brand"], texts["new_project"]]
)

# ========================
# إدخال البيانات
# ========================
st.markdown(texts["enter_details"])
col1, col2 = st.columns(2)
with col1:
    selling_price = st.number_input(texts["selling_price"], min_value=0, value=0, step=10)
    units_sold = st.number_input(texts["units_sold"], min_value=0, value=0, step=1)
    manufacturing_cost = st.number_input(texts["manufacturing_cost"], min_value=0, value=0, step=10)
    packaging_cost = st.number_input(texts["packaging_cost"], min_value=0, value=0, step=10)
with col2:
    ads_sales = st.number_input(texts["ads_sales"], min_value=0, value=0, step=100)
    ads_awareness = st.number_input(texts["ads_awareness"], min_value=0, value=0, step=100)
    photography_cost = st.number_input(texts["photography_cost"], min_value=0, value=0, step=100)
    marketing_team = st.number_input(texts["marketing_team"], min_value=0, value=0, step=100)

# ========================
# تكاليف إضافية اختيارية
# ========================
st.markdown(texts["additional_details"])
col3, col4 = st.columns(2)
with col3:
    shipping_cost = st.number_input(texts["shipping_cost"], min_value=0, value=0, step=10)
    return_cost_per_unit = st.number_input(texts["return_cost"], min_value=0, value=0, step=10)
with col4:
    delivery_rate = st.slider(texts["delivery_rate"], min_value=0, max_value=100, value=100, step=1)
    return_rate = 100 - delivery_rate

# ========================
# الحسابات
# ========================
if st.button(texts["calculate"]):
    gross_revenue = selling_price * units_sold
    total_manufacturing = manufacturing_cost * units_sold
    total_packaging = packaging_cost * units_sold
    total_shipping = shipping_cost * units_sold
    ads_total = ads_sales + ads_awareness
    total_fixed = ads_total + photography_cost + marketing_team
    units_returned = (return_rate / 100) * units_sold
    returns_cost = units_returned * return_cost_per_unit
    total_costs = total_manufacturing + total_packaging + total_shipping + total_fixed + returns_cost
    net_profit = gross_revenue - total_costs
    delivered_units = (delivery_rate / 100) * units_sold
    cac = total_costs / delivered_units if delivered_units > 0 else 0

    # ========================
    # عرض النتائج
    # ========================
    st.markdown("---")
    st.subheader(texts["results"])
    col1, col2 = st.columns(2)
    with col1:
        st.metric(texts["gross_revenue"], f"{gross_revenue:,.2f}")
        st.metric(texts["total_costs"], f"{total_costs:,.2f}")
        st.metric(texts["net_profit"], f"{net_profit:,.2f}")
        st.metric(texts["cac"], f"{cac:,.2f}")
    with col2:
        st.metric(texts["return_rate"], f"{return_rate:.2f}%")
        st.metric(texts["units_returned"], f"{units_returned:,.2f}")
        st.metric(texts["returns_cost"], f"{returns_cost:,.2f}")

    # ========================
    # رسالة تقييم المشروع
    # ========================
    if net_profit > 0:
        st.success(texts["project_success"])
    else:
        st.error(texts["project_warning"])

    # ========================
    # إنشاء تقرير PDF مع اللوجو والتوقيع
    # ========================
    pdf = FPDF()
    pdf.add_page()
    # استخدم خط Unicode (تأكد انك مرفوع الخط في مجلد fonts)
    pdf.add_font("ArialUnicode", "", "fonts/Amiri-Regular.ttf", uni=True)
    pdf.set_font("ArialUnicode", size=14)

    # إضافة اللوجو أعلى التقرير
    pdf.image("logo.png", x=80, w=50)
    pdf.ln(20)

    pdf.cell(0, 10, f"Client Name: {client_name}", ln=True)
    pdf.ln(5)
    pdf.cell(0, 10, f"Brand Status: {brand_status}", ln=True)
    pdf.ln(5)
    pdf.cell(0, 10, f"{texts['gross_revenue']}: {gross_revenue:,.2f}", ln=True)
    pdf.cell(0, 10, f"{texts['total_costs']}: {total_costs:,.2f}", ln=True)
    pdf.cell(0, 10, f"{texts['net_profit']}: {net_profit:,.2f}", ln=True)
    pdf.cell(0, 10, f"{texts['return_rate']}: {return_rate:.2f}%", ln=True)
    pdf.cell(0, 10, f"{texts['units_returned']}: {units_returned:,.2f}", ln=True)
    pdf.cell(0, 10, f"{texts['returns_cost']}: {returns_cost:,.2f}", ln=True)
    pdf.cell(0, 10, f"{texts['cac']}: {cac:,.2f}", ln=True)
    pdf.ln(10)

    # إضافة التوقيع أسفل التقرير
    pdf.image("signature.png", x=80, w=50)
    pdf.ln(10)
    pdf.cell(0, 10, "Developed by Mohamed.A Marketing", ln=True, align="C")

    pdf.output("profit_report.pdf")
    with open("profit_report.pdf", "rb") as f:
        st.download_button("📥 Download PDF", f, file_name="profit_report.pdf")

# ========================
# قسم الاستشارة
# ========================
st.markdown("---")
st.subheader(texts["consult"])
st.markdown(texts["consult_text"])
user_msg = st.text_area("✉️", placeholder=texts["placeholder"], height=120)
if st.button(texts["send_message"]):
    if user_msg.strip():
        whatsapp_url = f"https://wa.me/201001753411?text={user_msg.replace(' ', '%20')}"
        st.info("Message prepared for WhatsApp 👇")
        st.markdown(
            f"<a href='{whatsapp_url}' target='_blank' "
            "style='display:inline-block; background:#25D366; color:white; padding:10px 20px; "
            "border-radius:8px; text-decoration:none; font-weight:bold;'>Open WhatsApp</a>",
            unsafe_allow_html=True
        )
    else:
        st.warning("Please enter a message first!")

# ========================
# الفوتر (أيقونات التواصل + Developed By)
# ========================
st.markdown("---")
st.markdown(
    f"""
    <div style='text-align:center; display:flex; justify-content:center; gap:10px; margin-bottom:20px;'>
        <a href='https://www.facebook.com/1mohamed.abdo.97' target='_blank'>
            <img src='https://cdn-icons-png.flaticon.com/512/733/733547.png
