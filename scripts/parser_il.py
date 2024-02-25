import itertools

from article_parser_utils import Author, ArticleText

def parser_author_il(authors):
    return [Author(author['name']) if 'name' in author.keys() else '' for author in authors]
    
def get_text_recursive_il(dict_object):
    # base case
    if 'type' in dict_object.keys() and dict_object['type'] == 'text':
        return dict_object['text'] if 'text' in dict_object.keys() else ''
    if 'type' in dict_object.keys() and dict_object['type'] == 'link':
        return ''.join(get_text_recursive_il(i) for i in dict_object['items']) + f" ( {dict_object['url']} ) " if 'url' in dict_object.keys() else ''
    # No text will be found
    if 'items' in dict_object.keys():
        return ''.join(get_text_recursive_il(i) for i in dict_object['items'])
     
def paragraph_parser_il(json_id, body_lst) -> ArticleText:
    body = []
    for i, item in enumerate(body_lst):
        paragraph = []
        # Unpack sub-headline:
        if item['type'] == 'subheadline' and 'text' in item.keys():
            paragraph.append(item['text'])
        if 'items' in item.keys():
            # Unpack paragraph
            if item['type'] == 'paragraph':
                for item_i in item['items']:
                    paragraph.append(get_text_recursive_il(item_i))
            # Unpack list of texts
            if item['type'] == 'list':
                unpacked_items = list(itertools.chain(*item['items']))
                for item_i in unpacked_items:
                    paragraph.append(get_text_recursive_il(item_i) + '\n\t')    
        
        body.append(''.join(sentence for sentence in paragraph))
    article_text = ArticleText(json_id, '\n '.join(body))
    return article_text

def parser_il(json_obj):
    art_text = []
    art_authors = []
    for (art_id, art_data) in json_obj.items():
        if 'body' in art_data.keys():
            art_text.append(paragraph_parser_il(art_id, art_data['body']))
        if 'authors' in art_data.keys():
            art_authors.append(parser_author_il(art_data['authors']))
    return  art_text, art_authors

def get_level1_types_il():
    types = []
    for item in json_obj.values():
        body = item['body']
        for b in body:
            types.append(b['type'])
    return set(types)