from bottle import route, run, template, request
import grid
import clus
print "loading data"
foo,_=grid.readInput('data.csv')
print "pivoing data"
a=grid.pivotData(foo)
print "complete"
@route('/data/<name>')
def index(name='p173'):
    clusters= a[name.upper()].getLocation()
    count= len(a[name.upper()].coor)
    return {'names':list(a[name.upper()].places), 'data': list(a[name.upper()].coor), 'centers':clusters}

@route('/pack')
def packMap():
    return template('packList',rows=sorted(a.keys()))


@route('/pack/<name>')
def packMap(name='p173'):
    return template('map_circles',pack=name)


run(host='0.0.0.0', port=8080, reloader=True, debug=True)
