def get_data():
    import requests
    import re
    from bs4 import BeautifulSoup
    import datetime

    r = BeautifulSoup(requests.get('http://status.pr/Home').text,'html.parser')

    ret = {}

    def is_data_card(tag):
        if tag.has_attr('class'):
            return tag['class']==['card-block']
        else:
            return False

    def is_data_point(tag):
        if tag.has_attr('class'):
            return tag['class'] in (['text-muted'],['text-muted', 'capitalize'],['text-muted','info','font-medium-2'],['text-muted','pb-0'],["font-large-2","text-bold-300","info"])
        else:
            return False

    def str_to_float(data_str):
        if data_str != "":

            data_int = float(data_str.replace(',','').replace('%','').strip())
            if '%' in data_str:
                data_int = data_int*100
            return data_int
        else:
            return None

    def str_to_date(date_str):
        m_dict = {'jan':1,'feb':2,'mar':3,'apr':4,'may':5,'jun':6,'jul':7,'aug':8,'sep':9,'oct':10,'nov':11,'dec':12}
        d = int(date_str[:2])
        m = date_str[date_str.find('/')+1:date_str.find('/',3)]
        y = int(date_str[-4:])

        return datetime.date(y,m_dict[m],d)

    card_names = ['gas','supermarket','AEE','telecommunication','antenna','tower','shelter','refugee', 'pet','hospital','dialysis','pharmacy','port',
                    'container','bank','cooperatives','ATMs','barrel','bread','ama','federal_mail']

    for j,card in enumerate(list(r.find_all(is_data_card))[1:-1]):
        name = ""
        curr = ""
        total = ""
        big_val = ""
        last_update = ""
        source = ""
        note = ""
        weird_oil_card = False

        for i,data_point in enumerate(list(card.find_all(is_data_point))):
            line = data_point.text
            if 'Barriles' in line: weird_oil_card=True

            if not weird_oil_card:
                if i == 0:
                    big_val = line
                elif i == 1 and data_point['class'] != ["font-large-2","text-bold-300","info"]:
                    if line.find('de') != -1 and 'Diálisis' not in line and 'Servicio de Telecomunicaciones' not in line:
                        # Handle gasoline/supermarkets/containers/bank branches/postal offices
                        name = line[:re.search('( [1-9])',line).start()-1].strip()
                        curr = line[re.search('( [1-9])',line).start()+1:line.find('de ')-1].strip()
                        total = line[line.find('de ')+3:].strip()
                    else:
                        # Handle the rest
                        name = line[:line.find('  ')].strip()
                elif i == 2:
                    # g.write(line+"\n\n\n")
                    last_update = line[re.search('( [0-9])',line).start()+1:].strip()
                elif i == 3:
                    source = line[len('Fuente: '):].strip()
                elif i == 4:
                    note = line[len('Nota: '):].strip()
            else:
                name = "Abastos en Barriles"
                if i == 1:
                    big_val = {}
                    big_val['Diesel'] = line[len('Diesel '):].strip()
                elif i == 2:
                    big_val['Gasoline'] = line[len('Gasolina '):].strip()
                elif i == 3:
                    last_update = line[re.search('( [0-9])',line).start()+1:].strip()
                elif i == 4:
                    source = line[len('Fuente: '):].strip()
                elif i == 5:
                    note = line[len('Nota: '):].strip()

        if card_names[j]!='barrel':
            big_val = str_to_float(big_val)
            curr = str_to_float(curr)
            total = str_to_float(total)
            last_update = str_to_date(last_update)
            ret[card_names[j]]={'Reported Value':big_val,'Current':curr,'Total':total,'Last Update':last_update,'Source':source,'Note':note}
        else:
            last_update = str_to_date(last_update)
            ret[card_names[j]+'_diesel']={'Reported Value':str_to_float(big_val['Diesel']),'Current':curr,'Total':total,'Last Update':last_update,'Source':source,'Note':note}
            ret[card_names[j]+'_gasoline']={'Reported Value':str_to_float(big_val['Gasoline']),'Current':curr,'Total':total,'Last Update':last_update,'Source':source,'Note':note}
    return ret

def get_data_as_tsv(out_path,sep='\t'):
    tsv_headers = ['Key','Reported Value','Current','Total','Last Update','Source','Note']

    with open(out_path,'w+') as f:
        for header in tsv_headers:
            f.write(header)
            if header != tsv_headers[-1]:
                f.write(sep)
        f.write('\n')

        data_dict = get_data()
        for key in data_dict.keys():
            f.write(key)
            f.write(sep)

            for header in tsv_headers[1:]:
                f.write(str(data_dict[key][header]))
                if header != tsv_headers[-1]:
                    f.write(sep)
            f.write('\n')
