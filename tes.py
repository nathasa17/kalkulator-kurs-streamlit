import streamlit as st
import requests

# =========================================================
# KODE APLIKASI UTAMA ANDA
# =========================================================

# 1. Konfigurasi Halaman Web
st.set_page_config(page_title="SaaS Konversi Mata Uang", page_icon="💱", layout="centered")

st.title("💱 Kalkulator Konversi Mata Uang")
st.write("Aplikasi konversi mata uang global dengan kurs real-time menggunakan Python & Streamlit.")

# =========================================================
# IDENTITAS PEMBUAT (SIDEBAR)
# =========================================================
with st.sidebar:
    st.image ("https://cdn-icons-png.flaticon.com/512/6997/6997662.png", width=100)
    st.title("Profil Pengembang")
    st.markdown("---")
    st.markdown("Nabila Shandy Nathasa")
    st.markdown("2313000005")
    st.markdown("Sistem Informasi")
    st.markdown("---")
    st.caption("© 2026 Hak Cipta Dilindungi.")

# 2. Ambil Data Kurs Terbaru dari API Gratis
@st.cache_data(ttl=3600)
def ambil_data_kurs():
    url = "https://open.er-api.com/v6/latest/USD"
    respons = requests.get(url)
    return respons.json()["rates"]

try:
    data_kurs = ambil_data_kurs()
    daftar_mata_uang = list(data_kurs.keys())

    # 3. Desain Tampilan Aplikasi (UI)
    col1, col2 = st.columns(2)
    
    with col1:
        mata_uang_asal = st.selectbox("Dari Mata Uang:", daftar_mata_uang, index=daftar_mata_uang.index("USD"))
    with col2:
        default_tujuan = daftar_mata_uang.index("IDR") if "IDR" in daftar_mata_uang else 0
        mata_uang_tujuan = st.selectbox("Ke Mata Uang:", daftar_mata_uang, index=default_tujuan)

    nominal = st.number_input("Masukkan Jumlah Uang:", min_value=0.0, value=1.0, step=1.0)

    # 4. Logika Perhitungan Kurs
    nominal_dalam_usd = nominal / data_kurs[mata_uang_asal]
    hasil_konversi = nominal_dalam_usd * data_kurs[mata_uang_tujuan]

    # 5. Menampilkan Hasil
    st.markdown("---")
    st.subheader("Hasil Konversi:")
    st.success(f"### {nominal:,.2f} {mata_uang_asal} = {hasil_konversi:,.2f} {mata_uang_tujuan}")
    
    st.caption("ℹ️ Data kurs diperbarui secara otomatis secara real-time dari pasar global.")

except Exception as e:
    st.error("Gagal memuat data kurs. Pastikan laptop Anda terhubung ke internet.")
