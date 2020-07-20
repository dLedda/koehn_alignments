from typing import List, Tuple, NamedTuple, Iterator
from collections import OrderedDict
import argparse

Alignment = List[Tuple[int, int]]
Sentence = List[str]


class PhrasePair(NamedTuple):
    e_phrase_span: Tuple[int, int]
    f_phrase_span: Tuple[int, int]


BOX_DRAWING = {
    "dotted": {
        "hili": "██   ██",
        "grey": "░░   ░░",
        "blnk": "  ░░░  ",
    },
    "filled": {
        "hili": "███████",
        "grey": "░░░░░░░",
        "blnk": "       ",
    }
}
CELL_WIDTH = len(BOX_DRAWING["dotted"]["hili"])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-r",
        "--render_type",
        type=str,
        default="both",
        help="How to render the phrases. Choose from 'text', 'image', or 'both'. Default: 'both'"
    )
    parser.add_argument(
        "-s",
        "--hide_alignment",
        action="store_true",
        help="Turn off the initial render of the alignment."
    )
    parser.add_argument(
        "-e",
        "--e_file",
        type=str,
        default="./e",
        help="Location of the file containing the translated sentences, separated by newlines. Default: './e'"
    )
    parser.add_argument(
        "-f",
        "--f_file",
        type=str,
        default="./f",
        help="Location of the file containing the foreign sentences, separated by newlines. Default: './f'"
    )
    parser.add_argument(
        "-a",
        "--align_file",
        type=str,
        default="./align",
        help="Location of the file containing translated sentences, separated by newlines. Default: './align'"
    )
    args = parser.parse_args()

    for e_sent, f_sent, alignment in load_alignments(args.e_file, args.f_file, args.align_file):
        if not args.hide_alignment:
            print_word_grid(f_sent, e_sent, alignment)
            input("Press enter to continue...")
        phrase_pairs = find_all_phrase_pairs_in_alignment(alignment, len(e_sent), len(f_sent))
        render_phrase_pairs(
            phrase_pairs,
            e_sentence=e_sent,
            f_sentence=f_sent,
            render_type=args.render_type,
            alignment=alignment)


def print_word_grid(sent_x: List[str], sent_y: List[str], highlighted_cells: List[Tuple[int, int]], dotted_cells=None):
    if dotted_cells is None:
        dotted_cells = []
    max_e_len = max([len(word) for word in sent_y])
    max_f_len = max([len(word) for word in sent_x])
    print_grid_headers(max_e_len, max_f_len, sent_x)
    for y_ord in range(len(sent_y)):
        for row in range(3):
            left_column_text = sent_y[y_ord].rjust(max_e_len, " ") if row == 1 else " " * max_e_len
            print(left_column_text, end=" ")
            for x_ord in range(len(sent_x)):
                print_appropriate_cell(x_ord, y_ord, highlighted_cells, dotted_cells if row == 1 else [])
            print()


def print_appropriate_cell(x_ord, y_ord, highlighted_cells, dotted_cells):
    test_pair = (y_ord, x_ord)
    if test_pair in highlighted_cells:
        color = "hili"
    elif (y_ord - x_ord) % 2 == 0:
        color = "grey"
    else:
        color = "blnk"
    cell_chars = BOX_DRAWING["dotted" if test_pair in dotted_cells else "filled"][color]
    print(cell_chars, end="")


def print_grid_headers(max_e_len, max_f_len, sent_f, width=CELL_WIDTH):
    for char_pos in range(max_f_len, 0, -1):
        print(" " * max_e_len, end=" ")
        for word in sent_f:
            try:
                print(word[-char_pos].center(width, " "), end="")
            except IndexError:
                print(" " * width, end="")
        print()


def find_all_phrase_pairs_in_alignment(alignment: Alignment, e_len: int, f_len: int) -> OrderedDict:
    phrase_pairs: OrderedDict = OrderedDict()
    for e_start in range(e_len):
        for e_end in range(e_start, e_len):
            f_start, f_end = f_len, -1
            for e_alignment_pos, f_alignment_pos in alignment:
                if e_start <= e_alignment_pos <= e_end:
                    f_start = min(f_alignment_pos, f_start)
                    f_end = max(f_alignment_pos, f_end)
            extracted_phrase_pairs = extract(alignment, e_start, e_end, f_start, f_end, f_len)
            phrase_pairs.update(extracted_phrase_pairs)
    return phrase_pairs


def extract(alignment: Alignment, e_start: int, e_end: int, f_start: int, f_end: int, f_len: int) -> OrderedDict:
    extracted_phrase_pairs = OrderedDict()
    if f_end == -1:
        return extracted_phrase_pairs
    for e_alignment_pos, f_alignment_pos in alignment:
        if (e_alignment_pos < e_start or e_end < e_alignment_pos) and f_start <= f_alignment_pos <= f_end:
            return extracted_phrase_pairs
    f_stretch_s = f_start
    while True:
        f_stretch_e = f_end
        while True:
            extracted_phrase_pairs[PhrasePair(
                e_phrase_span=(e_start, e_end),
                f_phrase_span=(f_stretch_s, f_stretch_e))] = None
            f_stretch_e += 1
            if f_in_alignment(f_stretch_e, alignment) or f_stretch_e >= f_len:
                break
        f_stretch_s -= 1
        if f_in_alignment(f_stretch_s, alignment) or f_stretch_s < 0:
            break
    return extracted_phrase_pairs


def f_in_alignment(sought_f_pos: int, alignment: Alignment):
    for e_pos, f_pos in alignment:
        if sought_f_pos == f_pos:
            return True
    return False


def render_phrase_pairs(phrase_pairs: OrderedDict, e_sentence: List[str], f_sentence: List[str], render_type: str, alignment: Alignment) -> None:
    for pair in phrase_pairs:
        if render_type == "image" or render_type == "both":
            print_word_grid(f_sentence, e_sentence, list_cells_in_phrase_pair(pair), alignment)
        if render_type == "text" or render_type == "both":
            e_span, f_span = pair
            print("E: ", *[e_sentence[i] for i in range(e_span[0], e_span[1] + 1)])
            print("F: ", *[f_sentence[i] for i in range(f_span[0], f_span[1] + 1)])
            print()
        input("Press enter to continue...")


def list_cells_in_phrase_pair(phrase_pair: PhrasePair) -> List[Tuple[int, int]]:
    alignment: Alignment = []
    for e_pos in range(phrase_pair.e_phrase_span[0], phrase_pair.e_phrase_span[1] + 1):
        for f_pos in range(phrase_pair.f_phrase_span[0], phrase_pair.f_phrase_span[1] + 1):
            alignment.append((e_pos, f_pos))
    return alignment


def load_alignments(e_file: str, f_file: str, align_file: str) -> Iterator[Tuple[Sentence, Sentence, Alignment]]:
    for e_sent, f_sent, alignment in zip(sents_in_file(e_file), sents_in_file(f_file), alignments_in_file(align_file)):
        yield e_sent, f_sent, alignment


def alignments_in_file(source_file_loc: str) -> Iterator[Alignment]:
    with open(source_file_loc, 'r') as source_file:
        for line in source_file:
            alignment = []
            positions = line.strip().split()
            for i in range(0, len(positions), 2):
                alignment.append((int(positions[i]), int(positions[i+1])))
            yield alignment


def sents_in_file(source_file_loc: str) -> Iterator[List[str]]:
    with open(source_file_loc, 'r') as source_file:
        for line in source_file:
            yield line.strip().split()


if __name__ == "__main__":
    main()
