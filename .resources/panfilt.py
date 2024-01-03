#!/usr/bin/env python3

from panflute import *
from nbconvert import HTMLExporter

from pathlib import Path
import os
import shutil
import argparse
import csv
from sys import stderr

def handle_links(elem, doc, args=None):
    if isinstance(elem, Figure):
        img = elem.content[0].content[0]
        if "://" in img.url:
            return elem
        tgt = Path(img.url)
        if tgt.suffix in (".csv", ".tsv"):
            # For CSV/TSV "figures", make a table
            title = elem.caption
            has_header = "noheader" not in elem.classes
            with open(tgt) as fh:
                dialect = "excel" if tgt.suffix == ".csv" else "excel-tab"
                reader = csv.reader(fh, dialect=dialect)
                body = []
                for row in reader:
                    cells = [TableCell(Plain(Str(x))) for x in row]
                    body.append(TableRow(*cells))
            header = TableHead(body.pop(0)) if has_header else None
            return Table(TableBody(*body), head=header, caption=title)
    if isinstance(elem, Link):
        if "://" in elem.url:
            return elem
        tgt = Path(elem.url)
        if tgt.suffix == ".ipynb":
            ofile = f"{tgt.stem}.html"
            with open(args.outdir / ofile, "w") as ofh:
                html, res = HTMLExporter().from_filename(tgt)
                ofh.write(html)
            elem.url=ofile
        else:
            shutil.copyfile(tgt, args.outdir/tgt.name)
            elem.url=tgt.name
    return elem


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--outdir", default=Path(os.environ.get('MD2HTML_OUTDIR', ".")), type=Path,
        help="Output directory (must exist)")
    ap.add_argument("args", nargs="+")
    args = ap.parse_args(argv)
    run_filter(handle_links, args=args)

if __name__ == "__main__":
    main()
