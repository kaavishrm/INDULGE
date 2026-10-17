"""Small HTML helpers for the slides (from the Westside v4 deck). Every slide is a <section class="slide"> holding one 16:9 <div class="frame">."""
import re
from html import escape as esc

M_MARK = '<svg class="m" viewBox="0 0 1632 473" aria-hidden="true"><use href="#logo-m"/></svg>'

# The Park's corporate mark (THE / PARK / Hotels, park.svg from theparkhotels.com), drawn in the slide's ink
P_VIEW = '0 0 97 77'  # the symbol carries the logo's own coordinates (257.5 357.5 97 77)
P_MARK = f'<svg viewBox="{P_VIEW}" aria-hidden="true"><use href="#logo-p"/></svg>'
WORDMARK = f'<span class="wm pk" role="img" aria-label="The Park Hotels">{P_MARK}</span>'


def head(section):
    return (f'<div class="head">{WORDMARK}'
            f'<span class="sec"><span class="label">{section}</span>{M_MARK}</span></div>')


def fab(kind, seed=1, cls='fab'):
    """A canvas the deck paints with procedurally drawn cloth (fabric.js) when it scrolls near."""
    return f'<canvas class="{cls}" data-fab="{kind}" data-seed="{seed}" aria-hidden="true"></canvas>'


def slide(sid, section, body, src='', dark=False, cls='', bare=False, cloth=None):
    """bare=True drops the running head (cover, close); cloth=(kind, seed) paints the whole slide with cloth."""
    hd = '' if bare else head(section)
    bg = fab(*cloth) if cloth else ''
    folio = f'<div class="folio"><span class="src">{src}</span><span class="pg label" data-pg></span></div>'
    return (f'<section class="slide{" dark" if dark else ""}{" " + cls if cls else ""}" id="{sid}" aria-label="{esc(section)}">{bg}'
            f'<div class="frame">{hd}<div class="body">{body}</div>{folio}</div></section>')


def sep(n):
    """Set the separators inside a Didone number in the sans (the Didone's are hairlines that vanish)."""
    return re.sub(r'([,–~+])', r'<span class="sep">\1</span>', n)


def chapter(sid, no, title, line, cloth):
    """A chapter opener: cloth full bleed, a Didone chapter number, the chapter title and one line."""
    body = (f'<div class="chap grow"><span class="cn">{no}</span><h2 class="ct">{title}</h2>'
            + (f'<p class="cl">{line}</p>' if line else '') + '</div>')
    return slide(sid, f'{no} · {title}', body, dark=True, cls='chapter scrim', cloth=cloth)


def stat(num, label, source='', small=''):
    s = f'<div class="s">{source}</div>' if source else ''
    sm = f'<small>{small}</small>' if small else ''
    return f'<div class="stat"><div class="num"><span>{sep(num)}{sm}</span></div><div class="k">{label}</div>{s}</div>'


def ul(items, cls='list'):
    return f'<ul class="{cls}">' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'


def table(cols, rows, cls='tbl', right=(), total=None, col_cls=None):
    """cols: header labels; rows: lists of cell HTML; right: indexes of right-aligned columns; total: optional last row."""
    col_cls = col_cls or {}
    def cell(i, v, tag='td'):
        c = []
        dh = f' data-h="{esc(re.sub(r"<[^>]+>", "", cols[i]))}"' if tag == 'td' and i < len(cols) else ''
        if i in right:
            c.append('r')
        if i in col_cls:
            c.append(col_cls[i])
        return f'<{tag}{dh}{" class=" + chr(34) + " ".join(c) + chr(34) if c else ""}>{v}</{tag}>'
    h = '<tr>' + ''.join(cell(i, c, 'th') for i, c in enumerate(cols)) + '</tr>'
    b = ''.join('<tr>' + ''.join(cell(i, v) for i, v in enumerate(r)) + '</tr>' for r in rows)
    if total:
        b += '<tr class="tot">' + ''.join(cell(i, v) for i, v in enumerate(total)) + '</tr>'
    return f'<div class="scroll-x"><table class="{cls}"><thead>{h}</thead><tbody>{b}</tbody></table></div>'


def tile(kind, seed, no, title, dark_text=False, cls=''):
    """A cloth tile with a Didone number top left and a thin uppercase title bottom left."""
    return (f'<div class="tile{" d" if dark_text else ""}{" " + cls if cls else ""}">{fab(kind, seed)}'
            f'<div class="ov"><span class="no">{no}</span><span class="t">{title}</span></div></div>')
