from article_parser_utils import Author, ArticleText, safe_get_text_value

def parser_author_yle(authors):
    return [Author(safe_get_text_value (j, 'name')) for j in authors] if len(authors) > 0 else []

def paragraph_parser_yle(json_id, body_lst):
    text = [safe_get_text_value(content_obj, 'text') for content_obj in body_lst[0]['content']]
    article_text = ArticleText(json_id, '\n '.join(text))
    return article_text
def parser_yle(json_obj):
    art_text = []
    art_authors = []
    for (art_id, art_data) in json_obj.items():
        if 'data' in art_data.keys():
            art_text.append(paragraph_parser_yle(art_id, art_data['data']))
            if 'authors' in art_data['data'][0].keys():
                art_authors.append(parser_author_yle(art_data['data'][0]['authors']))
            else:
                art_authors.append([])
    return  art_text, art_authors

