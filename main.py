from minesweeper import Minesweeper
from solver import find_viable_unmask

if __name__ == '__main__':
    field = Minesweeper()
    field.generate_mines()

    field.print_field()
    field.unmask_pos(0, 0)
    print("")

    while True:
        field.print_field(non_masked_only=True)
        unmask = find_viable_unmask(field)
        if len(unmask) == 0:
            break
        for u in unmask:
            field.unmask_pos(u[0], u[1])

    if field.is_game_done():
        print("Game done!")
    else:
        print("Stuck!")
        
