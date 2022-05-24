import gspread
import networkx as nx
import Rainbow_matching as rm

'''
This project uses "networkx" so run in terminal 
pip install networkx
'''

account = gspread.service_account("credentials.json")

spreadsheet = account.open("EX8")
sheet1 = spreadsheet.get_worksheet(0)

number_of_nodes = int(sheet1.cell(1,2).value)

G = nx.path_graph(number_of_nodes)
for i in range(number_of_nodes-1):
    G.edges[i, i+1]['color'] = sheet1.cell(i+1,2).value

k = int(sheet1.cell(9,2).value)

print(rm.rainbow_matching(G, k))