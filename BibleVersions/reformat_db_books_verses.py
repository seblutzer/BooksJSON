import os
import shutil
import sqlite3
import unicodedata
from pathlib import Path
from typing import Dict, Tuple, List, Optional, Any


ENGLISH_TO_PORTUGUESE = {
    # Antigo Testamento
    "genesis": "Gênesis",
    "exodus": "Êxodo",
    "leviticus": "Levítico",
    "numbers": "Números",
    "deuteronomy": "Deuteronômio",
    "joshua": "Josué",
    "judges": "Juízes",
    "ruth": "Rute",
    "1 samuel": "1 Samuel",
    "i samuel": "1 Samuel",
    "first samuel": "1 Samuel",
    "2 samuel": "2 Samuel",
    "ii samuel": "2 Samuel",
    "second samuel": "2 Samuel",
    "1 kings": "1 Reis",
    "i kings": "1 Reis",
    "first kings": "1 Reis",
    "2 kings": "2 Reis",
    "ii kings": "2 Reis",
    "second kings": "2 Reis",
    "1 chronicles": "1 Crônicas",
    "i chronicles": "1 Crônicas",
    "first chronicles": "1 Crônicas",
    "2 chronicles": "2 Crônicas",
    "ii chronicles": "2 Crônicas",
    "second chronicles": "2 Crônicas",
    "ezra": "Esdras",
    "nehemiah": "Neemias",
    "esther": "Ester",
    "job": "Jó",
    "psalms": "Salmos",
    "psalm": "Salmos",
    "proverbs": "Provérbios",
    "ecclesiastes": "Eclesiastes",
    "song of solomon": "Cântico dos Cânticos",
    "song of songs": "Cântico dos Cânticos",
    "song of soloman": "Cântico dos Cânticos",
    "canticles": "Cântico dos Cânticos",
    "cânticos": "Cântico dos Cânticos",
    "isaiah": "Isaías",
    "jeremiah": "Jeremias",
    "lamentations": "Lamentações",
    "ezekiel": "Ezequiel",
    "daniel": "Daniel",
    "hosea": "Oseias",
    "joel": "Joel",
    "amos": "Amós",
    "obadiah": "Obadias",
    "jonah": "Jonas",
    "micah": "Miquéias",
    "nahum": "Naum",
    "habakkuk": "Habacuque",
    "zephaniah": "Sofonias",
    "haggai": "Ageu",
    "zechariah": "Zacarias",
    "malachi": "Malaquias",

    # Novo Testamento
    "matthew": "Mateus",
    "mark": "Marcos",
    "luke": "Lucas",
    "john": "João",
    "acts": "Atos",
    "acts of the apostles": "Atos",
    "Atos dos Apóstolos": "Atos",
    "romans": "Romanos",
    "1 corinthians": "1 Coríntios",
    "i corinthians": "1 Coríntios",
    "first corinthians": "1 Coríntios",
    "2 corinthians": "2 Coríntios",
    "ii corinthians": "2 Coríntios",
    "second corinthians": "2 Coríntios",
    "galatians": "Gálatas",
    "ephesians": "Efésios",
    "philippians": "Filipenses",
    "colossians": "Colossenses",
    "1 thessalonians": "1 Tessalonicenses",
    "i thessalonians": "1 Tessalonicenses",
    "first thessalonians": "1 Tessalonicenses",
    "2 thessalonians": "2 Tessalonicenses",
    "ii thessalonians": "2 Tessalonicenses",
    "second thessalonians": "2 Tessalonicenses",
    "1 timothy": "1 Timóteo",
    "i timothy": "1 Timóteo",
    "first timothy": "1 Timóteo",
    "2 timothy": "2 Timóteo",
    "ii timothy": "2 Timóteo",
    "second timothy": "2 Timóteo",
    "titus": "Tito",
    "philemon": "Filemom",
    "hebrews": "Hebreus",
    "james": "Tiago",
    "1 peter": "1 Pedro",
    "i peter": "1 Pedro",
    "first peter": "1 Pedro",
    "2 peter": "2 Pedro",
    "ii peter": "2 Pedro",
    "second peter": "2 Pedro",
    "1 john": "1 João",
    "i john": "1 João",
    "first john": "1 João",
    "2 john": "2 João",
    "ii john": "2 João",
    "second john": "2 João",
    "3 john": "3 João",
    "iii john": "3 João",
    "third john": "3 João",
    "jude": "Judas",
    "revelation": "Apocalipse",
    "revelations": "Apocalipse",
    "the revelation": "Apocalipse",
    "book of revelation": "Apocalipse",
    "revelation of john": "Apocalipse",

    # Deuterocanônicos / Apócrifos
    "1 esdras": "1 Esdras",
    "i esdras": "1 Esdras",
    "first esdras": "1 Esdras",
    "2 esdras": "2 Esdras",
    "ii esdras": "2 Esdras",
    "second esdras": "2 Esdras",
    "tobit": "Tobias",
    "tobias": "Tobias",
    "judith": "Judite",
    "additions to esther": "Adições a Ester",
    "rest of esther": "Adições a Ester",
    "additional psalm": "Salmo Adicional",
    "psalm 151": "Salmo Adicional",
    "wisdom": "Sabedoria de Salomão",
    "wisdom of solomon": "Sabedoria de Salomão",
    "sirach": "Sirac",
    "ecclesiasticus": "Sirac",
    "baruch": "Baruque",
    "prayer of azariah": "Oração de Azarias",
    "song of the three children": "Oração de Azarias",
    "susanna": "Susana",
    "bel and the dragon": "Bel e o Dragão",
    "prayer of manasseh": "Oração de Manassés",
    "prayer of manasses": "Oração de Manassés",
    "1 maccabees": "1 Macabeus",
    "i maccabees": "1 Macabeus",
    "first maccabees": "1 Macabeus",
    "2 maccabees": "2 Macabeus",
    "ii maccabees": "2 Macabeus",
    "second maccabees": "2 Macabeus",
    "3 maccabees": "3 Macabeus",
    "iii maccabees": "3 Macabeus",
    "third maccabees": "3 Macabeus",
    "4 maccabees": "4 Macabeus",
    "iv maccabees": "4 Macabeus",
    "fourth maccabees": "4 Macabeus",
    "i enoch": "1 Enoque",
    "ii enoch": "2 Enoque",
    "iii enoch": "3 Enoque",
    "iv enoch": "4 Enoque",
    "laodiceans": "Laodiceanos",
    "Odes": "Odes de Salomão"
}

BOOK_KEY_TO_ID_NAME: Dict[str, Tuple[int, str]] = {
    # AT (prefixes do TXT costumam ser esses)
    "Gen": (1, "Gênesis"),
    "Exo": (2, "Êxodo"),
    "Lev": (3, "Levítico"),
    "Num": (4, "Números"),
    "Deu": (5, "Deuteronômio"),
    "Jos": (6, "Josué"),
    "Jdg": (7, "Juízes"),
    "Rut": (8, "Rute"),
    "1Sa": (9, "1 Samuel"),
    "2Sa": (10, "2 Samuel"),
    "1Ki": (11, "1 Reis"),
    "2Ki": (12, "2 Reis"),
    "1Ch": (13, "1 Crônicas"),
    "2Ch": (14, "2 Crônicas"),
    "Ezr": (15, "Esdras"),
    "Neh": (16, "Neemias"),
    "1Es": (17, "1 Esdras"),
    "2Es": (18, "2 Esdras"),
    "Tob": (19, "Tobias"),
    "Jdt": (20, "Judite"),
    "Est": (21, "Ester"),
    "1Ma": (22, "1 Macabeus"),
    "2Ma": (23, "2 Macabeus"),
    "3Ma": (24, "3 Macabeus"),
    "4Ma": (25, "4 Macabeus"),
    "Job": (26, "Jó"),
    "Psa": (27, "Salmos"),
    "Man": (28, "Oração de Manassés"),
    "Pro": (29, "Provérbios"),
    "Ecc": (30, "Eclesiastes"),
    "Sng": (31, "Cântico dos Cânticos"),
    "Wis": (32, "Sabedoria de Salomão"),
    "Sir": (33, "Sirac"),
    "Isa": (34, "Isaías"),
    "Jer": (35, "Jeremias"),
    "Lam": (36, "Lamentações"),
    "Bar": (37, "Baruque"),
    "Ezk": (38, "Ezequiel"),
    "Dan": (39, "Daniel"),
    "Hos": (40, "Oseias"),
    "Jol": (41, "Joel"),
    "Amo": (42, "Amós"),
    "Oba": (43, "Obadias"),
    "Jon": (44, "Jonas"),
    "Mic": (45, "Miquéias"),
    "Nam": (46, "Naum"),
    "Hab": (47, "Habacuque"),
    "Zep": (48, "Sofonias"),
    "Hag": (49, "Ageu"),
    "Zec": (50, "Zacarias"),
    "Mal": (51, "Malaquias"),

    # NT
    "Mat": (52, "Mateus"),
    "Mrk": (53, "Marcos"),
    "Luk": (54, "Lucas"),
    "Jhn": (55, "João"),
    "Act": (56, "Atos"),
    "Rom": (57, "Romanos"),
    "1Co": (58, "1 Coríntios"),
    "2Co": (59, "2 Coríntios"),
    "Gal": (60, "Gálatas"),
    "Eph": (61, "Efésios"),
    "Php": (62, "Filipenses"),
    "Col": (63, "Colossenses"),
    "1Th": (64, "1 Tessalonicenses"),
    "2Th": (65, "2 Tessalonicenses"),
    "1Ti": (66, "1 Timóteo"),
    "2Ti": (67, "2 Timóteo"),
    "Tit": (68, "Tito"),
    "Phm": (69, "Filemom"),
    "Heb": (70, "Hebreus"),
    "Jas": (71, "Tiago"),
    #"Jam": (71, "Tiago"),
    "1Pe": (72, "1 Pedro"),
    "2Pe": (73, "2 Pedro"),
    "1Jn": (74, "1 João"),
    "2Jn": (75, "2 João"),
    "3Jn": (76, "3 João"),
    "Jud": (77, "Judas"),
    "Rev": (78, "Apocalipse"),
    "Lao": (79, "Laodiceanos"),
    "1En": (81, "1 Enoque"),
    "2En": (82, "2 Enoque"),
    "3En": (83, "3 Enoque"),
    "Ode": (84, "Odes de Salomão")
}

# =====================
# Requisitos de dados
# =====================
# Este script assume que você já definiu no mesmo arquivo (acima desta rotina):
#
# ENGLISH_TO_PORTUGUESE = {...}
# BOOK_KEY_TO_ID_NAME: Dict[str, Tuple[int, str]] = {...}
#
# Se eles não existirem, o script vai falhar com uma mensagem.

def _require_dicts():
    g = globals()
    if "ENGLISH_TO_PORTUGUESE" not in g or "BOOK_KEY_TO_ID_NAME" not in g:
        raise RuntimeError(
            "Defina as variáveis ENGLISH_TO_PORTUGUESE e BOOK_KEY_TO_ID_NAME acima deste script."
        )


def _strip_accents(s: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn"
    )


def _norm_key(s: str) -> str:
    """Normaliza para comparação: minúsculo, sem acentos e com espaços limpos."""
    s = s or ""
    s = s.replace("\u00A0", " ")  # non-breaking space
    s = " ".join(str(s).split())
    return _strip_accents(s).strip().lower()


def _build_mappings():
    ENGLISH_TO_PORTUGUESE = globals()["ENGLISH_TO_PORTUGUESE"]
    BOOK_KEY_TO_ID_NAME = globals()["BOOK_KEY_TO_ID_NAME"]

    portuguese_norm_to_id: Dict[str, int] = {}
    portuguese_norm_to_name: Dict[str, str] = {}
    for _k, (bid, pname) in BOOK_KEY_TO_ID_NAME.items():
        pn = _norm_key(pname)
        portuguese_norm_to_id[pn] = bid
        portuguese_norm_to_name[pn] = pname

    english_norm_to_portuguese: Dict[str, str] = {}
    for ek, pv in ENGLISH_TO_PORTUGUESE.items():
        english_norm_to_portuguese[_norm_key(ek)] = pv

    return portuguese_norm_to_id, portuguese_norm_to_name, english_norm_to_portuguese


# =====================
# Regras para adições
# =====================
# Essas adições (apócrifos) devem ser inseridas DENTRO de livros canônicos.
# O script detecta o nome do livro vindo do DB de entrada e redistribui os versos:
# - Prayer of Azariah -> Daniel 3, entre 23 e 24 como 23.1, 23.2, ...
# - Susanna -> Daniel 13
# - Bel and the Dragon -> Daniel 14
# - Additions to Esther -> após o último capítulo de Esther (capítulos extras sequenciais)
# - Additional Psalm -> Salmo 151 (dentro de Psalms)


ADDITION_TYPES = {
    "prayer_of_azariah": [
        "prayer of azariah",
        "azariah",
        "prayer of azarias",
        "benediction of azarias",
        "song of azarias",
    ],
    "susanna": [
        "susanna",
        "the history of susanna",
    ],
    "bel_and_the_dragon": [
        "bel and the dragon",
        "bel and the dragon",
        "bel",
        "dragon",
    ],
    "additions_to_esther": [
        "additions to esther",
        "additions of esther",
        "the rest of esther",
        "additional esther",
    ],
    "additional_psalm": [
        "additional psalm",
        "psalm 151",
        "psalm 151",
        "psalm 151",
        "psalm 151 (",
    ],
}


def _detect_addition_type(raw_name: str) -> Optional[str]:
    n = _norm_key(raw_name)
    for atype, keys in ADDITION_TYPES.items():
        for k in keys:
            nk = _norm_key(k)
            if nk and nk in n:
                return atype
    return None


def _find_host_book_ids(
    portuguese_norm_to_id: Dict[str, int],
) -> Tuple[int, int, int]:
    """Retorna (daniel_id, esther_id, psalms_id)."""

    daniel_id = None
    esther_id = None
    psalms_id = None

    for pn, bid in portuguese_norm_to_id.items():
        # pn = normalizado do nome canônico em PT
        if daniel_id is None and (pn == "daniel" or "daniel" in pn):
            daniel_id = bid
        if esther_id is None and (pn == "ester" or "ester" in pn):
            esther_id = bid
        # Psalmos pode estar como "Salmos" ou "Salmo".
        if psalms_id is None and (pn.startswith("salmo") or pn.startswith("salmos") or "salmos" in pn or "psalm" in pn):
            psalms_id = bid

    if daniel_id is None or esther_id is None or psalms_id is None:
        raise RuntimeError(
            "Não foi possível localizar os IDs em BOOK_KEY_TO_ID_NAME para Daniel/Ester/Salmos."
        )

    return daniel_id, esther_id, psalms_id


def _guess_book_id_and_action(
    raw_name: str,
    portuguese_norm_to_id: Dict[str, int],
    portuguese_norm_to_name: Dict[str, str],
    english_norm_to_portuguese: Dict[str, str],
) -> Tuple[int, str, Optional[str]]:
    """Retorna (new_id, canonical_host_name, addition_type).

    addition_type é None quando o livro mapeia para um livro canônico normal.
    Quando addition_type != None, new_id é o ID do livro HOST onde a adição deve ser inserida.
    """

    addition_type = _detect_addition_type(raw_name)

    if addition_type is not None:
        daniel_id, esther_id, psalms_id = _find_host_book_ids(portuguese_norm_to_id)

        if addition_type in {"prayer_of_azariah", "susanna", "bel_and_the_dragon"}:
            host_id = daniel_id
            # canonical name do host:
            # procura um pname cujo normalizado seja "daniel" ou contenha "daniel"
            # (melhor esforço)
            canonical_host_name = None
            for pn, bid in portuguese_norm_to_id.items():
                if bid == host_id and (pn == "daniel" or "daniel" in pn):
                    canonical_host_name = portuguese_norm_to_name[pn]
                    break
            if canonical_host_name is None:
                canonical_host_name = portuguese_norm_to_name.get(_norm_key("Daniel"), "Daniel")
            return host_id, canonical_host_name, addition_type

        if addition_type == "additions_to_esther":
            host_id = esther_id
            canonical_host_name = None
            for pn, bid in portuguese_norm_to_id.items():
                if bid == host_id and (pn == "ester" or "ester" in pn):
                    canonical_host_name = portuguese_norm_to_name[pn]
                    break
            if canonical_host_name is None:
                canonical_host_name = portuguese_norm_to_name.get(_norm_key("Ester"), "Ester")
            return host_id, canonical_host_name, addition_type

        if addition_type == "additional_psalm":
            host_id = psalms_id
            canonical_host_name = None
            for pn, bid in portuguese_norm_to_id.items():
                if bid == host_id and (pn.startswith("salmo") or pn.startswith("salmos") or "salmos" in pn or "psalm" in pn):
                    canonical_host_name = portuguese_norm_to_name[pn]
                    break
            if canonical_host_name is None:
                canonical_host_name = portuguese_norm_to_name.get(_norm_key("Salmos"), "Salmos")
            return host_id, canonical_host_name, addition_type

        # Se cair aqui, não mapeamos.
        raise ValueError(f"Tipo de adição não suportado: {addition_type}")

    # Livro normal: tenta mapear EN->PT e depois PT->id.
    n = _norm_key(raw_name)

    if n in portuguese_norm_to_id:
        return portuguese_norm_to_id[n], portuguese_norm_to_name[n], None

    if n in english_norm_to_portuguese:
        pname = english_norm_to_portuguese[n]
        pn = _norm_key(pname)
        bid = portuguese_norm_to_id.get(pn)
        if bid is not None:
            return bid, portuguese_norm_to_name[pn], None

    # Fallback: substring (ex.: "Wisdom" / "Wisdom of Solomon" / "The Book of Wisdom")
    best_pname = None
    best_len = -1
    for ek_norm, pv in english_norm_to_portuguese.items():
        if ek_norm and ek_norm in n and len(ek_norm) > best_len:
            best_len = len(ek_norm)
            best_pname = pv

    if best_pname is not None:
        pn = _norm_key(best_pname)
        bid = portuguese_norm_to_id.get(pn)
        if bid is not None:
            return bid, portuguese_norm_to_name[pn], None

    raise ValueError(f"Não foi possível mapear o nome do livro '{raw_name}'.")


# =====================
# SQLite helpers
# =====================


def _list_tables(conn: sqlite3.Connection) -> List[str]:
    cur = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
    )
    return [r[0] for r in cur.fetchall()]


def _get_table_columns(conn: sqlite3.Connection, table: str) -> List[str]:
    cur = conn.execute(f"PRAGMA table_info({table})")
    cols = [r[1] for r in cur.fetchall()]
    return cols


def _find_single_candidate_table(tables: List[str], contains: str) -> Optional[str]:
    contains = contains.lower()
    matches = [t for t in tables if contains in t.lower()]
    if not matches:
        return None
    return matches[0]


def _validate_books_schema(cols: List[str]) -> bool:
    norm = {_norm_key(c) for c in cols}
    return norm == {_norm_key("id"), _norm_key("name")}


def _validate_verses_schema(cols: List[str]) -> bool:
    norm = {_norm_key(c) for c in cols}
    # note: verse é a coluna
    return norm == {_norm_key("book_id"), _norm_key("chapter"), _norm_key("verse"), _norm_key("text")}


def _remap_books(
    conn: sqlite3.Connection,
    book_table: str,
    portuguese_norm_to_id: Dict[str, int],
    portuguese_norm_to_name: Dict[str, str],
    english_norm_to_portuguese: Dict[str, str],
) -> Tuple[Dict[int, int], Dict[int, str], List[Tuple[int, str]]]:
    """Retorna:
    - old_id_to_new_id: mapeia id da entrada -> id do host canônico
    - old_id_to_addition_type: para livros de adição, indica qual transformação aplicar
    - books_out: lista (new_id, canonical_name_host) para inserir na tabela books
    """

    cols = _get_table_columns(conn, book_table)

    col_map = {_norm_key(c): c for c in cols}
    if "id" not in col_map or "name" not in col_map:
        raise ValueError(f"Tabela '{book_table}' não possui colunas esperadas 'id' e 'name'.")

    id_col = col_map["id"]
    name_col = col_map["name"]

    cur = conn.execute(f"SELECT {id_col}, {name_col} FROM {book_table}")

    old_id_to_new_id: Dict[int, int] = {}
    old_id_to_addition_type: Dict[int, str] = {}
    books_out_by_id: Dict[int, str] = {}

    for old_id, raw_name in cur.fetchall():
        if raw_name is None:
            continue

        new_id, canonical_host_name, addition_type = _guess_book_id_and_action(
            raw_name,
            portuguese_norm_to_id,
            portuguese_norm_to_name,
            english_norm_to_portuguese,
        )

        old_id_int = int(old_id)
        old_id_to_new_id[old_id_int] = new_id
        if addition_type is not None:
            old_id_to_addition_type[old_id_int] = addition_type

        books_out_by_id[new_id] = canonical_host_name

    books_list = sorted(books_out_by_id.items(), key=lambda x: x[0])
    return old_id_to_new_id, old_id_to_addition_type, [(bid, name) for bid, name in books_list]


def _find_and_parse_verses_table(
    conn: sqlite3.Connection,
    verse_tables: List[str],
) -> Tuple[str, str]:
    """Retorna (table_name, text_column_name).

    A tabela de versos deve ter colunas book_id/chapter/verse, e após remover qualquer coluna 'id',
    deve sobrar exatamente 1 coluna para texto. Se sobrar mais de 1, é ignorada.
    """

    valid_candidates: List[Tuple[str, str]] = []

    for vt in verse_tables:
        cols = _get_table_columns(conn, vt)

        if not cols:
            continue

        # Remover qualquer coluna id (qualquer casing)
        remaining = [c for c in cols if _norm_key(c) != "id"]
        remaining_norm = {_norm_key(c): c for c in remaining}

        required = ["book_id", "chapter", "verse"]
        missing = [r for r in required if r not in remaining_norm]
        if missing:
            continue

        other = [
            c
            for c in remaining
            if _norm_key(c) not in {"book_id", "chapter", "verse"}
        ]

        if len(other) == 1:
            valid_candidates.append((vt, other[0]))
        else:
            if len(other) > 1:
                other_names = ", ".join(other)
                print(
                    f"AVISO: Tabela de versos '{vt}' tem colunas extras para texto: {other_names}. Será ignorada."
                )

    if not valid_candidates:
        raise ValueError("Nenhuma tabela de versos com o formato esperado foi encontrada.")

    if len(valid_candidates) > 1:
        excluded = [t for (t, _tc) in valid_candidates[1:]]
        print(f"AVISO: Múltiplas tabelas de versos válidas encontradas. Excluindo: {', '.join(excluded)}")

    return valid_candidates[0]


def _verify_already_formatted(
    conn: sqlite3.Connection,
    portuguese_norm_to_id: Dict[str, int],
    portuguese_norm_to_name: Dict[str, str],
    english_norm_to_portuguese: Dict[str, str],
) -> bool:
    tables = _list_tables(conn)
    if set(tables) != {"books", "verses"}:
        return False

    books_cols = _get_table_columns(conn, "books")
    verses_cols = _get_table_columns(conn, "verses")

    if not _validate_books_schema(books_cols):
        return False
    if not _validate_verses_schema(verses_cols):
        return False

    # Verificar mapeamento de id por nome para garantir renumeração correta.
    col_map = {_norm_key(c): c for c in books_cols}
    id_col = col_map["id"]
    name_col = col_map["name"]

    old_id_to_expected: Dict[int, int] = {}
    cur = conn.execute(f"SELECT {id_col}, {name_col} FROM books")
    for old_id, raw_name in cur.fetchall():
        if raw_name is None:
            continue
        new_id, _canonical_name, _atype = _guess_book_id_and_action(
            raw_name,
            portuguese_norm_to_id,
            portuguese_norm_to_name,
            english_norm_to_portuguese,
        )
        old_id_to_expected[int(old_id)] = new_id

    if not old_id_to_expected:
        return False

    for old_id, expected_id in old_id_to_expected.items():
        if old_id != expected_id:
            return False

    # Checar coerência: todo book_id presente em verses precisa existir em books.
    verses_col_map = {_norm_key(c): c for c in verses_cols}
    v_book_col = verses_col_map["book_id"]

    cur2 = conn.execute(f"SELECT DISTINCT {v_book_col} FROM verses")
    verse_book_ids = {int(r[0]) for r in cur2.fetchall() if r and r[0] is not None}
    if not verse_book_ids:
        return False

    if not verse_book_ids.issubset(set(old_id_to_expected.keys())):
        return False

    return True


def _create_expected_schema(conn: sqlite3.Connection) -> None:
    cur = conn.cursor()
    cur.execute("CREATE TABLE books (id INTEGER NOT NULL, name TEXT NOT NULL)")
    # verse como TEXT para permitir valores fracionados: 23.1, 23.2, ...
    cur.execute(
        "CREATE TABLE verses (book_id INTEGER NOT NULL, chapter INTEGER NOT NULL, verse TEXT NOT NULL, text TEXT NOT NULL)"
    )
    cur.execute("CREATE INDEX idx_books_id ON books(id)")
    cur.execute("CREATE INDEX idx_verses_book_chap_verse ON verses(book_id, chapter, verse)")
    conn.commit()


def _parse_int_or_zero(v: Any) -> int:
    if v is None:
        return 0
    try:
        return int(v)
    except Exception:
        try:
            return int(float(str(v).strip()))
        except Exception:
            return 0


def _parse_verse_text(v: Any) -> str:
    if v is None:
        return ""
    # se vier tipo int ou str numérica, mantém como string sem perder o valor
    s = str(v).strip()
    if s == "":
        return ""
    return s


def _reformat_one_db(db_path: Path) -> None:
    print(f"Processando: {db_path.name}")

    _require_dicts()
    portuguese_norm_to_id, portuguese_norm_to_name, english_norm_to_portuguese = _build_mappings()

    try:
        conn = sqlite3.connect(str(db_path))
    except Exception as e:
        print(f"AVISO: Não foi possível abrir '{db_path.name}': {e}")
        return

    try:
        if _verify_already_formatted(
            conn,
            portuguese_norm_to_id,
            portuguese_norm_to_name,
            english_norm_to_portuguese,
        ):
            print("OK: Já está exatamente no formato esperado. Pulando.")
            return

        tables = _list_tables(conn)

        book_table = _find_single_candidate_table(tables, "book")
        if not book_table:
            raise ValueError("Não encontrei nenhuma tabela com 'book' no nome.")

        all_book_tables = [t for t in tables if "book" in t.lower()]
        if len(all_book_tables) > 1:
            extras = [t for t in all_book_tables if t != book_table]
            print(f"AVISO: Múltiplas tabelas com 'book' encontradas. Excluindo: {', '.join(extras)}")

        verse_tables = [t for t in tables if "verse" in t.lower()]
        if not verse_tables:
            raise ValueError("Não encontrei nenhuma tabela com 'verse' no nome.")

        old_id_to_new_id, old_id_to_addition_type, books_out = _remap_books(
            conn,
            book_table,
            portuguese_norm_to_id,
            portuguese_norm_to_name,
            english_norm_to_portuguese,
        )

        verses_table, text_col = _find_and_parse_verses_table(conn, verse_tables)
        verses_cols = _get_table_columns(conn, verses_table)
        norm_cols = {_norm_key(c): c for c in verses_cols}

        book_id_col = norm_cols["book_id"]
        chapter_col = norm_cols["chapter"]
        verse_col = norm_cols["verse"]
        text_column = text_col

        # Ler versos da tabela original
        cur = conn.execute(
            f"SELECT {book_id_col}, {chapter_col}, {verse_col}, {text_column} FROM {verses_table}"
        )
        source_rows = cur.fetchall()

        # Pré-cálculos para adições:
        daniel_id, esther_id, psalms_id = _find_host_book_ids(portuguese_norm_to_id)

        # base capítulo de Esther (máximo capítulo existente em Esther normal)
        esther_max_chapter = 0
        for old_book_id, ch, _vs, _tx in source_rows:
            if old_book_id is None:
                continue
            old_id_int = int(old_book_id)
            new_id = old_id_to_new_id.get(old_id_int)
            if new_id != esther_id:
                continue
            if old_id_int in old_id_to_addition_type:
                # é uma adição, não consideramos no máximo existente
                continue
            esther_max_chapter = max(esther_max_chapter, _parse_int_or_zero(ch))

        # Para Prayer of Azariah: precisamos criar mapeamento seq -> 23.1,23.2...
        prayer_old_ids = [
            oid for oid, at in old_id_to_addition_type.items() if at == "prayer_of_azariah"
        ]

        prayer_seq_by_row_index: Dict[int, int] = {}
        if prayer_old_ids:
            prayer_indices: List[int] = [
                i for i, (obid, _ch, _vs, _tx) in enumerate(source_rows)
                if obid is not None and int(obid) in prayer_old_ids
            ]

            # ordenar por capítulo/verso originais para preservar a ordem
            def sort_key(i: int) -> Tuple[int, int]:
                obid, ch, vs, tx = source_rows[i]
                return (_parse_int_or_zero(ch), _parse_int_or_zero(vs))

            prayer_indices.sort(key=sort_key)
            for idx, row_i in enumerate(prayer_indices, start=1):
                prayer_seq_by_row_index[row_i] = idx

        # Para Additions to Esther: min capítulo da adição por livro
        est_add_min_chapter_by_old_id: Dict[int, int] = {}
        for old_id_int, atype in old_id_to_addition_type.items():
            if atype == "additions_to_esther":
                chs = []
                for obid, ch, _vs, _tx in source_rows:
                    if obid is not None and int(obid) == old_id_int:
                        chs.append(_parse_int_or_zero(ch))
                if chs:
                    est_add_min_chapter_by_old_id[old_id_int] = min(chs)
                else:
                    est_add_min_chapter_by_old_id[old_id_int] = 1

        # Criar novo db
        tmp_path = db_path.with_suffix(db_path.suffix + ".tmp")
        out_path = db_path
        backup_path = db_path.with_suffix(db_path.suffix + ".bak")

        if tmp_path.exists():
            tmp_path.unlink()
        if backup_path.exists():
            backup_path.unlink()

        out_conn = sqlite3.connect(str(tmp_path))
        try:
            _create_expected_schema(out_conn)

            out_cur = out_conn.cursor()

            # Inserir livros
            out_cur.executemany(
                "INSERT INTO books (id, name) VALUES (?, ?)",
                books_out,
            )

            # Inserir versos
            inserted = 0
            skipped = 0

            for row_index, (old_book_id, chapter, verse, text) in enumerate(source_rows):
                if old_book_id is None:
                    skipped += 1
                    continue

                old_book_id_int = int(old_book_id)
                if old_book_id_int not in old_id_to_new_id:
                    skipped += 1
                    continue

                new_book_id = old_id_to_new_id[old_book_id_int]
                addition_type = old_id_to_addition_type.get(old_book_id_int)

                if addition_type == "prayer_of_azariah":
                    target_chapter = 3
                    seq = prayer_seq_by_row_index.get(row_index)
                    if seq is None:
                        skipped += 1
                        continue
                    target_verse_text = f"23.{seq}"

                elif addition_type == "susanna":
                    target_chapter = 13
                    target_verse_text = _parse_verse_text(verse)

                elif addition_type == "bel_and_the_dragon":
                    target_chapter = 14
                    target_verse_text = _parse_verse_text(verse)

                elif addition_type == "additions_to_esther":
                    src_ch = _parse_int_or_zero(chapter)
                    min_src_ch = est_add_min_chapter_by_old_id.get(old_book_id_int, 1)
                    target_chapter = esther_max_chapter + (src_ch - min_src_ch) + 1
                    target_verse_text = _parse_verse_text(verse)

                elif addition_type == "additional_psalm":
                    target_chapter = 151
                    target_verse_text = _parse_verse_text(verse)

                else:
                    target_chapter = _parse_int_or_zero(chapter)
                    target_verse_text = _parse_verse_text(verse)

                text_s = "" if text is None else str(text)

                # book_id é inteiro; chapter inteiro; verse TEXTO (inclui frações)
                out_cur.execute(
                    "INSERT INTO verses (book_id, chapter, verse, text) VALUES (?, ?, ?, ?)",
                    (int(new_book_id), int(target_chapter), target_verse_text, text_s),
                )
                inserted += 1

            out_conn.commit()

            out_conn.close()
            conn.close()

            shutil.copy2(str(db_path), str(backup_path))
            shutil.move(str(tmp_path), str(out_path))

            print(
                f"OK: Reformatado. Livros: {len(books_out)}. Versos: {inserted} inseridos. {skipped} pulados. Backup: {backup_path.name}"
            )
        except Exception:
            out_conn.close()
            if tmp_path.exists():
                tmp_path.unlink()
            raise

    finally:
        try:
            conn.close()
        except Exception:
            pass


def main():
    script_dir = Path(__file__).resolve().parent
    db_files = sorted(script_dir.glob("*.db"))

    if not db_files:
        print("Nenhum arquivo .db encontrado na pasta onde o script está.")
        return

    for db in db_files:
        try:
            _reformat_one_db(db)
        except Exception as e:
            print(f"ERRO ao processar '{db.name}': {e}")


if __name__ == "__main__":
    main()

