import streamlit as st
import pandas as pd
import datetime
from io import BytesIO
import matplotlib.pyplot as plt

st.set_page_config(page_title="BSC TTĐHTT", layout="wide")

# Khởi tạo hoặc tải dữ liệu cũ
@st.cache_data
def init_data():
    return pd.DataFrame(columns=[
        "Tháng", "Người nhập", "BTS (phút)", "NodeB (phút)", "eNodeB (phút)",
        "SC M1", "SC M2", "SC M3", "Điểm BSC"
    ])

data_store = init_data()

st.title("📊 Tính điểm BSC hàng tháng - TTĐHTT VNPT Yên Bái")

# Nhập liệu
col1, col2 = st.columns(2)
with col1:
    thang = st.date_input("🗓️ Chọn tháng", datetime.date.today())
    nguoi_nhap = st.text_input("👤 Tên người nhập", "Nguyễn Văn A")
    bts = st.number_input("📡 Thời gian mất liên lạc BTS (phút)", 0.0)
    nodeb = st.number_input("🔗 NodeB (phút)", 0.0)
    enodeb = st.number_input("🌐 eNodeB (phút)", 0.0)
with col2:
    sc1 = st.number_input("⚠️ Sự cố mức 1", 0)
    sc2 = st.number_input("⚠️ Sự cố mức 2", 0)
    sc3 = st.number_input("⚠️ Sự cố mức 3", 0)

# Hàm tính điểm
def tinh_diem(bts, nodeb, enodeb, sc1, sc2, sc3):
    diem = 100
    diem -= bts * 0.1
    diem -= nodeb * 0.05
    diem -= enodeb * 0.05
    diem -= sc1 * 5
    diem -= sc2 * 2
    diem -= sc3 * 1
    return round(max(diem, 0), 2)

if st.button("✅ Tính điểm BSC"):
    diem_bsc = tinh_diem(bts, nodeb, enodeb, sc1, sc2, sc3)
    st.success(f"🎯 Điểm BSC của {nguoi_nhap} tháng {thang.strftime('%m/%Y')}: {diem_bsc} điểm")

    # Cập nhật dữ liệu mới
    new_row = pd.DataFrame([{
        "Tháng": thang.strftime("%Y-%m"),
        "Người nhập": nguoi_nhap,
        "BTS (phút)": bts,
        "NodeB (phút)": nodeb,
        "eNodeB (phút)": enodeb,
        "SC M1": sc1,
        "SC M2": sc2,
        "SC M3": sc3,
        "Điểm BSC": diem_bsc
    }])
    data_store = pd.concat([data_store, new_row], ignore_index=True)

# Hiển thị bảng tổng hợp
if not data_store.empty:
    st.subheader("📋 Bảng tổng hợp điểm BSC các cá nhân")
    st.dataframe(data_store)

    # Bảng tổng hợp theo tháng
    st.subheader("📊 Trung bình điểm toàn đơn vị theo tháng")
    avg_table = data_store.groupby("Tháng")["Điểm BSC"].mean().reset_index(name="Điểm trung bình toàn đơn vị")
    st.dataframe(avg_table)

    # Biểu đồ tổng thể
    fig, ax = plt.subplots()
    ax.plot(avg_table["Tháng"], avg_table["Điểm trung bình toàn đơn vị"], marker='o', color='blue')
    ax.set_title("📈 Biểu đồ điểm trung bình BSC toàn TTĐHTT")
    ax.set_xlabel("Tháng")
    ax.set_ylabel("Điểm trung bình")
    ax.grid(True)
    st.pyplot(fig)

    # Tải về Excel
    def convert_df(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name="ChiTietCaNhan")
            avg_table.to_excel(writer, index=False, sheet_name="TongHopDonVi")
        return output.getvalue()

    st.download_button(
        label="📥 Tải toàn bộ kết quả về Excel",
        data=convert_df(data_store),
        file_name="BSC_TTĐHTT_ChiTiet_TongHop.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

