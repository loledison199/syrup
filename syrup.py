from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError

def findOne(d, fh):                    
    try:
        api = Finding(appid="EdisonLi-syrup-PRD-c8e35c535-b071148d", config_file=None)
        response = api.execute('findItemsAdvanced', {
            'keywords' : d['keywords'],
            'itemFilter' : d['itemFilter'],
            'paginationInput' : {
                'entriesPerPage' : '25',
                'pageNumber' : '1'
                },
            'sortOrder' : 'PricePlusShippingLowest'
            })

        fh.write('<h3> Keywords: ' + d['keywords'] + '</h3>\n')
        fh.write('<table border="1">\n')
        for item in response.reply.searchResult.item:
            fh.write("<tr><th>%s</th><th>%s %s</th><th>%s</th><th><a href=%s>click</a></th>\n" % (
                item.itemId,
                item.sellingStatus.currentPrice.value,
                item.sellingStatus.currentPrice._currencyId,
                item.title,
                item.viewItemURL))
        fh.write('</table>\n')

    except ConnectionError as e:
        print(e)
        print(e.response.dict())

if __name__ == '__main__':

    # gather input search targets from input.txt
    targets = []
    with open('input.txt', 'r') as ip:
        for line in ip:
            line = line.strip()
            # ignore empty lines
            if not line:
                continue
            # ignore lines that starts with '#'
            if line[0] == '#':
                continue

            # use fancy python thingy to strip each item
            parts = [a.strip() for a in line.split(',')]
            if len(parts) < 3:
                continue

            # construct my local search target
            d = {
                'keywords': parts[0],
                'itemFilter': [
                    {'name': 'Condition', 'value': 'Used'},
                    {'name': 'MinPrice', 'value': parts[1]},
                    {'name': 'MaxPrice', 'value': parts[2]},
                ]
            }

            # append to target list
            targets.append(d)

    # execute search and print to html
    with open('syrup.html', 'w') as fh:
        for d in targets:
            findOne(d, fh)
