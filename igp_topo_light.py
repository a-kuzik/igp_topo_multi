import textfsm
import yaml
import webbrowser
from pprint import pprint

with open("config.yaml", "r") as file:
    conf = yaml.load(file, Loader=yaml.FullLoader)

host_type = conf["host_type"]
igp = conf["igp"]
lsdb_file = conf["lsdb_file"]

try:
    with open(lsdb_file) as file:
        lsdb = file.read()
except Exception as err:
    print(err)

tmpl1 = "templates/sh_ospf_db_router_det_jun.tmpl"
tmpl3 = "templates/sh_isis_db_det_cisco.tmpl"
tmpl4 = "templates/sh_isis_db_ext_jun.tmpl"
tmpl5 = "templates/disp_isis_lsdb_verbose_huawei.tmpl"
tmpl6 = "templates/sh_rou_ospf_db_type_router_det_nokia.tmpl"
tmpl7 = "templates/sh_rou_isis_db_det_nokia.tmpl"
tmpl8 = "templates/sh_ip_ospf_db_router_cisco.tmpl"

pw_nodes = []
hostnames = []
hosts = []

###Function for parsing raw data
def parse_textfsm(template, raw):
    templ = open(template)
    re_table = textfsm.TextFSM(templ)
    parse_data = re_table.ParseText(raw)
    return parse_data


###Function for creating lists of hosts and pseudonodes for ISIS
def hosts_pwnodes(links):
    for L61 in links:
        if L61[0].split(".")[1] == "00":
            if L61[0] not in hosts:
                hosts.append(L61[0])
        if L61[1].split(".")[1] == "00":
            if L61[1] not in hosts:
                hosts.append(L61[1])
        if L61[0].split(".")[1] != "00":
            if L61[0] not in pw_nodes:
                pw_nodes.append(L61[0])
        if L61[1].split(".")[1] != "00":
            if L61[1] not in pw_nodes:
                pw_nodes.append(L61[1])
    return hosts, pw_nodes


#######################
###Nokia
#######################
if host_type == "nokia":
    ##Creating topology from OSPF LSDB
    if igp == "ospf":
        list4 = []
        list5 = []
        out = parse_textfsm(tmpl6, lsdb)
        for L4 in out:
            if L4[2] == "Router":
                if L4[1] not in hosts:
                    hosts.append(L4[1])
            if "Point To Point" in L4[3]:
                list4.append((L4[1], L4[4]))
            if "Transit" in L4[3]:
                list5.append((L4[1], L4[4]))
                if L4[4] not in pw_nodes:
                    pw_nodes.append(L4[4])
        # Removing doubles from links for P2P and BMA types of connections
        for L5 in list4:
            for L6 in list4:
                if L5[0] == L6[1]:
                    if L5[1] == L6[0]:
                        list4.remove(L6)
        for L7 in list5:
            for L8 in list5:
                if L7[0] == L8[1]:
                    if L7[1] == L8[0]:
                        list5.remove(L8)
        for L9 in list5:
            list4.append(L9)
            links = list4

    ##Creating topology from ISIS LSDB
    if igp == "isis":
        list6 = []
        out1 = parse_textfsm(tmpl7, lsdb)
        for L10 in out1:
            if L10[0] not in hostnames:
                hostnames.append(L10[0])
        # Creating links between hosts and pseudonodes
        # Removing the lines with the same contents
        n = 0
        while True:
            n += 1
            for L11 in out1:
                if L11[0] == L11[4]:
                    out1.remove(L11)
            if n == 2:
                break
        # Removing cross links between nodes and hosts
        for L12 in out1:
            list6.append((L12[0], L12[4]))
        for L13 in list6:
            for L2 in list6:
                if L13[0] == L2[1]:
                    if L13[1] == L2[0]:
                        list6.remove(L2)
        links = list6
        # Creating lists of hosts and pseudo nodes
        hosts, pw_nodes = hosts_pwnodes(list6)

#######################
###Juniper
#######################
if host_type == "juniper":
    ##Creating topology from OSPF LSDB
    if igp == "ospf":
        list14 = []
        list15 = []
        out2 = parse_textfsm(tmpl1, lsdb)
        for L14 in out2:
            if L14[0] == "Router":
                if L14[1] not in hosts:
                    hosts.append(L14[1])
                if L14[2] == "PointToPoint":
                    list14.append((L14[1], L14[3]))
                if L14[2] == "Transit":
                    list15.append((L14[1], L14[3]))
                    if L14[3] not in pw_nodes:
                        pw_nodes.append(L14[3])
        # Removing doubles from links for P2P and BMA types of connections
        for L15 in list14:
            for L16 in list14:
                if L15[0] == L16[1]:
                    if L15[1] == L16[0]:
                        list14.remove(L16)
        for L17 in list15:
            for L18 in list15:
                if L17[0] == L18[1]:
                    if L17[1] == L18[0]:
                        list15.remove(L18)
        for L19 in list15:
            list14.append(L19)
        links = list14
    ##Creating topology from ISIS LSDB
    if igp == "isis":
        out3 = parse_textfsm(tmpl4, lsdb)
        list20 = []
        # Creating list of hostnames
        for L26 in out3:
            if L26[3] not in hostnames:
                hostnames.append(L26[3])
        # Creating links between hosts and pseudonodes
        # Removing the lines with the same contents
        n = 0
        while True:
            n += 1
            for L27 in out3:
                if L27[0] == L27[4]:
                    out3.remove(L27)
            if n == 2:
                break
        # Removing cross links between nodes and hosts
        for L28 in out3:
            list20.append((L28[0], L28[4]))
        for L24 in list20:
            for L25 in list20:
                if L24[0] == L25[1]:
                    if L24[1] == L25[0]:
                        list20.remove(L25)
        links = list20
        # Creating lists of hosts and pseudo nodes
        hosts, pw_nodes = hosts_pwnodes(list20)

#######################
###Cisco
#######################
if host_type == "cisco":
    if igp == "isis":
        list21 = []
        out4 = parse_textfsm(tmpl3, lsdb)
        # Spliting elements in lists and create list of links
        for L41 in out4:
            list21.append((L41[0], L41[4]))
        # Removing lines where element with index 0 is the same as index 1
        n = 0
        while True:
            n += 1
            for L42 in list21:
                if L42[0] == L42[1]:
                    list21.remove(L42)
            if n == 2:
                break
        # Removing double links
        for L44 in list21:
            for L45 in list21:
                if L44[0] == L45[1]:
                    if L44[1] == L45[0]:
                        list21.remove(L45)
        links = list21
        # Creating lists of hosts and pseudo nodes
        hosts, pw_nodes = hosts_pwnodes(list21)

    ##Creating topology from OSPF LSDB
    if igp == "ospf":
        list24 = []
        list25 = []
        out5 = parse_textfsm(tmpl8, lsdb)
        for L46 in out5:
            if L46[1] not in hosts:
                hosts.append(L46[1])
            if "point-to-point" in L46[2]:
                list24.append((L46[1], L46[3]))
            if "Transit" in L46[2]:
                list25.append((L46[1], L46[3]))
                if L46[3] not in pw_nodes:
                    pw_nodes.append(L46[3])
        # Removing doubles from links for P2P and BMA types of connections
        for L47 in list24:
            for L48 in list24:
                if L47[0] == L48[1]:
                    if L47[1] == L48[0]:
                        list24.remove(L48)
        for L49 in list25:
            for L50 in list25:
                if L49[0] == L50[1]:
                    if L49[1] == L50[0]:
                        list25.remove(L50)
        for L51 in list25:
            list24.append(L51)
            links = list24

#######################
###Huawei
#######################
if host_type == "huawei":
    if igp == "isis":
        out6 = parse_textfsm(tmpl5, lsdb)
        list23 = []
        # Creating list of hostnames
        for L52 in out6:
            if L52[1] not in hostnames:
                hostnames.append(L52[1])
        # Creating links between hosts and pseudonodes
        # Removing the lines with the same contents
        n = 0
        while True:
            n += 1
            for L53 in out6:
                if L53[0] == L53[3]:
                    out6.remove(L53)
            if n == 2:
                break
        # Removing cross links between nodes and hosts
        for L54 in out6:
            list23.append((L54[0], L54[3]))
        for L55 in list23:
            for L56 in list23:
                if L55[0] == L56[1]:
                    if L55[1] == L56[0]:
                        list23.remove(L56)
        links = list23
        # Creating lists of hosts and pseudo nodes
        hosts, pw_nodes = hosts_pwnodes(list23)

###Create json file for NeXUI
topologyData = {}
topologyData["nodes"] = []
for L35 in hosts:
    topologyData["nodes"].append({"id": L35, "name": L35, "icon": "router"})

try:
    if len(pw_nodes) != 0:
        for L36 in pw_nodes:
            topologyData["nodes"].append({"id": L36, "icon": "bma"})
except Exception as err:
    print(err)

topologyData.update({"links": []})
ids = 0
for l17 in links:
    topologyData["links"].append(
        {"id": ids, "source": l17[0], "target": l17[1], "color": "blue"}
    )
    ids += 1

text = "var topologyData = {}".format(topologyData)
with open("nextUI/app/topology_data.js", "w") as file:
    file.write(text)
print(
    """File for NeXtUI was created. If the drawing didn't opened in your browser
automatically, you can find file index.html in the directory /nextUI and open it manually"""
)

# Opening topology draw in browser
webbrowser.open_new_tab("nextUI/index.html")
