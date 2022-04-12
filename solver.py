from z3 import *;

def find_viable_unmask(field):
    # first aggregate all neighbours of all unmasked fields
    all_neighbours = set()
    all_having_neighbours = set()
    pos_to_neighbour = dict()
    for x in range(field.field_size):
        for y in range(field.field_size):
            if field.is_masked(x, y):
                continue
            n = field.get_neighbours(x, y, True)
            
            if len(n) == 0:
                continue
            
            all_having_neighbours.add(field.coord_to_hash(x, y))
            all_neighbours_hashed = [field.coord_to_hash(p[0], p[1]) for p in n]
            all_neighbours.update(all_neighbours_hashed)
            pos_to_neighbour[field.coord_to_hash(x, y)] = all_neighbours_hashed
    
    # convert to strongly ordered lists
    all_neighbours = list(all_neighbours)
    all_having_neighbours = list(all_having_neighbours)

    neighbour_to_index = dict()
    for i in range(len(all_neighbours)):
        neighbour_to_index[all_neighbours[i]] = i

    s = Solver()
    # construct candidates from open neighbours
    num_candidates = len(all_neighbours)
    unmask_candidates = IntVector('v', num_candidates)
    for i in range(num_candidates): # constrain to boolean values
        s.add(Or(unmask_candidates[i] == 0, unmask_candidates[i] == 1))

    # iterate through all fields having neighbours 
    # and add their respective values as conditions to the solver
    for hashed_pos in all_having_neighbours:
        neighs = pos_to_neighbour[hashed_pos]
        pos = field.hash_to_coord(hashed_pos)
        my_value = field.field_values[pos[0]][pos[1]]
        total = 0
        for n in neighs: # add up all neighbours
            total += unmask_candidates[neighbour_to_index[n]]
        # all neighbouring mines added up must equal the field's value
        s.add(total == my_value) 

    assert s.check() == z3.sat # if its not sat our minesweeper field is broken
    print("Num candidates:", num_candidates) 

    # see if we can be sure of any pos to be free of a mine
    safe_fields = set()
    for i in range(num_candidates):
        s.push()

        s.add(unmask_candidates[i] == 1) # can it be a mine?
        if s.check() == z3.unsat: # it can never be a mine!
            safe_fields.add(i)

        s.pop()
    
    safe_fields = [field.hash_to_coord(all_neighbours[i]) for i in safe_fields]
    print("Safe fields:", safe_fields)
    
    if len(safe_fields) > 0:
        return safe_fields
    if field.is_game_done():
        return safe_fields # all done!
    # no logically 'safe' fields! 
    # we're stuck! lets sample a lot of possible game states 
    # and figure out a spot where theres least likely to be a mine!
    num_samples = 0
    all_vals = []
    while s.check() == z3.sat and num_samples < 1000:
        num_samples += 1
        m = s.model()
        nope = []
        results = []
        # Add condition that the input variables need to differ from the current ones
        for i in range(num_candidates):
            nope.append(m[unmask_candidates[i]] != unmask_candidates[i])
            results.append(m[unmask_candidates[i]].as_long())
        all_vals.append(results)

        s.add(Or(nope))
    print("Found", num_samples, "samples")
    if num_samples == 0:
        return [] # no possible moves to be made
    
    lowest_val = num_samples + 1
    lowest_index = -1
    for col in range(num_candidates):
        sum = 0
        for row in range(len(all_vals)):
            sum += all_vals[row][col]
        if sum < lowest_val:
            lowest_val = sum
            lowest_index = col
    
    if lowest_val < num_samples:
        print("Selected", field.hash_to_coord(all_neighbours[lowest_index]), "with", lowest_val/num_samples, "uncertainty of it not being a mine!")
        return [field.hash_to_coord(all_neighbours[lowest_index])]
    return []