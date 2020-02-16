# -*- coding:utf-8 -*-
import json, sys
from datetime import datetime
from workflow import Workflow3, web

reload(sys)
sys.setdefaultencoding('utf-8')

ICON = 'icon.png'
ICON_ERROR = 'icon_error.png'

ERRORCODE_DICT = {
    "400": "Query not translatable",
    "500": "SpanishDict fails to translate"
}

def translate_uri(query, lang):
    return "http://translate1.spanishdict.com/dictionary/translation_prompt" + \
        "?lang_from=" + lang + \
        "&trtext=" + query

def get_translation(url):
    try:
        rs = web.get(url=url).json()
        if 'error' in rs:
            rs['errorCode'] = "400"
        return rs
    except:
        rs = {}
        rs['errorCode'] = "500"
        return rs

def main(wf):
    query = wf.args[0].strip()
    url = translate_uri(query, 'es')
    result = get_translation(url)
    errorCode = str(result.get("errorCode"))
    if errorCode == "500" or errorCode == "400":
        wf.add_item(title=ERRORCODE_DICT[errorCode], icon=ICON_ERROR)
    else:
        translation = result["results"]
        wf.add_item(title=translation, icon=ICON)

    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow3()
    sys.exit(wf.run(main))