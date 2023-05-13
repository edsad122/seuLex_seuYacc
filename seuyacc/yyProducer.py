from typing import List, Tuple, Dict, Set, Callable
import io

Producer = Tuple[int, List[int]]
producers: List[Producer] = [
    (83, [65]),
    (65, [67, 67]),
    (67, [99, 67]),
    (67, [100, 68]),
    (68, [101]),
    (68, [])
]

map_idname_idx: Dict[str, int] = {}
map_idx_idname: Dict[int, str] = {}

terminators: Set[int] = set()

def idname_to_idx(name: str) -> int:
    assert name in map_idname_idx
    return map_idname_idx[name]

def idx_to_idname(idx: int) -> str:
    assert idx in map_idx_idname
    return map_idx_idname[idx]

def append_new_symbol(idx: int, name: str, is_terminator: bool):
    map_idname_idx[name] = idx
    map_idx_idname[idx] = name
    if is_terminator:
        terminators.add(idx)

def is_terminator(idx: int) -> bool:
    return idx in terminators

def is_terminator(name: str) -> bool:
    idx = idname_to_idx(name)
    return is_terminator(idx)

def dump_producers(print_: Callable[[str], int]):
    for producer in producers:
        left = idx_to_idname(producer[0])
        print_("%s : => " % left)
        for item in producer[1]:
            print_(" %s " % idx_to_idname(item))
        print_()

def write_tab(file: io.TextIOBase, print_: Callable[[io.TextIOBase, str], int]):
    print_(file, "#define WHITESPACE 0  \n /*sp */ \n\n")
    for p_ in map_idname_idx.items():
        if not is_terminator(p_[1]):
            continue
        if not (p_[0][0] >= 'a' and p_[0][0] <= 'z') and not (p_[0][0] >= 'A' and p_[0][0] <= 'Z'):
            continue
        print_(file, "#define %s %s\n" % (p_[0], str(p_[1])))