import streamlit as st

def get_st_button_a_tag(url_link, button_name):
    """
    generate html a tag
    :param url_link:
    :param button_name:
    :return:
    """
    return f'''
    <a href={url_link}><button style="
    fontWeight: 400;
    padding: 0.25rem 0.75rem;
    borderRadius: 0.25rem;
    margin: 0px;
    lineHeight: 1.6;
    width: auto;
    userSelect: none;
    backgroundColor: #FFFFFF;
    border: 1px solid rgba(49, 51, 63, 0.2);">{button_name}</button></a>
    '''


with st.sidebar:
    st.warning("Refreshing the page cleans the history")
    st.markdown(get_st_button_a_tag('https://open-assistant.io', 'Open Assistant Site'), unsafe_allow_html=True)
    st.markdown(get_st_button_a_tag('https://github.com/nina2dv', 'Donate'), unsafe_allow_html=True)

for index, key in enumerate(st.session_state['messages']):
    col1, col2 = st.columns([3, 1])
    with col1:
        st.success(key["Response"])
    with col2:
        st.info(key["User"])

hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
