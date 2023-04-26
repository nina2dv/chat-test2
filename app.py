from text_generation import InferenceAPIClient
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

def predict(
    model: str,
    inputs: str,
    typical_p: float,
    top_p: float,
    temperature: float,
    top_k: int,
    repetition_penalty: float,
    watermark: bool,
    history,
):
    client = InferenceAPIClient(model, token=st.secrets["KEY"])
    preprompt, user_name, assistant_name, sep = "", "<|prompter|>", "<|assistant|>", "<|endoftext|>"

    history.append(inputs)

    past = []
    if not inputs.startswith(user_name):
        inputs = user_name + inputs

    total_inputs = preprompt + "".join(past) + inputs + sep + assistant_name.rstrip()

    partial_words = ""

    if model == "OpenAssistant/oasst-sft-1-pythia-12b" or model == "OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5":
        iterator = client.generate_stream(
            total_inputs,
            typical_p=typical_p,
            repetition_penalty=0.8,
            truncate=1000,
            watermark=watermark,
            max_new_tokens=800,
        )
    for i, response in enumerate(iterator):
        if response.token.special:
            continue

        partial_words = partial_words + response.token.text
        if partial_words.endswith(user_name.rstrip()):
            partial_words = partial_words.rstrip(user_name.rstrip())
        if partial_words.endswith(assistant_name.rstrip()):
            partial_words = partial_words.rstrip(assistant_name.rstrip())

        if i == 0:
            history.append(" " + partial_words)
        elif response.token.text not in user_name:
            history[-1] = partial_words

        chat = [
            (history[i].strip(), history[i + 1].strip())
            for i in range(0, len(history) - 1, 2)
        ]
        # yield chat, history
        yield history

# client = InferenceAPIClient("OpenAssistant/oasst-sft-1-pythia-12b")
st.title("Open-Assistant SFT-1 12B Demo")
with st.sidebar:
    genre = st.radio(
    "Select model",
    ('OpenAssistant/oasst-sft-1-pythia-12b', 'OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5'))
    
    st.warning("Refreshing the page cleans the history")
    st.markdown(get_st_button_a_tag('https://open-assistant.io', 'Open Assistant Site'), unsafe_allow_html=True)
    st.markdown(get_st_button_a_tag('https://github.com/nina2dv', 'Donate'), unsafe_allow_html=True)

if 'messages' not in st.session_state:
    st.session_state['messages'] = [{"User": "User", "Response": "Open Assistant"}, ]
    
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

hist = []
form = st.form(key='my_form')
search = form.text_area(label='User : ', height=100, help="Ask anything")
submit_button = form.form_submit_button(label='Enter')
if submit_button:
    *_, last = predict(genre, search, 0.2, 0.25, 0.6, 50,1.01, False, hist)  # check PEP 448
    st.success(last[1])
    st.session_state['messages'].append({"User": last[0], "Response": last[1]})
    # text = client.generate(f"<|prompter|>{search}<|endoftext|><|assistant|>").generated_text
    # st.info(f"{text}")



