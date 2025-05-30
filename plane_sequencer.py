"""

For U3O3 SAT. Part1.
To settle the assumption that orders can contain supplie quantities greater than the carry capacity of either plane.

"""

from constants import SMALLER_PLANE, LARGER_PLANE, C1, C2

def determine_planes ( net_weight ):
    # Alternate planes to simultaneously complete orders.
    # Only use larger plane if remaining weight is in [C2, 2 * C1]

    print(f"Sequence for {net_weight} kg order")
    
    remaining_weight = net_weight
    
    plane_sequence = [] # (Zero-Indexed)
    num_planes = 0
    previous_plane = None
    
    while remaining_weight > 0:
        
        if (remaining_weight <= C1 or remaining_weight > C2) and previous_plane != SMALLER_PLANE:
            plane_sequence.append( SMALLER_PLANE )
            remaining_weight -= C1
            previous_plane = SMALLER_PLANE
            
        else:
            plane_sequence.append( LARGER_PLANE )
            remaining_weight -= C2
            previous_plane = LARGER_PLANE

        num_planes += 1
    
    print("Fleet Total Carry Capacity:", net_weight - remaining_weight)
      
    return plane_sequence
    
if __name__ == "__main__":
    print()

    print( determine_planes(6000.0), "\n")
    print( determine_planes(5600.0), "\n" )
    print( determine_planes(5500.0), "\n" )
    print( determine_planes(5400.0), "\n" )