#get stockdata from eastmoney web

import requests
import json


def getjson_stockdata(codenumber):
    url ='http://21.push2his.eastmoney.com/api/qt/stock/kline/get?'
    headers = {
            'Cookie': 'qgqp_b_id=b87cee305c38b309d852cce9e3b9fb61; em_hq_fls=js; ct=weXh0EQEmoADGO5LvfNOBZ00awO1CghuGXp-jR4XkXyXyQiyq1UIBQGMwjHdwtQN0AxwgO3fMWl9uzOeSp1sA52HHwpu8MNWr3ICGvzljGkN9qBV9nuk_H1-S3SGS528HyXckjxHXxkfqofmcIJgcDWWh-wcXz34JiIVVwxjgQY; ut=FobyicMgeV6oOlrtxUaVoieuvidY5esdMCb41if8eqJiqFkwjYg2XAbdyOr2X4dfFAuLZp6zEVvi6dzeDfXQ-AmvlHTZlZ3bcLhnG2QmQB3OEIitjRXjxmZdVjfgoTl0R9Og4o-lLlFot79Tn7wCWlEmBE-Xgvm3SmKy2u_2-TT13T3Di_nblC7WJodHxryF1X8Pl-UvxHe5Ba7LrbinuGObOU_DTORRbA7CCJ680VXlO_XrihmSuhjM8Lv31Xbr4c5cw7OSmrJV114RfOXqtdOJA8M5cx0c; st_si=99026570019922; HAList=ty-1-600166-%u798F%u7530%u6C7D%u8F66%2Cty-1-600660-%u798F%u8000%u73BB%u7483%2Cty-0-300229-%u62D3%u5C14%u601D%2Cf-0-000001-%u4E0A%u8BC1%u6307%u6570; emshistory=%5B%22600166%22%5D; st_pvi=95106582090246; st_sp=2021-08-10%2015%3A37%3A11; st_inirUrl=https%3A%2F%2Fwww.baidu.com%2Flink; st_sn=10; st_psi=2023042709494629-113200301201-9045204979; st_asi=delete',
            'Referer': 'http://quote.eastmoney.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            }
    if codenumber[0]=='6':
        code = '1.'+codenumber
    else:
        code = '0.'+codenumber
    params ={
            'cb':'jQuery3510406753977783055331682559914408',
            'secid':code,
            'ut':'fa5fd1943c7b386f172d6893dbfba10b',
            'fields1':'f1,f2,f3,f4,f5,f6',
            'fields2':'f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61',
            'klt':'101',
            'fqt':'1',
            'beg':'0',
            'end':'20500101',
            'smplmt':'999999', #采样，决定返回的数据长度，默认值为460，可能导致数据不足，可调整为较大的值。
            'lmt':'1000000',
            '_':'1682559914436',
            }
    response = requests.get(url=url, headers=headers, params=params)
    data = response.text
    data = data[41:-2]  #将返回字符串转换为json格式
    return data


# if __name__ == '__main__':
#     # totolPage = pageNumber()
#     # for page in range(totolPage):
#     #     list_pages = getjson_stocklist(page+1)
#     #     for lists_page in list_pages:
#     #         SECURITY_CODE = lists_page['SECURITY_CODE']
#     #         SECURITY_NAME_ABBR = lists_page['SECURITY_NAME_ABBR']