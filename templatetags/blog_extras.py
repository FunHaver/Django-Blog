from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(needs_autoescape=True)
def sift_html(text, autoescape=True):
    """
    Unescapes designated html tags after django's escaping has passed over
    the text.
    """
    permitted_tags = ('i', 'b', 'a', 'br')

    #Tests for autoescape and assigns either conditional_escape function or
    #do nothing function depending on whether autoescape has been performed by
    #Django or not

    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x
    
    
    def escaped_char_decode(escaped_text_str):
        if escaped_text_str == "&lt;":
            return "<"
        elif escaped_text_str == "&gt;":
            return ">"
        elif escaped_text_str == "&quot;":
            return '"'
        else:
            return "Error: Could not escape " + escaped_text_str

    def html_tag_permitted(tag_str):
        full_tag_name = ""
        x = 0
        
        #  Allows for the name char accumulation to occur if closing tag is being read
        if tag_str[0] == "/":
            x += 1
        while x < len(tag_str):
            if tag_str[x] == " " or tag_str[x:x+4] == "&lt;" or tag_str[x:x+4] == "&gt;":
                if full_tag_name in permitted_tags:
                    return True
                else:
                    return False
            else:
                full_tag_name += tag_str[x]
                x+=1

    def detect_escaped_html_character_length(escaped_char_str):
        
        if escaped_char_str[0] == "&":
             
            if escaped_char_str[3] == ";":
                return 4
            elif escaped_char_str[5] == ";":
                return 6
            else:
                return 0
        else:
            return 0

    def selective_unescape(escaped_text):
        finished_text = ""
        x = 0 
        unescape_permitted = False 
        while x < len(escaped_text):
            unescaped_char = ""

            escaped_html_character_length = detect_escaped_html_character_length(escaped_text[x:x+6])
            if escaped_html_character_length != 0:
                #Detect which HTML encoded escaped character
                unescaped_char = escaped_char_decode(escaped_text[x:x+escaped_html_character_length])
                
                #Searches forward in string for type of HTML tag
                #Returns true if tag exists in permitted_tags
                #Returns false if tag does not exist in permitted_tags OR
                #if it is a permitted but malformed tag

                if unescaped_char == "<":
                    unescape_permitted = html_tag_permitted(escaped_text[x+4:])

                    if unescape_permitted:
                        x += 4
                        finished_text = finished_text + unescaped_char
                    else:
                        finished_text = finished_text + escaped_text[x]
                        x += 1
                elif unescaped_char == '"' and unescape_permitted:
                    x += 6
                    finished_text = finished_text + unescaped_char

                elif unescaped_char == ">" and unescape_permitted:
                    x += 4
                    finished_text = finished_text + unescaped_char
                    unescape_permitted = False
                else:
                    finished_text = finished_text + escaped_text[x]
                    x += 1

            else:
                finished_text = finished_text + escaped_text[x]
                x += 1
        
        return finished_text

    return mark_safe(selective_unescape(esc(text)))

@register.filter(needs_autoescape=True)
def carriage_return_to_break_tag(text, autoescape=True):
    if autoescape:
        esc = conditional_escape # pylint: disable=unused-variable
    else:
        esc = lambda x: x

    processed_text = ""
    x = 0
    while x < len(text):
        if text[x] == chr(10) or text[x] == chr(13):
            processed_text += "<br>"
            x += 2
        else:
            processed_text += text[x]
            x += 1
        
    
    return processed_text