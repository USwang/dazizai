import requests
import json
import csv
from datetime import datetime
from exts import db
from models import Stockdata, Stocklist

#网址
def getjson_stockincome(codenumber):
        url ='https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/lrbAjaxNew?'
        headers = {
                'Cookie': 'qgqp_b_id=b87cee305c38b309d852cce9e3b9fb61; em_hq_fls=js; ct=weXh0EQEmoADGO5LvfNOBZ00awO1CghuGXp-jR4XkXyXyQiyq1UIBQGMwjHdwtQN0AxwgO3fMWl9uzOeSp1sA52HHwpu8MNWr3ICGvzljGkN9qBV9nuk_H1-S3SGS528HyXckjxHXxkfqofmcIJgcDWWh-wcXz34JiIVVwxjgQY; ut=FobyicMgeV6oOlrtxUaVoieuvidY5esdMCb41if8eqJiqFkwjYg2XAbdyOr2X4dfFAuLZp6zEVvi6dzeDfXQ-AmvlHTZlZ3bcLhnG2QmQB3OEIitjRXjxmZdVjfgoTl0R9Og4o-lLlFot79Tn7wCWlEmBE-Xgvm3SmKy2u_2-TT13T3Di_nblC7WJodHxryF1X8Pl-UvxHe5Ba7LrbinuGObOU_DTORRbA7CCJ680VXlO_XrihmSuhjM8Lv31Xbr4c5cw7OSmrJV114RfOXqtdOJA8M5cx0c; emshistory=%5B%22600168%22%2C%22600166%22%5D; st_si=96747731529293; st_asi=delete; HAList=ty-1-688678-%u798F%u7ACB%u65FA%2Cty-1-000001-%u4E0A%u8BC1%u6307%u6570%2Cty-0-300059-%u4E1C%u65B9%u8D22%u5BCC%2Cty-1-600166-%u798F%u7530%u6C7D%u8F66%2Cty-1-600168-%u6B66%u6C49%u63A7%u80A1%2Cty-1-600660-%u798F%u8000%u73BB%u7483%2Cty-0-300229-%u62D3%u5C14%u601D%2Cf-0-000001-%u4E0A%u8BC1%u6307%u6570; st_pvi=95106582090246; st_sp=2021-08-10%2015%3A37%3A11; st_inirUrl=https%3A%2F%2Fwww.baidu.com%2Flink; st_sn=29; st_psi=20230505193615554-111000300841-6619305167; JSESSIONID=BE177C063CC1A664DE227D3C0F355DCD',
                'Referer': 'https://data.eastmoney.com/',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
                }

        if codenumber[0] == '8':  # 剔除新三板
                pass
        elif codenumber[0] == '6':  # 主板
                code = 'SH' + codenumber
        else:
                code = 'SZ' + codenumber
        time_string = ['-03-31', '-06-30', '-09-30', '-12-31']  #特定格式
        now = datetime.now()
        current_year = now.year  # 获取当前年份
        imcomelist = []
        # #从1990年开始，不足的数据将为空，需要跳过。
        for year in range(1990, current_year+1, 1):
                for m in range(4):
                        dataes = str(year) + time_string[m]
                        # print(dataes)
                        # dataes='2023-3-31'
                        params = {
                                'companyType': '4',
                                'reportDateType': '0',
                                'reportType': '1',
                                'dates': dataes,
                                'code': code,  # 第几页
                        }
                        response = requests.get(url=url, headers=headers, params=params)
                        # print(response.status_code)
                        # print(response.url)
                        # print(response.text)
                        result_json = response.text
                        # print(result_json)
                        result_dict = json.loads(result_json)
                        # print(result_dict['data'])
                        # print(type(result_dict))
                        # 判断KEY 是否存在
                        if 'data' in result_dict:
                                data = result_dict['data'][0]
                        imcomelist.append(data)
        # imcomejson = json.dumps(imcomelist) #列表转json
        return imcomelist
# lies = db.session.query(Stocklist).all()
# for li in lies:
#     code= li.SECURITY_CODE
#     if code[0] == '8':    #剔除新三板
#         continue
#     elif code[0] == '6':  #主板
#         code = 'SH'+code
#     else:
#         code = 'SZ'+code
#     print(code)