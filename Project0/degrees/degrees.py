from asyncio import start_server
from concurrent.futures.process import _ThreadWakeup
import csv
from platform import node
from sre_parse import State
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass
    ##print(people) #print the final dataset

def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    ""
    ""
    Approach: 
    1. use BFS for find the shorest path
    2. figure out how many degrees of connections are there
    
    Init:
    checked person id list
    degree = 0
    path = [] ## path is [(movie id, person id),(movie id, person id), ...] each pair is 1 degree
    Steps:
    input source and destination return both person ids
    if source == target
        return degree = 0 "same person"
    add source person id to checked list

    loop
    use neighbor_for_person to return a list of (movie id, person id) -> movie person pair (mpp)

        loop
        if person ids in mpp can be found in the checked person id lists and the queue list
            yes: remove that pair of mpp
        else break the loop and add the person ids in the checked list 

    add mpp to queue
    
    if there is mpp pair in the queue
        yes: take mpp out of queue
        no: return none  ## this means no connetion is found
    
    add mpp to path []

    if the person id in mpp = target person id
        yes: break the loop and return path
    
    """""
    num_explored = 0
    explored = set()

    start = Node(state = source, parent=None, action=None)
    frontier = QueueFrontier()
    frontier.add(start)

    while True:
        if frontier.empty():
                raise Exception("no solution")
        
        node = frontier.remove()
        num_explored += 1

        if node.state == target:
            movies = []
            stars = []
            while node.parent is not None:
                movies.append(node.action)
                stars.append(node.state)
                node = node.parent
            movies.reverse()
            stars.reverse()
            solution = list(zip(movies, stars))
            
            print("Number Explored: ", num_explored, ". Degree: ",len(solution))
            print("Path: ", solution)
            print("Movies: ", movies)
            print("Stars: ", stars)
            return solution
        
        explored.add(node.state)

        for action , state in neighbors_for_person(node.state):
            if not frontier.contains_state(state) and state not in explored:
                child = Node(state = state, parent=node, action = action)
                frontier.add(child)


    raise NotImplementedError


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
