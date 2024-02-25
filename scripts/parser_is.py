import itertools

from article_parser_utils import Author, ArticleText

def parser_author_is(authors):
    # ['assetData']['analyticsMetadata']['author']
    return [Author(n) for n in authors.split(', ')]

def get_text_recursive_is(dict_object):
    # base case
    if 'type' in dict_object.keys() and dict_object['type'] in ['text', 'personLink']:
        return dict_object['content'] if 'content' in dict_object.keys() else ''
    if 'type' in dict_object.keys() and dict_object['type'] in ['externalLink', 'internalLink']:
        return f" {dict_object['content']} ( {dict_object['href']} ) " if 'content' in dict_object.keys() else ''
    if 'type' in dict_object.keys() and dict_object['type'] in ['paragraph']:
        return '\t'.join(get_text_recursive_is(i) for i in dict_object['crumbs'])
    if 'type' in dict_object.keys() and dict_object['type'] in ['list']:
        return '\n'.join(get_text_recursive_is(i) for i in dict_object['listContent'])
def paragraph_parser_is(json_id, body_lst) -> ArticleText:
    body = []
    
    for i, item in enumerate(body_lst):
        paragraph = []
        # Unpack sub-headline:
        if item['type'] == 'heading' and 'content' in item.keys():
            paragraph.append(item['content'])
        if item['type'] == 'citation' and 'text' in item.keys():
            paragraph.append(item['text'])
        if (item['type'] == 'blockquote' or item['type'] == 'factbox') and 'body' in item.keys():
            # Unpack blockquote
            for item_i in item['body']:
                paragraph.append(get_text_recursive_is(item_i))
        if item['type'] == 'paragraph' and 'crumbs' in item.keys():
            # Unpack paragraph
            for item_i in item['crumbs']:
                paragraph.append(get_text_recursive_is(item_i))
        
        body.append(''.join(sentence for sentence in paragraph if sentence is not None))
    article_text = ArticleText(json_id, '\n '.join(body))
    return article_text

def parser_is(json_object):
    art_text = []
    art_authors = []
    for (art_id, art_data) in json_object.items():
        if 'assetData' in art_data.keys():
            # get article text
            if 'splitBody' in art_data['assetData'].keys():
                art_text.append(paragraph_parser_is(art_id, art_data['assetData']['splitBody']))
            # get author(s)
            if 'analyticsMetadata' in art_data['assetData'].keys():
                if 'author' in art_data['assetData']['analyticsMetadata']:
                    art_authors.append(parser_author_is(art_data['assetData']['analyticsMetadata']['author']))
                else:
                    art_authors.append([])
    return  art_text, art_authors