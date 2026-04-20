import streamlit as st
import pandas as pd

if "user_input" not in st.session_state:
    st.session_state["user_input"] = ""
    
# --- Try Asking Panel ---
SUGGESTIONS = [
    "Toplam satış nedir?",
    "En yüksek satış nedir?",
    "En düşük satış nedir?",
    "Ortalama satış nedir?",
    "En çok satış yapan şehir hangisi?",
    "Aylara göre satış nasıl?",
    "En iyi satış elemanı kim?"
]

def show_try_asking_panel():
    st.markdown("### 💡 Try asking")
    st.caption("Bir soruya tıkla, otomatik yazsın:")

    cols = st.columns(2)

    for i, suggestion in enumerate(SUGGESTIONS):
        col = cols[i % 2]
        if col.button(suggestion, key=f"suggestion_{i}"):
            st.session_state["user_input"] = suggestion
            st.session_state["auto_ask"] = True 
            st.rerun()
            
if "user_input" not in st.session_state:
    st.session_state["user_input"] = ""
    
st.title("Sales Data Assistant")
st.write("CSV verisini analiz eden basit soru-cevap uygulaması")

uploaded_file = st.file_uploader("CSV dosyası yükle", type=["csv"])

def answer_question(df, question):
    question = question.lower()
    df.columns = df.columns.str.strip().str.lower()

    SUGGESTIONS = [
    "Toplam satış nedir?",
    "En yüksek satış nedir?",
    "En düşük satış nedir?",
    "Ortalama satış nedir?",
    "En çok satış yapan şehir hangisi?",
    "Aylara göre satış nasıl?",
    "En iyi satış elemanı kim?"
]
def show_try_asking_panel():
    st.markdown("### 💡 Try asking")
    st.caption("Bir soruya tıkla, otomatik yazsın:")

    cols = st.columns(2)

    for i, suggestion in enumerate(SUGGESTIONS):
        col = cols[i % 2]
        if col.button(suggestion, key=f"suggestion_{i}"):
            st.session_state["user_input"] = suggestion
            st.session_state["auto_ask"] = True   
            st.rerun()

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


    elif "şehir" in question or "sehir" in question:
        return df.groupby("sehir")["toplam_satis"].sum()

    elif "satış elemanı" in question or "satis elemani" in question:
        return df.groupby("Satis_elemani")["toplam_satis"].sum()

    else:
        return "Bu soruyu henüz anlayamıyorum."

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("Veri yüklendi")
    st.write("İlk 5 satır:")
    st.dataframe(df.head())
    show_try_asking_panel()

    question = st.text_input(
    "Sorunu yaz",
    value=st.session_state.get("user_input", ""),
    key="user_input_field"
)

if st.button("Cevapla"):
    if question.strip():
        result = answer_question(df, question)
        st.markdown("---")
        st.markdown("### 📊 Sonuç")
        if "ay" in question and isinstance(result, (pd.Series, pd.DataFrame)):
            st.markdown("### 📊 Grafik")   
            st.markdown("### 📈 Satış Trendi")
            st.line_chart(result)
        if isinstance(result, pd.Series):
            st.markdown("### 📈 Satış Trendi")
            st.line_chart(result)
            st.dataframe(result)

        elif isinstance(result, pd.DataFrame):
            st.bar_chart(result)
            st.dataframe(result)

    else:
         st.success(result)
else:
    st.warning("Lütfen bir soru yaz.")

#  Auto ask (butonsuz cevap)

if st.session_state.get("auto_ask"):
    result = answer_question(df, st.session_state["user_input"])
    st.markdown("---")
    st.markdown("### 📊 Sonuç")
   
    if isinstance(result, pd.Series):
        st.markdown("### 📊 Grafik")
        st.line_chart(result)
        st.dataframe(result)
    elif isinstance(result, pd.DataFrame):
         st.bar_chart(result)
         st.dataframe(result)
    else:
         st.success(result)

    st.session_state["auto_ask"] = False
