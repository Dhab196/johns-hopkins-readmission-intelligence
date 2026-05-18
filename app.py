# عرض معلومات أساسية - تم تعديله لتحسين العرض
st.markdown("### 📊 Key Metrics")

col1, col2 = st.columns(2)
with col1:
    st.metric("🏥 Hospital", data["hospital_name"])
    st.metric("📍 Location", f'{data["city"]}, {data["state"]}')
    st.metric("📈 Readmission mix", readmission_mix)

with col2:
    st.metric("🆔 CCN", data["ccn"])
    st.metric("📅 Latest update", latest_update)
    st.metric("🛡️ Leapfrog grade", safety_grade)

st.metric("🛏️ Beds (historical context)", beds)
