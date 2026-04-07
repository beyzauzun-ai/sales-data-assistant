import streamlit as st
import pandas as pd

st.title("Sales Data Assistant")
st.write("CSV verisini analiz eden basit soru-cevap uygulaması")

uploaded_file = st.file_uploader("CSV dosyası yükle", type=["csv"])

def answer_question(df, question):
    question = question.lower()
    df.columns = df.columns.str.strip().str.lower()

    if "ortalama" in question and "satış" in question:
        return f"Ortalama satış: {df['toplam_satis'].mean():.2f}"

    elif "en yüksek" in question:
        return f"En yüksek satış: {df['toplam_satis'].max()}"

    elif "en düşük" in question:
        return f"En düşük satış: {df['toplam_satis'].min()}"

    elif "toplam satış" in question:
        return f"Toplam satış: {df['toplam_satis'].sum()}"

    elif "şehir" in question and "en çok" in question:
        return f"En çok satış yapan şehir: {df.groupby('sehir')['toplam_satis'].sum().idxmax()}"

    elif "hangi şehir" in question:
        return df.groupby("sehir")["toplam_satis"].sum()

    elif "en iyi satış elemanı" in question:
        if "satis_elemani" in df.columns:
            return f"En iyi satış elemanı: {df.groupby('satis_elemani')['toplam_satis'].sum().idxmax()}"
        elif "satis_elemani" not in df.columns and "satis_elemanı" in df.columns:
            return f"En iyi satış elemanı: {df.groupby('satis_elemanı')['toplam_satis'].sum().idxmax()}"
        else:
            return "Satış elemanı sütunu bulunamadı."

    elif "ay" in question:
        return df.groupby("ay")["toplam_satis"].sum()

    else:
        return "Bu soruyu henüz anlayamıyorum."

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("Veri yüklendi")
    st.write("İlk 5 satır:")
    st.dataframe(df.head())

    question = st.text_input("Sorunu yaz")

    if st.button("Cevapla"):
        if question.strip():
            result = answer_question(df, question)
            st.subheader("Sonuç")
            st.write(result)
        else:
            st.warning("Lütfen bir soru yaz.")