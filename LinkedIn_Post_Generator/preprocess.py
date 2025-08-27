import json
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from llm_helper import llm  # Assuming llm_helper.py is in the same directory


def process_post(raw_post,processed_post='data/processed_posts.json'):
    """
    Processes a raw post and appends it to the processed post list.
    """
    # Convert the raw post to lowercase
    all_posts = []
    with open(raw_post, 'r', encoding='utf-8') as file:
        raw_data = json.load(file)

    for post in raw_data:
        metadata = extract_text(post['text'])
        post_with_text = post|metadata
        all_posts.append(post_with_text)
        print(f"Processed post: {post_with_text}")

    unified_tags = get_unified_post(all_posts)
    for post in all_posts:
        currenbt_tag = post.get('tags', [])
        new_tags = {unified_tags[tag] for tag in currenbt_tag}
        post['tags'] = list(new_tags)

    with open(processed_post, 'w', encoding='utf-8') as file:
        json.dump(all_posts, file, ensure_ascii=False, indent=4)
        
        

def get_unified_post(post_with_metadata):
    """
    Returns a unified post with text and metadata.
    """
    unique_tags = set()
    for post in post_with_metadata:
        unique_tags.update(post.get('tags', []))

    unique_tags_list = ','.join(unique_tags)
    template = '''I will give you a list of tags. You need to unify tags with the following requirements,
    1. Tags are unified and merged to create a shorter list. 
       Example 1: "Jobseekers", "Job Hunting","Jobs" can be all merged into a single tag "Job Search". 
       Example 2: "Motivation", "Inspiration", "Drive" can be mapped to "Motivation"
       Example 3: "Personal Growth", "Personal Development", "Self Improvement" can be mapped to "Self Improvement"
       Example 4: "Scam Alert", "Job Scam" etc. can be mapped to "Scams"
    2. Each tag should be follow title case convention. example: "Motivation", "Job Search"
    3. Output should be a JSON object, No preamble
    3. Output should have mapping of original tag and the unified tag. 
       For example: {{"Jobseekers": "Job Search",  "Job Hunting": "Job Search", "Motivation": "Motivation}}
    
    Here is the list of tags: 
    {tags}
    '''
    pt = PromptTemplate.from_template(template=template)
    chain = pt | llm 
    response = chain.invoke({"tags": unique_tags_list}) 
    try:
        output_parser = JsonOutputParser()
        parsed_response = output_parser.parse(response.content)
        return parsed_response  
    except OutputParserException as e:
        print(f"Error parsing response: {e}")
        return {}



def extract_text(post):
    """
    Extracts text from a post.
    """
    template = '''
    You are given a LinkedIn post. You need to extract number of lines, language of the post and tags.
    1. Return a valid JSON. No preamble. 
    2. JSON object should have exactly three keys: line_count, language and tags. 
    3. tags is an array of text tags. Extract maximum two tags.
    4. Language should be English or Hinglish (Hinglish means hindi + english)
    
    Here is the actual post on which you need to perform this task:  
    {post}
    '''
    pt = PromptTemplate(template=template)
    chain = pt | llm 
    response = chain.invoke({"post": post})
    try:
        output_parser = JsonOutputParser()
        parsed_response = output_parser.parse(response.content)
        return parsed_response
    except OutputParserException as e:
        print(f"Error parsing response: {e}")
        return {}   

    
    
    
    # return{
    #     'line_counrt':10,
    #      'language': 'english',
    #      'tag':['Mental halth','Motivation']
    # }

if __name__ == "__main__":
    process_post('data/raw_posts.json', 'data/processed_posts.json')
    print("Processing complete.")