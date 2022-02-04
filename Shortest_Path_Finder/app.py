from flask import*
from haversine import haversine
from haversine import haversine_vector, Unit
from geopy.geocoders import Nominatim



app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/output",methods=['GET','POST'])
def hel():
  return "Bhargav"


def anji(l):
    p=[]
    for i in range(len(l)):
        k=tuple(map(float,l[i].split(',')))
        p.append(k)
    a=haversine_vector(p, p, Unit.KILOMETERS, comb=True)
    dist = a
    def path_len(path):
        return sum(dist[i][j] for i, j in zip(path, path[1:]))
    to_visit = set(range(len(dist)))
    state = {(i, frozenset([0, i])): [0, i] for i in range(1, len(dist[0]))}
    for _ in range(len(dist) - 2):
        next_state = {}
        for position, path in state.items():
            current_node, visited = position
            for node in to_visit - visited:
                new_path = path + [node]
                new_pos = (node, frozenset(new_path))
                if new_pos not in next_state or path_len(new_path) < path_len(next_state[new_pos]):
                    next_state[new_pos] = new_path
        state = next_state
    shortest = min((path + [0] for path in state.values()), key=path_len)
    print(shortest)
    print('path: {0}, length: {1}'.format(shortest, path_len(shortest)))
    return shortest,path_len(shortest)


def locations(a):
    geolocator = Nominatim(user_agent="geoapiExercises")
    a=str(a)
    location = geolocator.reverse(a)
    return location


@app.route('/output/',methods=['GET','POST'])
def output():
    if request.method=='POST':
        tb=request.form.get("idi")#title
        tb=str(tb)

        ab=request.form.get('idii')#abstract
        ab1=str(ab)

        int1=request.form.get("id2")#introduction
        int1=str(int1)

        com=request.form.get("id3")#components
        com=str(com)

        aut=request.form.get("id4")#authors
        aut=str(aut)

        n11=locations(tb)
        n22=locations(ab1)
        n33=locations(int1)
        n44=locations(com)
        n55=locations(aut)



        if request.form['button_check']=='check_similarity':
          l=[]

          l.append(tb)
          l.append(ab)
          l.append(int1)
          l.append(com)
          l.append(aut)

          #ll=['16.498659370671454,80.65388506932013', '16.50985343021631,80.61815626605107', '16.50985343021631,80.61815626605107']
          ab=anji(l)
          print(ab)
          return render_template("output.html",l1=tb,l2=ab1,l3=int1,l4=com,l5=aut,r=ab,n1=n11,n2=n22,n3=n33,n4=n44,n5=n55)

        else:
            return "BHARGAV"


if __name__ == '__main__':
  app.run(debug = True)