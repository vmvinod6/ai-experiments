import pandas as pd
import json
class FewshotPosts:
    def __init__(self, file_path="data/processed_posts.json"):
        self.df = None
        self.unified_tags = None
        self.languages = None
        self.lengths = None
        self.load_data(file_path)

    def load_data(self,file_path="data/processed_posts.json"):
        """
        Load the processed posts data from a JSON file.
        """
        post= json.load(open(file_path, 'r', encoding='utf-8'))
        self.df = pd.json_normalize(post)
        self.df['length'] = self.df['line_count'].apply(self.categorize_length)
        all_tags = self.df['tags'].apply(lambda x: x).sum()
        all_tags = set(list(all_tags))  
        self.languages = self.df['language'].unique().tolist()
        self.lengths = self.df['length'].unique().tolist()
        self.unified_tags = {tag: tag for tag in all_tags}

    def categorize_length(self,line_count):
        if line_count < 5:
            return "Short"
        elif 5 <= line_count < 10:
            return "Medium"
        else:
            return "Long"   

    def get_tags(self):
        """        Get unified tags.
        """
        if self.unified_tags is not None:
            return self.unified_tags
        return []
    
    def get_languages(self):
        """        Get unique languages from the posts.
        """
        if self.languages is not None:
            return self.languages
        return []

    def get_lengths(self):
        """        Get unique lengths from the posts.
        """
        if self.lengths is not None:
            return self.lengths
        return []

    def get_filtered_posts(self, length=None, language=None,tag=None):
        """        Filter posts based on length, language, and tags.
        """
        filtered_df = self.df[
            (self.df['length'] == length) &
            (self.df['language'] == language) &
            (self.df['tags'].apply(lambda tags: tag in tags))
        ]
        return filtered_df.to_dict(orient='records')
        


if __name__ == "__main__":
    fewshot_posts = FewshotPosts()
    fewshot_posts.load_data()
    lang = fewshot_posts.get_languages()
    print(f"Available Languages: {lang}")
    #filtered_posts = fewshot_posts.get_filtered_posts(length="Short", language="Hinglish", tag="Job Search")
    #print(f"Filtered Posts: {filtered_posts}")