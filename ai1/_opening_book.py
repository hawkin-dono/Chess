from ._helper import load_dict_from_txt

"""
(12 opening moves - 28561 games)

Carlsen.pgn [5662]
Kasparov.pgn [2128]
Stockfish vs AlphaZero [117]
Dragon_by_Komodo_3_2_64-bit_8CPU.bare.[3701].pgn
Dragon_by_Komodo_3_3_64-bit_8CPU.bare.[2954].pgn
Stockfish_14_1_64-bit_8CPU.bare.[1719].pgn
Stockfish_14_64-bit_8CPU.bare.[1932].pgn
Stockfish_15_1_64-bit_8CPU.bare.[1663].pgn
Stockfish_15_64-bit_8CPU.bare.[2687].pgn
Stockfish_16_1_64-bit_8CPU.bare.[2505].pgn
Stockfish_16_64-bit_8CPU.bare.[3100].pgn
Torch_v1_64-bit_8CPU.bare.[2519].pgn
Torch_v2_64-bit_8CPU.bare.[1748].pgn
"""

WHITE_OPENING_BOOK = load_dict_from_txt('ai1/data/white_opening_book.txt')
BLACK_OPENING_BOOK = load_dict_from_txt('ai1/data/black_opening_book.txt')

OPENING_BOOK = {
    True: WHITE_OPENING_BOOK,
    False: BLACK_OPENING_BOOK,
}