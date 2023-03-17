from text_generation import InferenceAPIClient
import streamlit as st

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

    if model == "OpenAssistant/oasst-sft-1-pythia-12b":
        iterator = client.generate_stream(
            total_inputs,
            typical_p=typical_p,
            truncate=1000,
            watermark=watermark,
            max_new_tokens=500,
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
st.title("Open-Assistant SFT-1 12B Model")


if 'messages' not in st.session_state:
    st.session_state['messages'] = [{"User": "Hi", "Response": "Hello"}, ]

for index, key in enumerate(st.session_state['messages']):
    col1, col2 = st.columns([3, 1])
    with col1:
        st.success(key["Response"])
    with col2:
        st.info(key["User"])

hist = []
form = st.form(key='my_form')
search = form.text_area(label='User : ', height=100)
submit_button = form.form_submit_button(label='Enter')
if submit_button:
    *_, last = predict("OpenAssistant/oasst-sft-1-pythia-12b", search, 0.2, 0.25, 0.6, 50,1.01, False, hist)  # check PEP 448
    st.warning(last[1])
    st.session_state['messages'].append({"User": last[0], "Response": last[1]})
    # text = client.generate(f"<|prompter|>{search}<|endoftext|><|assistant|>").generated_text
    # st.info(f"{text}")



