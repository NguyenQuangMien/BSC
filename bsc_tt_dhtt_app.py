
import streamlit as st

st.set_page_config(page_title="Tính điểm BSC - TTĐHTT", layout="wide")

st.title("📊 Ứng dụng tính điểm BSC hàng tháng - TTĐHTT")
st.markdown("### VNPT Yên Bái - Từ tháng 07/2025")

with st.expander("📝 Hướng dẫn nhập liệu"):
    st.markdown("""
    **CS1 – Chất lượng phục vụ (30%)**
    - T1: Thời gian mất liên lạc BTS (phút)
    - T2: Thời gian mất liên lạc NodeB (phút)
    - T3: Thời gian mất liên lạc eNodeB (phút)
    - S1 → S4: Sự cố mức 1 đến mức 4

    **CS2 – QoS / QoE (30%)**
    - FBB / MyTV / MBB QoS (%)
    - FBB / MyTV / MBB QoE (%)

    **CS3 – Tối ưu OLT (20%)**
    - Tổng số OLT giao
    - Số OLT đã tối ưu

    **CS4 – Xử lý PAKH (20%)**
    - Tổng phiếu
    - Phiếu đạt yêu cầu
    """)

# === Nhập dữ liệu ===
st.sidebar.header("📥 Nhập liệu")

# CS1
st.sidebar.subheader("CS1 - Mất liên lạc & sự cố")
T1 = st.sidebar.number_input("Thời gian mất liên lạc BTS (phút)", 0.0, 100.0, 5.0)
T2 = st.sidebar.number_input("Thời gian mất liên lạc NodeB (phút)", 0.0, 100.0, 5.0)
T3 = st.sidebar.number_input("Thời gian mất liên lạc eNodeB (phút)", 0.0, 100.0, 5.0)
S1 = st.sidebar.number_input("Sự cố mức 1", 0, 100, 0)
S2 = st.sidebar.number_input("Sự cố mức 2", 0, 100, 0)
S3 = st.sidebar.number_input("Sự cố mức 3", 0, 100, 0)
S4 = st.sidebar.number_input("Sự cố mức 4", 0, 100, 0)

# CS2
st.sidebar.subheader("CS2 - QoS / QoE")
QoS_FBB = st.sidebar.slider("QoS - FBB", 0.0, 100.0, 99.0)
QoS_MyTV = st.sidebar.slider("QoS - MyTV", 0.0, 100.0, 98.0)
QoS_MBB = st.sidebar.slider("QoS - MBB", 0.0, 100.0, 97.0)
QoE_FBB = st.sidebar.slider("QoE - FBB", 0.0, 100.0, 98.0)
QoE_MyTV = st.sidebar.slider("QoE - MyTV", 0.0, 100.0, 97.0)
QoE_MBB = st.sidebar.slider("QoE - MBB", 0.0, 100.0, 97.0)

# CS3
st.sidebar.subheader("CS3 - Tối ưu OLT")
olt_total = st.sidebar.number_input("Tổng số OLT được giao", 1, 100, 5)
olt_done = st.sidebar.number_input("Số OLT đã tối ưu", 0, 100, 5)

# CS4
st.sidebar.subheader("CS4 - Phiếu PAKH")
pak_total = st.sidebar.number_input("Tổng số phiếu", 1, 1000, 15)
pak_ok = st.sidebar.number_input("Số phiếu đạt yêu cầu", 0, 1000, 14)

# === Tính điểm ===
if st.button("✅ Tính điểm BSC"):
    # CS1
    time_avg = (T1 + T2 + T3) / 3
    diem_time = 5 if time_avg <= 9 else max(0, 5 - (time_avg - 9) * 0.5)
    tong_su_co = S1*4 + S2*3 + S3*2 + S4
    diem_su_co = max(0, 5 - tong_su_co * 0.1)
    diem_cs1 = round((diem_time + diem_su_co) / 2, 2)

    # CS2
    diem_qos = (QoS_FBB + QoS_MyTV + QoS_MBB) / 3
    diem_qoe = (QoE_FBB + QoE_MyTV + QoE_MBB) / 3
    diem_cs2 = round((diem_qos + diem_qoe) / 40, 2)

    # CS3
    ti_le_olt = olt_done / olt_total
    diem_cs3 = round(ti_le_olt * 5, 2)

    # CS4
    ti_le_pakh = pak_ok / pak_total
    diem_cs4 = round(ti_le_pakh * 5, 2)

    # Tổng điểm
    tong_diem = round(diem_cs1 * 0.3 + diem_cs2 * 0.3 + diem_cs3 * 0.2 + diem_cs4 * 0.2, 2)

    # Hiển thị kết quả
    st.success("🎯 KẾT QUẢ ĐÁNH GIÁ BSC")
    st.write(f"**CS1 - Chất lượng phục vụ:** {diem_cs1}/5")
    st.write(f"**CS2 - QoS/QoE:** {diem_cs2}/5")
    st.write(f"**CS3 - Tối ưu OLT:** {diem_cs3}/5")
    st.write(f"**CS4 - Phiếu xử lý PAKH:** {diem_cs4}/5")
    st.markdown(f"### 🏁 **TỔNG ĐIỂM BSC: {tong_diem} / 5.00**")

