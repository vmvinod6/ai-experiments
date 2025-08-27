import streamlit as st
from few_shot_posts import FewshotPosts
from post_generation import generate_post   
def main():
    st.title("LinkedIn Post Generator!")
    col1, col2,col3 = st.columns(3)
    fs = FewshotPosts()
    with col1:
        selected_tag= st.selectbox("Title", options = fs.get_tags())
    
    with col2:
        selected_length = st.selectbox("Length", options = fs.get_lengths())
    
    with col3:
        selected_language = st.selectbox("Language", options = fs.get_languages())

    if st.button("Filter Posts"):
        fs.load_data()
        filtered_posts = fs.get_filtered_posts(length=selected_length, language=selected_language, tag=selected_tag)
        st.write(f"Filtered Posts: {filtered_posts}")

    if st.button("Clear Selection"):
        selected_tag = None
        selected_length = None
        selected_language = None
    

    if st.button("Generate New Post"):
        post = generate_post(length=selected_length, language=selected_language, tag=selected_tag)
        st.subheader("Generated Post:")
        st.write(post)
    

if __name__ == "__main__":
    main()