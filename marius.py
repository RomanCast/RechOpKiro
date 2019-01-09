
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2
from utils import *
from dumb import *

# Distance callback
def create_distance_callback(dist_matrix):
  # Create a callback to calculate distances between cities.

  def distance_callback(from_node, to_node):
    return int(dist_matrix[from_node][to_node])

  return distance_callback

def main(ville):
    dist_matrix = DistMatrix(ville)
    print('dist_matrix = {}'.format(dist_matrix))
    dumb_architecture = dumb_solution_bis(ville)
    # antennas

    # for cluster in dumb_architecture:
    #     distrib = cluster[0][0]
    #     liste_antennes = [distrib]
    #     for chaine in cluster[1:]:
    #         liste_antennes.append(chaine[1])

    # Distance matrix
    for reseau in dumb_architecture:
        dist_matrix, liste_noeuds = sous_DistMatrix(reseau, dist_matrix)
        tsp_size = len(liste_noeuds)
        num_routes = 1
        depot = reseau[0][0]

        # Create routing model
        if tsp_size > 0:
            routing = pywrapcp.RoutingModel(tsp_size, num_routes, depot)
            search_parameters = pywrapcp.RoutingModel.DefaultSearchParameters()
            # Create the distance callback.
            dist_callback = create_distance_callback(dist_matrix)
            routing.SetArcCostEvaluatorOfAllVehicles(dist_callback)
            # Solve the problem.
            assignment = routing.SolveWithParameters(search_parameters)
            if assignment:
                # Solution distance.
                print ('Total cost = {}'.format(assignment.ObjectiveValue()))
                # Display the solution.
                # Only one route here; otherwise iterate from 0 to routing.vehicles() - 1
                route_number = 0
                index = routing.Start(route_number) # Index of the variable for the starting node.
                route = ''
                while not routing.IsEnd(index):
                    # Convert variable indices to node indices in the displayed route.
                    route += str(liste_noeuds[routing.IndexToNode(index)]) + ' -> '
                    index = assignment.Value(routing.NextVar(index))
                    route += str(liste_noeuds[routing.IndexToNode(index)])
                    print('Route:\n\n' + route)
                else:
                    print('No solution found.')
            else:
                print('Specify an instance greater than 0.')

if __name__ == '__main__':
  main('grenoble')

def longue_boucle(reseau, distances):
    long = len(reseau[0])
    while(long > 30):
        antenne = reseau[0].pop()
        insert_plus_proche(antenne, reseau, distances)
