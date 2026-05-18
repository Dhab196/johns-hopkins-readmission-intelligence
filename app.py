# عرض معلومات أساسية بطريقة منسقة ومضمونة العرض
st.markdown("### 📊 Key Metrics")
st.markdown("---")

row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.markdown("**🏥 Hospital**")
    st.write(data["hospital_name"])
    st.markdown("**📍 Location**")
    st.write(f'{data["city"]}, {data["state"]}')

with row1_col2:
    st.markdown("**🆔 CCN**")
    st.write(data["ccn"])
    st.markdown("**📅 Latest update used**")
    st.write(latest_update)

st.markdown("---")

row2_col1, row2_col2, row2_col3 = st.columns(3)

with row2_col1:
    st.markdown("**📈 Readmission mix**")
    st.write(readmission_mix)

with row2_col2:
    st.markdown("**🛡️ Leapfrog grade**")
    st.write(safety_grade)

with row2_col3:
    st.markdown("**🛏️ Beds (historical context)**")
    st.write(beds)

st.markdown("---")
