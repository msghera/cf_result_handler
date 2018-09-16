from urllib.request import Request, urlopen
import pandas as pd
import requests

def exists(url) :
    request = requests.get(url)
    if request.status_code != 200:
        print('Web site does not exist') 
        return False
    return True
    
def fetch_res(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    df = pd.read_html(webpage)[0]
    col_name = list (df.columns)
    new_df = list(df[col_name[1]])
    return new_df[1:]

def main():
    df = pd.read_excel('student_detail.xlsx', encoding='utf-8')
    iiuc_cf_handle = list(df['Codeforces ID'])
    _name = list(df['Name'])
    name = dict()
    result = pd.DataFrame()
    _contest_name = []
    _rank = [[] for _ in range(20)]
    for i in range(len(iiuc_cf_handle)) : name[iiuc_cf_handle[i]] = _name[i]
    contest_file = open('contest.txt', 'r')
    contest_lst = contest_file.read().split('\n')
    for contest_num in contest_lst: 
        prev_lst = []
        standing = []
        for page_num in range(1, 100):
            print('Contest ' +str(contest_num) + ' Page '+ str(page_num))
            url = 'http://codeforces.com/contest/'+str(contest_num)+'/standings/page/'+str(page_num)
            lst = fetch_res(url)
            if lst == prev_lst : break
            for i in lst : 
                if i in iiuc_cf_handle : standing.append(i)
            prev_lst = lst 
        if len(standing) : 
            _contest_name.append('http://codeforces.com/contest/'+str(contest_num)+'/standings'+'\n\n')
            for i in range(20) : 
                if(i < len(standing)) : _rank[i].append(name[standing[i]])
                else : _rank[i].append('')
        # if len(standing) : result += ('http://codeforces.com/contest/'+str(contest_num)+'/standings'+'\n\n')
        # for i in range(len(standing)) : result +=('Rank ' + str(i+1) + ' : ' + str(name[standing[i]]) + '\n')
        # if len(standing) : result+= '\n\n'
        
    result['Contest Link'] = list(_contest_name)
    _rank_lst = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th', '11th', '12th', '13th', '14th', '15th', '16th', '17th', '18th', '19th', '20th']
    for i in range(20) :    result[_rank_lst[i]] = _rank[i]
    result.to_csv('Complete_Result_Codeforces_For_IIUCian.csv', index=False)
if __name__ == '__main__':
    main()
