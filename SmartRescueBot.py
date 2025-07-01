import pygame
import heapq
import itertools
import time
GRID_SIZE = 5
CELL_SIZE = 100
WIDTH, HEIGHT = CELL_SIZE * GRID_SIZE, CELL_SIZE * GRID_SIZE
FPS = 3
WHITE = (255, 255, 255)
GRAY = (220, 220, 220)
BLACK = (0, 0, 0)
RED = (200, 50, 50)
GREEN = (50, 200, 50)
BLUE = (50, 50, 255)
YELLOW = (255, 255, 0)
grid = [['.' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
def a_star_search(grid, start, targets):
    rows, cols = len(grid), len(grid[0])
    target_set = set(targets)
    def is_valid(x, y):
        return 0 <= x < rows and 0 <= y < cols and grid[x][y] != 'X'
    def manhattan(p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
    def mst_heuristic(current, remaining_targets):
        if not remaining_targets:
            return 0
        min_to_any = min(manhattan(current, t) for t in remaining_targets)
        edges = [(manhattan(a, b), a, b) for a, b in itertools.combinations(remaining_targets, 2)]
        edges.sort()
        parent = {}
        def find(u):
            while parent[u] != u:
                parent[u] = parent[parent[u]]
                u = parent[u]
            return u
        def union(u, v):
            ru, rv = find(u), find(v)
            if ru != rv:
                parent[rv] = ru
                return True
            return False
        for t in remaining_targets:
            parent[t] = t
        mst_cost = 0
        for cost, u, v in edges:
            if union(u, v):
                mst_cost += cost
        return min_to_any + mst_cost
    pq = []
    initial_state = (start, frozenset())
    heapq.heappush(pq, (0, 0, initial_state, []))
    visited = set()
    while pq:
        f, g, (pos, visited_targets), path = heapq.heappop(pq)
        if visited_targets == target_set:
            return path + [pos]
        if (pos, visited_targets) in visited:
            continue
        visited.add((pos, visited_targets))
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = pos[0] + dx, pos[1] + dy
            if not is_valid(nx, ny):
                continue
            new_pos = (nx, ny)
            new_visited = set(visited_targets)
            if new_pos in target_set:
                new_visited.add(new_pos)
            new_state = (new_pos, frozenset(new_visited))
            h = mst_heuristic(new_pos, target_set - new_visited)
            heapq.heappush(pq, (g + 1 + h, g + 1, new_state, path + [pos]))
    return None
def draw_grid(screen, path, robot_pos, editing=True):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            rect = pygame.Rect(j*CELL_SIZE, i*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, GRAY, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)
            cell = grid[i][j]
            if (i, j) == robot_pos and not editing:
                pygame.draw.circle(screen, BLUE, rect.center, CELL_SIZE//3)
            elif (i, j) in path and not editing:
                pygame.draw.circle(screen, YELLOW, rect.center, CELL_SIZE//5)
            elif cell == 'X':
                pygame.draw.rect(screen, BLACK, rect)
            elif cell == 'T':
                pygame.draw.circle(screen, RED, rect.center, CELL_SIZE//4)
            elif cell == 'R':
                pygame.draw.circle(screen, GREEN, rect.center, CELL_SIZE//4)
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Rescue Robot - Informed Search")
    clock = pygame.time.Clock()
    current_mode = 'X'
    robot_pos = None
    path = []
    editing = True
    while editing:
        screen.fill(WHITE)
        draw_grid(screen, path, robot_pos, editing=True)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_o:
                    current_mode = 'X'
                elif event.key == pygame.K_t:
                    current_mode = 'T'
                elif event.key == pygame.K_r:
                    current_mode = 'R'
                elif event.key == pygame.K_c:
                    current_mode = '.'
                elif event.key == pygame.K_RETURN:
                    editing = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                row, col = y // CELL_SIZE, x // CELL_SIZE
                if current_mode == 'R':
                    for i in range(GRID_SIZE):
                        for j in range(GRID_SIZE):
                            if grid[i][j] == 'R':
                                grid[i][j] = '.'
                    grid[row][col] = 'R'
                    robot_pos = (row, col)
                else:
                    grid[row][col] = current_mode
        clock.tick(30)
    start = None
    targets = []
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if grid[i][j] == 'R':
                start = (i, j)
            elif grid[i][j] == 'T':
                targets.append((i, j))
    if not start or not targets:
        print("Error: Place a robot and at least one target.")
        time.sleep(2)
        pygame.quit()
        return
    path = a_star_search(grid, start, targets)
    if path is None:
        font = pygame.font.SysFont(None, 48)
        screen.fill(WHITE)
        draw_grid(screen, [], start, editing=False)
        text = font.render("No path found", True, RED)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()
        time.sleep(3)
        pygame.quit()
        return
    print("\n--- Robot Step-by-Step Movement ---")
    path_so_far = []
    for step, pos in enumerate(path):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        path_so_far.append(pos)
        screen.fill(WHITE)
        draw_grid(screen, path_so_far, pos, editing=False)
        pygame.display.flip()
        print(f"Step {step + 1}: Robot moved to {pos}")
        clock.tick(FPS)
    total_cost = len(path) - 1
    font = pygame.font.SysFont(None, 32)
    screen.fill(WHITE)
    draw_grid(screen, path_so_far, path_so_far[-1], editing=False)
    summary_lines = ["All targets reached!", f"Total path cost: {total_cost}", f"Total moves: {len(path)}"]
    for i, line in enumerate(summary_lines):
        text_surface = font.render(line, True, BLUE)
        screen.blit(text_surface, (10, HEIGHT - (len(summary_lines) - i) * 30))
    pygame.display.flip()
    time.sleep(5)
    pygame.quit()
if __name__ == "__main__":
    main()
