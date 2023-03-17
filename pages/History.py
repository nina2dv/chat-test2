import streamlit as st
for index, key in enumerate(st.session_state['messages']):
    col1, col2 = st.columns([3, 1])
    with col1:
        st.success(key["Response"])
    with col2:
        st.info(key["User"])