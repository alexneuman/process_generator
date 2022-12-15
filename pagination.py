

from actions import *
import re

def get_pagination_actions(line) -> list[Action]:
    start_page = '0'
    max_page = ''
    line = re.sub(r'\s\s+', ' ', line).replace(': ', ':').replace(' :', ' 0:')
    if line.endswith(':'):
        line += '0'

    if re.search('PAGES \d+:-?\d+', line):
        start_page, max_page = re.search('PAGES (\d+):-?(\d+)', line).groups()
        if max_page == '0':
            max_page = ''

    return  [
    Capture(field_name='numItems', capturedef=['of (?<numItems>\\d+)', '(?<numItems>\\d+)'], optional=True, ignore_no_capture=True),
    Custom(field_name='itemsPerPage', value='10'),
    Capture(field_name='numPages', optional=True),
    Custom(field_name='pageNumParam', value='page'),
    Capture(field_name='sampleURL', value='%%startingURL%%?p=0', parseType={'sampleURL': 'url'}),
    Custom(field_name='startPageNum', value=str(start_page)),
    Custom(field_name='maxPageNum', value=str(max_page)),
    CreatePagination(field_name='create pagination', code="var url=new URL(`%%sampleURL%%`); var pageNumParam = `%%pageNumParam%%`; if([...url.searchParams].map(e=>e[0]==pageNumParam).filter(e=>e==true).length==0){throw `pageNumParam '${pageNumParam}' is not in url: ${url} query string`} ;var itemsPerPage=Number('%%itemsPerPage%%'); var numItems = Number(`%%numItems%%`)||0; var numPages=Number('%%numPages%%'?`%%numPages%%`:(Math.ceil(numItems/itemsPerPage)))||0; var maxPageNum = `%%maxPageNum%%` ;console.log(numPages, numItems ,itemsPerPage); if(!itemsPerPage && itemsPerPage!=Infinity && numPages==0){throw `itemsPerPage cannot be null when numPages is null.`}; if(itemsPerPage && !numItems && !numPages){throw `itemsPerPage cannot be null when both numPages and numItems are null.`}; for(let i=Number(`%%startPageNum%%`||0); i<=(numPages<=maxPageNum||!maxPageNum?numPages:maxPageNum); i++){ if (!`%%pageNumParam%%`){ throw 'You need to specify an action item for pageNumParam'; } url.searchParams.set('%%pageNumParam%%', `${i}`); WARP_RESULT.push({paginationURL: url.toString().replace('%7C%7C%27%27', '')}); }", block=True)
    ]