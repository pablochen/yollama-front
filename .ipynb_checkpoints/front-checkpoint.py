import streamlit as st
import requests
import time

url = "http://localhost:8000/run_model"

response_box_html = '''
<div id="response-box" style="
    background-color: #f3f5f8; 
    height: 500px; 
    margin: 5px; 
    padding: 10px;
    border: 1px solid orange;
    border-radius: 10px;
    overflow-y: auto;
">
    <p id="response-text" style="
        font-family: 'Noto Sans KR', sans-serif; 
        font-size: 16px; 
        margin: 0;
        padding: 0;
        white-space: pre-wrap;
    ">{}</p>
</div>
'''

def main():
    st.set_page_config(layout="wide")

    leftbar, rightbar = st.columns([2, 3])
    
    with rightbar:
        st.subheader("Answer")
        placeholder = st.empty()
        placeholder.markdown(response_box_html.format(''), unsafe_allow_html=True)
    
    with leftbar:
        st.subheader("Yollama")
        col1, col2, col3 = st.columns([2, 2, 1])

        with col1:
            token_options = ['128', '256', '512', '1024']
            token_len = st.selectbox("토큰 수:", token_options)
        
        with col2:
            thread_options = ['1', '2', '4', '8', '16', '32', '64', '128', '256', '512', '1024']
            thread_len = st.selectbox("쓰레드 수:", thread_options,
                                      index=thread_options.index('32'))

        with col3:
            search_len = st.number_input("검색결과 수:", min_value=1, max_value=20, 
                                         value=5, step=1)

        input_text = st.text_area("질문", "", height=315)

        st.markdown("""<style>div.stButton > button {width: 100%;}</style>""",
                    unsafe_allow_html=True)

        if st.button("실행"):
            params = {"input_text": input_text,
                     "token_len": token_len,
                     "thread_len": thread_len,
                     "search_len":search_len}

            full_text = ''
            with requests.get(url, params=params, stream=True) as response:
                if response.status_code == 200:
                    for line in response.iter_lines():
                        if line:
                            decoded_line = line.decode('utf-8')
                            full_text += decoded_line
                            full_text = full_text.replace('\n','<br>')
                            updated_html = response_box_html.format(full_text)
                            placeholder.markdown(updated_html, unsafe_allow_html=True)
                            time.sleep(0.1)
                            
                else:
                    st.error(f"Error: {response.status_code}")
                

if __name__ == "__main__":
    main()
