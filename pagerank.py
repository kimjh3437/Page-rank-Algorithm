import pydot
import sys
from collections import OrderedDict
import pandas as pd
#CODE OF GABE KIM 2282163 gjkim5@emory.edu

def pageRank(inputfile,outputfile):
    graph = pydot.graph_from_dot_file(inputfile) #read .dot file 
    adj_list = dict()    #use dictionary 

    for edge in graph[0].get_edges():   #retrieve all the nodes 
        if edge.get_source() not in adj_list:   # if the edge is not in the dict, then add 
            adj_list[edge.get_source()] = [edge.get_destination()]
        else:
            if edge.get_destination() not in adj_list[edge.get_source()]:
                adj_list[edge.get_source()].append(edge.get_destination())

    for edge in graph[0].get_edges():
        if edge.get_destination() not in adj_list:
            adj_list[edge.get_destination()] = []

    print len(adj_list)
    PR = dict()
    PR_Iteration = 1.0/len(adj_list) #make PR_It float 
    stopIterations = False
    iterations = 0
    # print PR_Iteration
    # print PR_Iteration

    for vertex in adj_list:
        PR[vertex] = [PR_Iteration]
        

    while(True):

        for vertex in adj_list:
            PR_Iteration = 0

            for incoming in adj_list:
                if vertex in adj_list[incoming]:
                    PR_Iteration = PR_Iteration + (PR[incoming][iterations]/len(adj_list[incoming]))  #PR value calculation

            PR[vertex].append(PR_Iteration)

            if PR[vertex][-1] - PR[vertex][-2] == 0:  #check if the current iteration is good to go

                stopIterations = True

        iterations += 1
        if stopIterations == True:
            break


    for vertex in PR:
        PR[vertex] = [PR[vertex][-1]]


    PR = pd.DataFrame(PR)  #using pandas put on dataframe

    PR = PR.transpose().sort_values(0,ascending = 0)  #sort the vertices based on their pr values 
    ranks = list()
    ranks.extend(range(len(PR),0,-1))   #add rankings 
    PR[0]=ranks
    #PR[0] = [*range(len(PR),0,-1)]
    PR = PR.reset_index()
    PR.rename(columns={'index':'Vertices',0:'PageRank'},inplace=True)
    print(PR)

    PR.to_csv(outputfile,index=False)

if __name__ == "__main__":
    
    pageRank(sys.argv[1],sys.argv[2])