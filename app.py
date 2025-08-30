import streamlit as st
from fpdf import FPDF

# ========================
# إعدادات الصفحة
# ========================
st.set_page_config(
    page_title="Profit Calculator",
    page_icon="logo.png",
    layout="centered"
)

# ========================
# اختيار اللغة (English default)
# ========================
language = st.selectbox("Select Language / اختر اللغة:", ["English", "العربية"])
is_en = language == "English"

# ========================
# ترجمات النصوص
# ========================
texts = {
    "English": {
        "client_name": "Client Name",
        "brand_status": "Select Brand Status",
        "existing": "Existing Brand",
        "new": "New Project / Forecast",
        "enter_details": "Enter your project details to calculate profit and loss:",
        "selling_price": "Selling Price",
        "units_sold": "Units Sold",
        "manufacturing_cost": "Manufacturing Cost (per unit)",
        "packaging_cost": "Packaging Cost (per unit)",
        "ads_sales": "Ads Cost (Sales)",
        "ads_awareness": "Ads Cost (Awareness)",
        "photography_cost": "Photography Cost",
        "marketing_team": "Marketing Team Cost",
        "shipping_cost": "Shipping Cost (per unit, optional)",
        "return_cost_per_unit": "Return Cost per Unit (optional)",
        "delivery_rate": "Successful Delivery Rate (%)",
        "compute": "Compute",
        "results": "Calculation Results:",
        "gross_revenue": "Gross Revenue",
        "total_costs": "Total Costs",
        "net_profit": "Net Profit",
        "units_returned": "Units Returned",
        "returns_cost": "Returns Cost",
        "cac": "Customer Acquisition Cost",
        "evaluation": "Project Evaluation",
        "consult": "Consult a Specialist",
        "consult_desc": "Send your issue or inquiry and I'll help you via WhatsApp.",
        "send_msg": "Send Your Message Now"
    },
    "العربية": {
        "client_name": "اسم العميل",
        "brand_status": "اختر نوع المشروع",
        "existing": "براند شغال",
        "new": "مشروع جديد / تقديري",
        "enter_details": "أدخل تفاصيل مشروعك لحساب الربح والخسارة:",
        "selling_price": "سعر البيع للمنتج الواحد",
        "units_sold": "عدد الوحدات المباعة",
        "manufacturing_cost": "تكلفة التصنيع (للوحدة)",
        "packaging_cost": "تكلفة التغليف (للوحدة)",
        "ads_sales": "تكلفة الإعلانات (مبيعات)",
        "ads_awareness": "تكلفة الإعلانات (وعي)",
        "photography_cost": "تكلفة التصوير",
        "marketing_team": "تكلفة فريق التسويق",
        "shipping_cost": "تكلفة الشحن (للوحدة، اختياري)",
        "return_cost_per_unit": "تكلفة المرتجعات لكل وحدة (اختياري)",
        "delivery_rate": "نسبة التسليمات الناجحة (%)",
        "compute": "احسب النتيجة",
        "results": "نتائج الحساب:",
        "gross_revenue": "إجمالي الإيرادات",
        "total_costs": "إجمالي التكاليف",
        "net_profit": "صافي الربح",
        "units_returned": "عدد الوحدات المرتجعة",
        "returns_cost": "تكلفة المرتجعات",
        "cac": "تكلفة الحصول على العميل",
        "evaluation": "تقييم المشروع",
        "consult": "لو محتاج استشارة من المتخصص",
        "consult_desc": "ابعتلي دلوقتي مشكلتك أو استفسارك، وأنا هكون معاك على واتساب",
        "send_msg": "ابعت رسالتك دلوقتي"
    }
}

t = texts["English"] if is_en else texts["العربية"]

# ========================
# إدخال اسم العميل
# ========================
client_name = st.text_input(f"{t['client_name']}:")

# ========================
# اختيار نوع المشروع
# ========================
project_type = st.selectbox(t["brand_status"], [t["existing"], t["new"]])

# ========================
# إدخال البيانات
# ========================
st.markdown(t["enter_details"])

col1, col2 = st.columns(2)

with col1:
    selling_price = st.number_input(t["selling_price"], min_value=0, value=0, step=10)
    units_sold = st.number_input(t["units_sold"], min_value=0, value=0, step=1)
    manufacturing_cost = st.number_input(t["manufacturing_cost"], min_value=0, value=0, step=10)
    packaging_cost = st.number_input(t["packaging_cost"], min_value=0, value=0, step=10)

with col2:
    ads_sales = st.number_input(t["ads_sales"], min_value=0, value=0, step=100)
    ads_awareness = st.number_input(t["ads_awareness"], min_value=0, value=0, step=100)
    photography_cost = st.number_input(t["photography_cost"], min_value=0, value=0, step=100)
    marketing_team = st.number_input(t["marketing_team"], min_value=0, value=0, step=100)

col3, col4 = st.columns(2)

with col3:
    shipping_cost = st.number_input(t["shipping_cost"], min_value=0, value=0, step=10)
    return_cost_per_unit = st.number_input(t["return_cost_per_unit"], min_value=0, value=0, step=10)

with col4:
    delivery_rate = st.slider(t["delivery_rate"], min_value=0, max_value=100, value=100, step=1)
    return_rate = 100 - delivery_rate

# ========================
# الحسابات + عرض النتائج + PDF
# ========================
if st.button(t["compute"]):
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
    cac = total_costs / max(units_sold,1)

    # Project evaluation
    if net_profit < 0:
        msg = "Warning: Net profit is negative! Review your plan."
    elif project_type == t["existing"]:
        msg = "Project looks profitable." if net_profit >=0 else "Project not profitable yet. Work on your plan."
    else:
        msg = "Project not profitable yet. Work on your plan." if net_profit <0 else "Project looks profitable."

    # عرض النتائج
    st.markdown("---")
    st.subheader(t["results"])
    st.markdown(f"{t['gross_revenue']}: {gross_revenue:,.2f}")
    st.markdown(f"{t['total_costs']}: {total_costs:,.2f}")
    st.markdown(f"{t['net_profit']}: {net_profit:,.2f}")
    st.markdown(f"{t['units_returned']}: {units_returned:,.2f}")
    st.markdown(f"{t['returns_cost']}: {returns_cost:,.2f}")
    st.markdown(f"{t['cac']}: {cac:,.2f}")
    st.markdown(f"{t['evaluation']}: {msg}")

    # إنشاء PDF بالإنجليزية فقط
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("Amiri", "", "fonts/Amiri-Regular.ttf", uni=True)
    pdf.set_font("Amiri", size=14)
    pdf.cell(0,10,f"Client Name: {client_name}", ln=True)
    pdf.cell(0,10,f"Gross Revenue: {gross_revenue:,.2f}", ln=True)
    pdf.cell(0,10,f"Total Costs: {total_costs:,.2f}", ln=True)
    pdf.cell(0,10,f"Net Profit: {net_profit:,.2f}", ln=True)
    pdf.cell(0,10,f"Units Returned: {units_returned:,.2f}", ln=True)
    pdf.cell(0,10,f"Returns Cost: {returns_cost:,.2f}", ln=True)
    pdf.cell(0,10,f"Customer Acquisition Cost: {cac:,.2f}", ln=True)
    pdf.cell(0,10,f"Project Evaluation: {msg}", ln=True)
    pdf.ln(10)
    pdf.cell(0,10,"Developed by Mohamed.A Marketing", ln=True, align="C")
    pdf_file = "profit_report.pdf"
    pdf.output(pdf_file)
    with open(pdf_file,"rb") as f:
        st.download_button("📥 Download PDF Report", f, file_name=pdf_file)

# ========================
# استشارة تواصل
# ========================
st.markdown("---")
st.subheader(t["consult"])
st.markdown(f"<p>{t['consult_desc']}</p>", unsafe_allow_html=True)
user_msg = st.text_area("✉️", placeholder="Write your issue here..." if is_en else "اكتب رسالتك هنا:", height=120)
if st.button(t["send_msg"]):
    if user_msg.strip():
        whatsapp_url = f"https://wa.me/201001753411?text={user_msg.replace(' ','%20')}"
        st.info("Message ready to send via WhatsApp" if is_en else "تم تجهيز رسالتك")
        st.markdown(f"<a href='{whatsapp_url}' target='_blank' style='display:inline-block; background:#25D366; color:white; padding:10px 20px; border-radius:8px; text-decoration:none; font-weight:bold;'>Open WhatsApp</a>", unsafe_allow_html=True)
    else:
        st.warning("Please write a message first." if is_en else "من فضلك اكتب رسالتك أولاً")

# ========================
# Footer - social icons
# ========================
st.markdown("---")
st.markdown("""
<div style='text-align:center; display:flex; justify-content:center; gap:10px; margin-bottom:20px;'>
    <a href='https://www.facebook.com/1mohamed.abdo.97' target='_blank'>
        <img src='https://cdn-icons-png.flaticon.com/512/733/733547.png' width='30'/>
    </a>
    <a href='https://wa.me/201001753411' target='_blank'>
        <img src='https://cdn-icons-png.flaticon.com/512/733/733585.png' width='30'/>
    </a>
</div>
""", unsafe_allow_html=True)
