import streamlit as st
import requests
import pandas as pd  # Ditambahkan untuk menyusun tabel riwayat agar rapi
from datetime import datetime  # Ditambahkan untuk mencatat waktu konversi

# ==========================================
# 1. KONFIGURASI HALAMAN & IDENTITAS (Sesuai Aplikasi Anda)
# ==========================================
st.set_page_config(page_title="Kalkulator Kurs Real-Time", layout="wide")

# Identitas Anda di Sidebar
st.sidebar.title("Identitas Mahasiswa")
st.sidebar.write("### Nabila Shandy Nathasa")
st.sidebar.write("NIM: 2313000005")
st.sidebar.write("Prodi: S1 Sistem Informasi")
st.sidebar.write("Perbanas Institute")

# ==========================================
# 2. INISIALISASI DATABASE MEMORI (FITUR BARU)
# ==========================================
# Membuat wadah penyimpanan kosong di memori browser saat web pertama kali dibuka
if 'riwayat_konversi' not in st.session_state:
    st.session_state['riwayat_konversi'] = []

# ==========================================
# 3. FUNGSI FETCH DATA API WITH CACHING
# ==========================================
@st.cache_data(ttl=3600)
def get_exchange_rates():
    url = "https://open.er-api.com/v6/latest/USD"  # Contoh API URL yang Anda gunakan
    try:
        response = requests.get(url)
        return response.json()
    except:
        return None

data_api = get_exchange_rates()

# ==========================================
# 4. HALAMAN UTAMA & INPUT USER
# ==========================================
st.title("💰 Kalkulator Konversi Mata Uang Global Real-Time")
st.write("Aplikasi SaaS berbasis Cloud untuk menghitung nilai kurs mata uang secara akurat.")

if data_api and data_api.get("result") == "success":
    rates = data_api.get("rates")
    list_mata_uang = list(rates.keys())
    
    # Grid Layout untuk Input
    col1, col2, col3 = st.columns(3)
    with col1:
        nominal = st.number_input("Masukkan Nominal Uang:", min_value=0.0, value=1.0, step=0.5)
    with col2:
        dari_curr = st.selectbox("Dari Mata Uang:", list_mata_uang, index=list_mata_uang.index("USD") if "USD" in list_mata_uang else 0)
    with col3:
        ke_curr = st.selectbox("Ke Mata Uang:", list_mata_uang, index=list_mata_uang.index("IDR") if "IDR" in list_mata_uang else 0)
        
    # ==========================================
    # 5. LOGIKA PERHITUNGAN & AUTO-SAVE (FITUR BARU)
    # ==========================================
    # Rumus konversi matematika
    nominal_dalam_usd = nominal / rates[dari_curr]
    hasil_konversi = nominal_dalam_usd * rates[ke_curr]
    
    # Tampilkan Hasil Utama ke Layar
    st.success(f"### Hasil: {nominal:,.2f} {dari_curr} = {hasil_konversi:,.2f} {ke_curr}")
    
    # LOGIKA MENYIMPAN KE RIWAYAT SECARA OTOMATIS
    waktu_sekarang = datetime.now().strftime("%H:%M:%S")
    
    data_log_baru = {
        "Waktu": waktu_sekarang,
        "Nominal Asal": f"{nominal:,.2f} {dari_curr}",
        "Hasil Konversi": f"{hasil_konversi:,.2f} {ke_curr}"
    }
    
    # Validasi agar tidak menyimpan data duplikat yang sama persis dalam waktu yang sama
    if not st.session_state['riwayat_konversi'] or st.session_state['riwayat_konversi'][-1]["Waktu"] != waktu_sekarang:
        st.session_state['riwayat_konversi'].append(data_log_baru)

    # ==========================================
    # 6. MENAMPILKAN TABEL RIWAYAT DI BAWAH (FITUR BARU)
    # ==========================================
    st.write("---")
    st.subheader("📜 Riwayat Konversi Pengguna (Auto-Saved)")
    
    if st.session_state['riwayat_konversi']:
        # Mengubah list memori menjadi tabel rapi dengan bantuan library Pandas
        df_tabel = pd.DataFrame(st.session_state['riwayat_konversi'])
        
        # Menampilkan tabel interaktif di web Streamlit
        st.dataframe(df_tabel, use_container_width=True)
        
        # Tombol pelengkap untuk membersihkan riwayat
        if st.button("🔴 Hapus Semua Riwayat"):
            st.session_state['riwayat_konversi'] = []
            st.rerun()
    else:
        st.info("Belum ada riwayat pencarian. Silakan lakukan transaksi di atas.")

else:
    st.error("Gagal memuat data kurs real-time. Periksa koneksi internet server cloud Anda.")
