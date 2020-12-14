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
    permitted_tags = ('i', 'b', 'a')

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
        else:
            return "Error: Could not escape " + escaped_text_str
    def html_tag_detect(escaped_text_str):
        
        if escaped_text_str[0] in permitted_tags and escaped_char_decode(escaped_text_str[1:5]) == ">":
            return True
        elif escaped_text_str[0] == "/":
            if escaped_text_str[1] in permitted_tags and escaped_char_decode(escaped_text_str[2:6]) == ">":
                return True
        else:
            return False

    def selective_unescape(escaped_text):
        finished_text = ""
        x = 0
        unescape_permitted = False 
        while x < len(escaped_text):
            unescaped_char = ""

            
            if escaped_text[x] == "&" and escaped_text[x+3] == ";":
                
                #Detect which HTML encoded escaped character
                unescaped_char = escaped_char_decode(escaped_text[x:x+4])
                
                #Searches forward in string for type of HTML tag
                #Returns true if tag exists in permitted_tags
                #Returns false if tag does not exist in permitted_tags OR
                #if it is a permitted but malformed tag

                if unescaped_char == "<":
                    unescape_permitted = html_tag_detect(escaped_text[x+4:])

                    if unescape_permitted:
                        x += 4
                        finished_text = finished_text + unescaped_char
                    else:
                        finished_text = finished_text + escaped_text[x]
                        x += 1
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
