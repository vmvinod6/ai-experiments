
import os 
from llm_helper import llm  # Assuming llm_helper.py is in the same directory
from few_shot_posts import FewshotPosts


def __get_length_category(line_count):
    if line_count < 5:
        return "Short"
    elif 5 <= line_count < 10:
        return "Medium"
    else:
        return "Long"


def __get_new_post_examples(length, language, tag):
    """
    Retrieve a few-shot examples of posts from the processed posts data.
    """
    post_examples = ""
    fs = FewshotPosts()
    examples = fs.get_filtered_posts(length=length, language=language, tag=tag)
    if len(examples) == 0:
        post_examples = "No examples found for the given criteria."
        return post_examples
    post_count = 0
    for example in examples[:2]:  # Get up to 2 examples
        post_count =post_count+1
        #post_examples += f"Post: {example['text']}\nLength: {example['line_count']} lines\nLanguage: {example['language']}\nTags: {', '.join(example['tags'])}\n\n"
        post_examples += f"\n\n {post_count} : {example['text']}\n\n"
    return post_examples

def get_template(length, language, tag):
    # length_str = __get_length_category(length)
    few_shot_posts = __get_new_post_examples(length, language, tag)
    template = f'''
    You are a LinkedIn post generator. You need to generate a LinkedIn post based on the following criteria:
    1. Length: {length} (Short: less than 5 lines, Medium: 5-10 lines, Long: more than 10 lines)
    2. Language: {language} (English or Hinglish)
    3. Tag: {tag} (e.g., Motivation, Job Search, Mental Health, Self Improvement, Scams)
    4. Use the wrting style and tone of the examples provided below.
        Examples :{few_shot_posts}
    '''
    return template

def generate_post(length, language, tag):
    print(f"Generating post with Length: {length}, Language: {language}, Tag: {tag}")
    template = get_template(length, language, tag)
    print(f"Using template:\n{template}")
    response =llm.invoke(template)
    return response.content

if __name__ == "__main__":
    length = 2  # Example length
    language = "Hinglish"  # Example language
    tag = "Job Search"  # Example tag
    post = generate_post(length, language, tag)
    print(f"Generated Post:\n{post}")