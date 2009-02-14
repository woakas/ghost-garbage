#!/usr/bin/env python

import sys
import datetime
import time
import optparse

try:
    from pyx import *
except ImportError, e:
    raise SystemExit("Missing python module: pyx (http://pyx.sourceforge.net)")

from parser import *

class Timeline(object):
    WEEKS, MONTHS, QUARTERS, YEARS = range(4)
    mapping = {
        "weeks": WEEKS,
        "months": MONTHS,
        "quarters": QUARTERS,
        "years": YEARS,
        }

    def __init__(self, plotter, tl1, tl2):
        self.pl = plotter
        self.timeline = (self.from_str(tl1), self.from_str(tl2))
    # __init__()

    def from_str(self, text):
        try:
            return Timeline.mapping[text]
        except KeyError, e:
            raise SystemExit("unknow option: %s" % (text,))
    # from_str()

    def get_timeline(self, type):
        if timeline[0] == type:
            return 1
        elif timeline[1] == type:
            return 2
        return 0
    # get_timeline()

    def has_timeline(self, type):
        return type in self.timeline
    # has_timeline()

    def get_y(self, type):
        if self.timeline[0] == type:
            y = self.pl.page_height - self.pl.timeline_height
            if self.pl.tl1_on_top:
                return y - self.pl.timeline_height
            else:
                return y
        elif self.timeline[1] == type:
            if self.pl.tl1_on_top:
                return self.pl.page_height - self.pl.timeline_height
            else:
                return 0
        else:
            return self.pl.page_height / 2 # To make bugs very visible
    # get_y()
# Timeline


class Plotter(object):
    cm = color.cmyk
    bar_height = 0.8
    bar_vskip = 0.05
    text_skip = 0.08
    text_height = 0.5
    comp_height = 0.1
    page_width = 40.0
    advance1 = 0.1
    advance2 = 0.4
    textsize = "" # r"\footnotesize"

    text_encoding = "latin1"

    label_pos = 0 # 0 is left, 1 is right, 2 is top
    task_format = r"{%(text)s}"
    label_project_format = r"{\textbf{\large%(text)s}}"
    label_top_format = r"{\textbf{%(text)s}}"
    label_regular_format = r"{\small%(text)s}"
    milestone_format = r"{" + textsize + "{%(text)s}}"
    enclosure_format = r"{" + textsize + "{%(text)s}}"
    resource_format = r"{\tiny \itshape" \
                      r"\parbox{%(resource_maxwidth)fcm}" \
                      r"{\textcolor[rgb]{0.4,0.4,0.4}{" \
                      r"\begin{flushleft}" \
                      r"%(text)s" \
                      r"\end{flushleft}}}}"
    resource_maxwidth = 3.0
    resource_skip = 0.4
    show_resources = True
    show_vacation  = True
    show_deps      = True
    show_days      = True
    align_to_day   = False
    tl1_on_top     = False
    caption_width  = 0.0
    timeline_height = 0.5

    comp_style = (cm.Black,)
    now_color = cm.Green
    now_skip = 0.3

    status_colors = (cm.Magenta,     # STATUS_UNKNOWN
                     cm.Gray,        # STATUS_NOT_STARTED
                     cm.Salmon,      # STATUS_WIP_LATE
                     cm.Black,       # STATUS_WIP
                     cm.Yellow,      # STATUS_ON_TIME
                     cm.Cyan,        # STATUS_WIP_AHEAD
                     cm.RoyalBlue,   # STATUS_FINISHED
                     cm.Red,         # STATUS_LATE
                     )

    level = 0
    day = 24 * 60 * 60
    time_interval = 7 * day

    caption_style = (style.linewidth.THIN,)

    week_color = color.gray(0.9)
    week_style = (style.linewidth.THIN, deco.filled([week_color]))
    week_format = "W%d"
    shortweek_format = "%d"
    min_week_width = 0.7
    week_line_style = (style.linewidth.THIN, color.gray(0.8),
                       style.linestyle.dashed)

    month_style = (style.linewidth.THIN, deco.filled([week_color]))
    month_line_style = (style.linewidth.THIN, color.gray(0.7),
                        style.linestyle.dashed)
    monthyear_format = "%B, %Y"
    month_format = "%B"
    shortmonth_format = "%b"
    min_monthyear_width = 3.0  # min width for displaying month and year
    min_month_width = 2.0      # min width for displaying month
    min_shortmonth_width = 0.5 # min width for displaying month in 3 letters

    quarter_format = r"Q%d"
    quarter_line_style = (style.linewidth.THIN, color.gray(0.6),
                          style.linestyle.dashed)

    year_style = (style.linewidth.THIN, deco.filled([week_color]))
    year_line_style = (style.linewidth.THIN, color.gray(0.5),
                       style.linestyle.dashed)
    year_format = r"%Y"
    min_year_width = 1.0

    dependency_style = (style.linewidth.normal, cm.Black, deco.earrow.normal)
    vacation_style = (style.linewidth.thin, color.gray(0.9),
                      deco.filled([color.gray(0.95)]))
    day_line_style = (style.linewidth.thin, color.gray(0.8))

    now_format = "Now (%a, %d %b %Y)"

    task_style = (color.cmyk.Black, style.linecap.round, style.linewidth.THIN)
    enclosure_style = (color.cmyk.Black, style.linecap.round,
                       style.linewidth.THIN)
    milestone_style = (style.linewidth.THIN, deco.filled([cm.Black]),
                       style.linejoin.bevel, style.linecap.round)

    task_separator_style = (style.linewidth.THIN, color.gray(0.5))


    def __init__(self, doc):
        self.timelines = Timeline(self, "months", "years")
        self.time_start = 0.0
        self.time_end = 0.0
        self.second_size = 1.0
        self.page_height = 0.0
        self.caption_width = 0
        self.lines = 0
        self.doc = doc
    # __init__()


    def process(self, scenario):
        self.canvas = canvas.canvas()
        self._setup_text()
        self._setup_page_height()
        self._setup_time_range()
        self.output_document(scenario)
    # process()


    def _setup_text(self):
        text.reset()
        text.set(mode="latex")
        text.preamble(r"\usepackage[%s]{inputenc}" % self.text_encoding)
        text.preamble(r"\usepackage{color}")
        text.preamble(r"\usepackage{bookman}")
        text.preamble(r"\definecolor{now_color}{cmyk}"
                      "{%(c)g,%(m)g,%(y)g,%(k)g}" %
                      self.now_color.color)
        text.preamble(r"\parindent=0pt")
    # _setup_text()


    def _setup_page_height(self):
        tasks = 0
        for p in self.doc.prjs.itervalues():
            tasks = max(tasks, len(p._known_tasks))

        self.lines = tasks
        bar_skip = self.bar_height + self.bar_vskip
        if self.label_pos in (0, 1):
            self.bar_skip = max(bar_skip, self.text_height)
        elif self.label_pos == 2:
            self.bar_skip = bar_skip + self.text_height + self.text_skip

        if self.tl1_on_top:
            self.header_height = 2 * self.timeline_height
            self.footer_height = 0
        else:
            self.header_height = self.timeline_height
            self.footer_height = self.timeline_height

        self.useful_height = self.bar_skip * self.lines + self.now_skip
        self.page_height = self.footer_height + self.header_height + \
                           self.useful_height
    # _setup_page_height()


    def _setup_time_range(self):
        start = sys.maxint
        end = -sys.maxint - 1
        for prj in self.doc.prjs.itervalues():
            start = min(start, prj.start)
            end = min(end, prj.end)

        start = datetime.date.fromtimestamp(prj.start)
        start -= datetime.timedelta(14)
        weekday = start.isoweekday()
        if weekday != 1:
            start -= datetime.timedelta(weekday - 1)

        end = datetime.date.fromtimestamp(prj.end)
        weekday = end.isoweekday()
        if weekday != 1:
            end += datetime.timedelta(8 - weekday)

        self.time_start = int(time.mktime(start.timetuple()))
        self.time_end = int(time.mktime(end.timetuple()))
        time_range = self.time_end - self.time_start
        self.time_range = time_range + self.time_interval
        self.second_size = self.page_width / float(self.time_range)
        self.day_size = self.seconds_to_coords(self.day)
    # _setup_time_range()


    def seconds_to_coords(self, seconds):
        return self.second_size * seconds
    # seconds_to_coords()


    def seconds_to_x(self, seconds):
        x = self.second_size * (seconds - self.time_start)
        return self.caption_width + x
    # seconds_to_x()


    def status_to_color(self, taskscenario):
        return self.status_colors[taskscenario.status]
    # status_to_color()


    def diamond(self, x, y, w=0.5, h=0.5, style=()):
        dw = w / 2
        dh = h / 2
        shape = path.path(path.moveto(x - dw, y), path.lineto(x, y + dh),
                          path.lineto(x + dw, y), path.lineto(x, y - dh),
                          path.closepath())
        self.canvas.stroke(shape, style)
    # diamond()

    to_escape = {
        '\\': '$\\backslash$',
        '{': '\\symbol{%d}' % ord('{'),
        '}': '\\symbol{%d}' % ord('}'),
        '#': '\\symbol{%d}' % ord('#'),
        '$': '\\symbol{%d}' % ord('$'),
        '%': '\\symbol{%d}' % ord('%'),
        '&': '\\symbol{%d}' % ord('&'),
        '~': '\\symbol{%d}' % ord('~'),
        '_': '\\symbol{%d}' % ord('_'),
        '^': '\\symbol{%d}' % ord('^')
        }
    def latex_escape(self, text):
        if not text:
            return text

        if isinstance(text, unicode):
            text = text.encode(self.text_encoding)

        escaped = []
        escaped_append = escaped.append
        to_escape_get = self.to_escape.get
        for c in text:
            escaped_append(to_escape_get(c, c))

        return ''.join(escaped)

    def text(self, x, y, text, style=()):
        if isinstance(text, unicode):
            text = text.encode(self.text_encoding)
        self.canvas.text(x, y, text, style)
    # text()


    def rect(self, x, y, w, h, style=(), fillcolor=None, linecolor=()):
        if fillcolor:
            style += (deco.filled((fillcolor,)),)

        shape = path.rect(x, y, w, h)
        if linecolor is not None:
            style += linecolor
            self.canvas.stroke(shape, style)
        else:
            self.canvas.fill(shape, style)
    # rect()


    def line(self, x0, y0, x1, y1, style=()):
        self.canvas.stroke(path.line(x0, y0, x1, y1), style)
    # line()


    def vline(self, x, y, h, style=()):
        self.canvas.stroke(path.line(x, y, x, y + h), style)
    # vline()


    def hline(self, x, y, w, style=()):
        self.canvas.stroke(path.line(x, y, x + w, y), style)
    # hline()


    def fill(self, shape, style=()):
        self.canvas.fill(shape, style)
    # fill()


    def stroke(self, shape, style=()):
        self.canvas.stroke(shape, style)
    # stroke()

    def arrow(self, x1, y1, x2, y2):
        x12 = x1 + self.advance1
        x22 = x2 - self.advance2


        if (x22 <= x12):
            if y2 > y1:
                midy = y1 + self.bar_skip/2
            else:
                midy = y1 - self.bar_skip/2
            self.canvas.stroke(path.path(path.moveto(x1,y1),
                                         path.lineto(x12,y1),
                                         path.lineto(x12,midy),
                                         path.lineto(x22,midy),
                                         path.lineto(x22,y2),
                                         path.lineto(x2,y2)),
                               self.dependency_style)
        else:
            self.canvas.stroke(path.path(path.moveto(x1,y1),
                                         path.lineto(x12,y1),
                                         path.lineto(x12,y2),
                                         path.lineto(x22,y2),
                                         path.lineto(x2,y2)),
                               self.dependency_style)
#         self.canvas.stroke(path.line(x1,y1,x2,y2), self.dependency_style)
    # arrow()

    def level_to_y(self, level):
        return self.page_height - self.header_height - \
               self.bar_skip * (level + 1)
    # level_to_y()


    def place_label(self, lvl, x, y, w, h, label, style=()):
        if self.caption_width > 0.0:
            tx = 0.2 + lvl
            ty = y + h / 2
            flags = (text.halign.boxleft, text.vshift.mathaxis)
        else:
            if self.label_pos == 0:
                tx = x - self.text_skip
                ty = y + h / 2
                flags = (text.halign.boxright, text.vshift.mathaxis)
            elif self.label_pos == 1:
                tx = x + w + self.text_skip
                ty = y + h / 2
                flags = (text.halign.boxleft, text.vshift.mathaxis)
            elif self.label_pos == 2:
                tx = x + w / 2
                ty = y + h + self.text_skip
                flags = (text.halign.boxcenter, text.vshift.bottomzero)

        if lvl == 0:
            fmt = self.label_project_format
        elif lvl == 1:
            fmt = self.label_top_format
        else:
            fmt = self.label_regular_format

        t = fmt % {"text": label,
                   "width": w,
                   "height": h,
                   }
        self.text(tx, ty, t, flags + style)
    # place_label()


    def output_task_milestone(self, lvl, prj, task, scenario):
        sc = task.scenarios[scenario]

        x = self.seconds_to_x(sc.start)
        y = self.level_to_y(task.level)

        w = self.bar_height * 0.75
        h = self.bar_height * 0.75
        w2 = w / 2
        h2 = h / 2

        self.diamond(x, y + h2, w, h, self.milestone_style)

        label = self.milestone_format % \
                {"text": self.latex_escape(task.name),
                 "width": w,
                 "height": h,
                 }
        self.place_label(lvl, x - w2, y + h2, w, h, label)
    # output_task_milestone()

    def _day_align(self, t):
        if self.align_to_day:
            dt = datetime.datetime.fromtimestamp(t)
            if dt.hour >= 12:
                return int(time.mktime(dt.date().timetuple())) + self.day
            else:
                return int(time.mktime(dt.date().timetuple()))
        else:
            return t

    def output_task_enclosure(self, lvl, prj, task, scenario):
        sc = task.scenarios[scenario]

        start = self._day_align(sc.start)
        end   = self._day_align(sc.end)

        x = self.seconds_to_x(start)
        y = self.level_to_y(task.level)

        w = self.seconds_to_coords(end - start)
        h = self.bar_height * 0.4

        h2 = h / 2
        w2 = min(h2 * 0.75, w / 10.0)

        if sc.complete >= 0:
            print "Missing complete bar"

        r = path.path(path.moveto(x, y + h),
                      path.rlineto(w, 0),
                      path.rlineto(0, -h),
                      path.rlineto(-w2, +h2),
                      path.rlineto(-(w - 2 * w2), 0),
                      path.rlineto(-w2, -h2),
                      path.closepath())

        fillstyle = (self.status_to_color(sc),)
        self.stroke(r, self.enclosure_style + (deco.filled(fillstyle),))

        label = self.enclosure_format % \
                {"text": self.latex_escape(task.name),
                 "width": w,
                 "height": h,
                 }
        self.place_label(lvl, x, y + h2, w, h2, label)
    # output_task_enclosure()


    def output_task_regular(self, lvl, prj, task, scenario):
        sc = task.scenarios[scenario]

        start = self._day_align(sc.start)
        end   = self._day_align(sc.end)

        x = self.seconds_to_x(start)
        y = self.level_to_y(task.level)

        w = self.seconds_to_coords(end - start)
        h = self.bar_height

        self.rect(x, y, w, h, style=self.task_style,
                  fillcolor=self.status_to_color(sc))

        if sc.complete >= 0:
            lw = w * sc.complete
            ly = y + (h - self.comp_height)/2
            self.rect(x, ly, lw, self.comp_height, self.comp_style,
                      linecolor=None)

        label = self.task_format % \
                {"text": self.latex_escape(task.name),
                 "width": w,
                 "height": h,
                 }
        self.place_label(lvl, x, y, w, h, label)

        if self.show_resources:
            if self.label_pos != 1:
                tx = x + w + self.resource_skip
                ty = y + h / 2 + self.text_skip / 2
                flags = (text.halign.boxleft, text.valign.middle)
            else:
                tx = x - self.resource_skip
                ty = y + h / 2 + self.text_skip / 2
                flags = (text.halign.boxright, text.valign.middle)

            res = u", ".join(r.name for r in task.resources)
            label = self.resource_format % \
                    {"resource_maxwidth": self.resource_maxwidth,
                     "text": self.latex_escape(res)}
            self.text(tx, ty, label, flags)
    # output_task_regular()

    def output_dep(self, parent, child, scenario):
        if parent.is_milestone:
            start = parent.scenarios[scenario].start
            px = self.seconds_to_x(self._day_align(start)) + 0.3 * \
                 self.bar_height
            py = self.level_to_y(parent.level) + 0.4 * self.bar_height
        else:
            end = parent.scenarios[scenario].end
            px = self.seconds_to_x(self._day_align(end))
            py = self.level_to_y(parent.level) + self.bar_height / 2

        if child.is_milestone:
            start = child.scenarios[scenario].start
            cx = self.seconds_to_x(self._day_align(start)) - 0.375 * \
                 self.bar_height
            cy = self.level_to_y(child.level) + 0.4 * self.bar_height
        else:
            start = child.scenarios[scenario].start
            cx = self.seconds_to_x(self._day_align(start))
            cy = self.level_to_y(child.level)

        self.arrow(px, py, cx, cy)
    # output_dep()

    def set_task_levels(self, task, scenario, level):
        def task_cmp(a, b):
            a_sc = a.scenarios[scenario]
            b_sc = b.scenarios[scenario]
            r = cmp(a_sc.start, b_sc.start)
            if r != 0:
                return r

            if a.is_milestone and not b.is_milestone:
                return -1
            elif not a.is_milestone and b.is_milestone:
                return 1
            elif a.is_milestone and b.is_milestone:
                return 0
            else:
                return cmp(a_sc.duration, b_sc.duration)
        # task_cmp()
        task.tasks.sort(task_cmp)

        task.level = level
        level += 1
        for t in task.tasks:
            level = self.set_task_levels(t, scenario, level)

        return level
    # set_task_levels()

    def output_task(self, lvl, prj, task, scenario):
        if task.is_milestone:
            self.output_task_milestone(lvl, prj, task, scenario)
        else:
            if task.tasks:
                self.output_task_enclosure(lvl, prj, task, scenario)
            else:
                self.output_task_regular(lvl, prj, task, scenario)
        for t in task.tasks:
            self.output_task(lvl+1, prj, t, scenario)
    # output_task()


    def output_week_line(self, x):
        self.vline(x, self.footer_height, self.useful_height,
                   self.week_line_style)
    # output_week_line()

    def output_day_line(self, x):
        if not self.show_days:
            return

        self.vline(x, self.footer_height, self.useful_height,
                   self.day_line_style)
    # output_day_line

    def output_week(self, d, x, y, w, h):
        if w <= 0:
            return

        if self.show_vacation:
            self.rect( x + (5 * self.day_size), self.footer_height,
                       2 * self.day_size,
                       self.useful_height,
                       self.vacation_style)
        if self.day_size > 0.1:
            for i in xrange(1, 7, 1):
                self.output_day_line(x + i * self.day_size)

        self.rect(x, y, w, h, self.week_style)
        if w > self.min_week_width:
            self.text(x, y + h / 2, self.week_format % d,
                      (text.parbox(w), text.valign.middle,
                       text.halign.flushcenter))
        else:
            self.text(x, y + h / 2, self.shortweek_format % d,
                      (text.parbox(w), text.valign.middle,
                       text.halign.flushcenter))
    # output_week()

    def output_month_line(self, x):
        self.vline(x, self.footer_height, self.useful_height,
                   self.month_line_style)
    # output_month_line()

    def output_month(self, d, x, y, w, h):
        if w <= 0:
            return

        self.output_month_line(x)
        self.rect(x, y, w, h, self.month_style)
        if w >= self.min_monthyear_width:
            self.text(x, y + h/2, d.strftime(self.monthyear_format),
                      (text.parbox(w), text.valign.middle,
                       text.halign.flushcenter))
        elif w >= self.min_month_width:
            self.text(x, y + h/2, d.strftime(self.month_format),
                      (text.parbox(w), text.valign.middle,
                       text.halign.flushcenter))
        elif w >= self.min_shortmonth_width:
            self.text(x, y + h/2, d.strftime(self.shortmonth_format),
                      (text.parbox(w), text.valign.middle,
                       text.halign.flushcenter))

    # output_month()

    def output_year(self, d, x, y, w, h):
        if w <= 0:
            return

        self.vline(x, self.footer_height, self.useful_height,
                   self.year_line_style)
        self.rect(x, y, w, h, self.year_style)
        if w >= self.min_year_width:
            self.text(x, y + h/2, d.strftime(self.year_format),
                      (text.parbox(w), text.valign.middle,
                       text.halign.flushcenter))
    # output_year()

    def output_quarter(self, d, x, y, w, h):
        if w <= 0:
            return

        self.rect(x, y, w, h, self.year_style)
        self.vline(x, self.footer_height, self.useful_height,
                   self.quarter_line_style)
        if w >= self.min_year_width:
            quarter = (d.month - 1) / 3 + 1
            self.text(x, y + h/2, self.quarter_format % (quarter,),
                      (text.parbox(w), text.valign.middle,
                       text.halign.flushcenter))
    # output_quarter()

    def output_timeline(self):
        h = self.timeline_height
        start_x = self.seconds_to_x(self.time_start)
        week_x = start_x
        week_y = self.timelines.get_y(Timeline.WEEKS)
        month_x = start_x
        month_y = self.timelines.get_y(Timeline.MONTHS)
        q_x = start_x
        q_y = self.timelines.get_y(Timeline.QUARTERS)
        year_x = start_x
        year_y = self.timelines.get_y(Timeline.YEARS)

        ty = h / 2

        start = datetime.date.fromtimestamp(self.time_start)
        last_week = start.isocalendar()[1]
        last_month = start
        last_q = start
        last_year = start
        time_end = self.time_range + self.time_start + self.day
        t = self.time_start
        wd = datetime.date.fromtimestamp(self.time_start).isocalendar()[2]
        while t < time_end:
            d = datetime.date.fromtimestamp(t)
            iso = d.isocalendar()

            # Ugly hack to compensate for daylight saving time transitions
            dt = datetime.datetime.fromtimestamp(t)
            if dt.hour == 23:
                t += 3600
            elif dt.hour == 1:
                t -= 3600

            if t == self.time_start:
                t += self.day
                wd = (wd % 7) + 1
                continue

            x1 = self.seconds_to_x(t)
            if wd == 1 and self.timelines.has_timeline(Timeline.WEEKS):
                w = x1 - week_x

                if w > 0:
                    self.output_week_line(week_x)
                    self.output_week(last_week, week_x, week_y, w, h)
                    week_x = x1
                    last_week = iso[1]

            if d.day == 1 and self.timelines.has_timeline(Timeline.MONTHS):
                w = x1 - month_x
                if w > 0:
                    self.output_month(last_month, month_x, month_y, w, h)
                month_x = x1
                last_month = d
            if d.day == 1 and d.month in (1, 4, 7, 10) \
                    and self.timelines.has_timeline(Timeline.QUARTERS):
                w = x1 - q_x
                if w > 0:
                    self.output_quarter(last_q, q_x, q_y, w, h)
                q_x = x1
                last_q = d
            if d.day == 1 and d.month == 1 \
                    and self.timelines.has_timeline(Timeline.YEARS):
                w = x1 - year_x
                if w > 0:
                    self.output_year(last_year, year_x, year_y, w, h)
                year_x = x1
                last_year = d


            t += self.day
            wd = (wd % 7) + 1

        if self.timelines.has_timeline(Timeline.WEEKS):
            w = self.caption_width + self.page_width - week_x
            self.output_week(d, week_x, week_y, w, h)
        if self.timelines.has_timeline(Timeline.MONTHS):
            w = self.caption_width + self.page_width - month_x
            self.output_month(d, month_x, month_y, w, h)
        if self.timelines.has_timeline(Timeline.QUARTERS):
            w = self.caption_width + self.page_width - q_x
            self.output_quarter(d, q_x, q_y, w, h)
        if self.timelines.has_timeline(Timeline.YEARS):
            w = self.caption_width + self.page_width - year_x
            self.output_year(d, year_x, year_y, w, h)
        self.hline(self.caption_width, self.footer_height,
                   self.page_width, self.month_style)
        if self.caption_width != 0.0:
            h = self.page_height - self.footer_height - self.header_height
            self.rect(0, self.footer_height, self.caption_width, h,
                      self.caption_style)

    # output_timeline()

    def output_vacations(self):
        for v in self.doc.vacations:
            self.rect(self.seconds_to_x(v.start), self.footer_height,
                      self.seconds_to_coords(v.end - v.start),
                      self.useful_height, self.vacation_style)
    # output_vacations()


    def output_now_line(self, prj):
        x = self.seconds_to_x(prj.now)
        self.vline(x, self.footer_height,
                   self.useful_height,
                   (style.linewidth.THick, self.now_color))

        now = datetime.datetime.fromtimestamp(prj.now)
        now_str = now.strftime(self.now_format)
        self.text(x + 0.1, self.footer_height + self.text_skip,
                  r"\textsf{\scriptsize \textcolor{now_color}{%s}}" % \
                  (now_str,),
                  (text.vshift.bottomzero,))
    # output_now_line()

    def output_depends(self, prj, task, scenario):
        for dep in task.depends:
            self.output_dep(prj.find_task(dep.dependency), task, scenario)

        for t in task.tasks:
            self.output_depends(prj, t, scenario)
    # output_depends()

    def output_project(self, prj, scenario):
        level = 0

        def task_cmp(a, b):
            a_sc = a.scenarios[scenario]
            b_sc = b.scenarios[scenario]
            r = cmp(a_sc.start, b_sc.start)
            if r != 0:
                return r

            if a.is_milestone and not b.is_milestone:
                return -1
            elif not a.is_milestone and b.is_milestone:
                return 1
            elif a.is_milestone and b.is_milestone:
                return 0
            else:
                return cmp(a_sc.duration, b_sc.duration)
        # task_cmp()
        prj.tasks.sort(task_cmp)

        for t in prj.tasks:
            level = self.set_task_levels(t, scenario, level)
        if self.show_deps:
            for t in prj.tasks:
                self.output_depends(prj, t, scenario)
        for t in prj.tasks:
            self.output_task(0, prj, t, scenario)
        for t in prj.tasks[1:]:
            self.hline(0, self.level_to_y(t.level - 1) - self.bar_height/2,
                       self.caption_width + self.page_width,
                       self.task_separator_style)

        if self.show_now:
            self.output_now_line(prj)
    # output_project()


    def output_document(self, scenario):
        if self.show_vacation:
            self.output_vacations()
        self.output_timeline()

        for p in self.doc.prjs.itervalues():
            self.output_project(p, scenario)
    # output_document()


    def save_pdf(self, filename):
        self.canvas.writePDFfile(filename)
    # save_pdf()


    def save_eps(self, filename):
        self.canvas.writeEPSfile(filename)
    # save_eps()


    def save_ps(self, filename):
        self.canvas.writePSfile(filename)
    # save_ps()


    def _to_poster(self, paper_name="A4", paper_width=None,
                   paper_height=None, margin=1.0, length_unit="cm"):

        if paper_name and hasattr(document.paperformat, paper_name):
            paperformat = getattr(document.paperformat, paper_name)
            w = paperformat.width
            h = paperformat.height
        elif paper_width and paper_height and length_unit:
            w = unit.length(float(paper_width), type="t", unit=length_unit)
            h = unit.length(float(paper_height), type="t", unit=length_unit)
            paperformat = document.paperformat(w, h, "User Defined")
        else:
            raise ValueError("Invalid paper spec %r" % paper)

        bbox = self.canvas.bbox()
        canvas_width = unit.tocm(bbox.width())
        canvas_height = unit.tocm(bbox.height())
        canvas_bottom = unit.tocm(bbox.bottom())
        canvas_left = unit.tocm(bbox.left())

        margin = unit.length(float(margin), type="t", unit=length_unit)
        w = unit.tocm(w - 2 * margin)
        h = unit.tocm(h - 2 * margin)

        w1_pages = int(canvas_width / w) + 1
        h1_pages = int(canvas_height / h) + 1
        n1_pages = w1_pages * h1_pages

        w2_pages = int(canvas_width / h) + 1
        h2_pages = int(canvas_height / w) + 1
        n2_pages = w2_pages * h2_pages

        rotate = n1_pages > n2_pages

        if rotate:
            w, h = h, h
            w_pages = w2_pages
            h_pages = h2_pages
        else:
            w_pages = w1_pages
            h_pages = h1_pages

        doc = document.document()
        x = canvas_left
        y = canvas_bottom
        for i in xrange(w_pages):
            y = canvas_bottom

            for j in xrange(h_pages):
                clip = path.rect(x, y, w, h)
                nc = canvas.canvas([canvas.clip(clip)])
                nc.insert(self.canvas)
                doc.append(document.page(nc, paperformat=paperformat,
                                         margin=margin, fittosize=0,
                                         rotated=rotate, centered=1))
                y += h
            # end for h_pages
            x += w
        # end for w_pages
        return doc
    # _to_poster()


    def save_poster_pdf(self, filename, paper_name="A4", paper_width=None,
                        paper_height=None, margin=1.0, length_unit="cm"):
        doc = self._to_poster(paper_name, paper_width, paper_height,
                              margin, length_unit)
        doc.writePDFfile(filename)
    # save_poster_pdf()


    def save_poster_eps(self, filename, paper_name="A4", paper_width=None,
                        paper_height=None, margin=1.0, length_unit="cm"):
        doc = self._to_poster(paper_name, paper_width, paper_height,
                              margin, length_unit)
        doc.writeEPSfile(filename)
    # save_poster_eps()


    def save_poster_ps(self, filename, paper_name="A4", paper_width=None,
                       paper_height=None, margin=1.0, length_unit="cm"):
        doc = self._to_poster(paper_name, paper_width, paper_height,
                              margin, length_unit)
        doc.writePSfile(filename)
    # save_poster_ps()
# Plotter


if __name__ == "__main__":
    usage = "usage: %prog [options] <input.tjx> [output]"
    parser = optparse.OptionParser(usage=usage)
    timeline_choices = Timeline.mapping.keys()
    timeline_txt_choices = ", ".join(timeline_choices)

    parser.add_option("-v", "--no-vacation", action="store_true",
                      default=False,
                      help="don't plot vacation")
    parser.add_option("-y", "--no-day", action="store_true",
                      default=False,
                      help="don't plot day lines")
    parser.add_option("-r", "--no-resources", action="store_true",
                      default=False,
                      help="don't show resource allocation")
    parser.add_option("-d", "--no-deps", action="store_true",
                      default=False,
                      help="don't show dependencies")
    parser.add_option("-N", "--no-now", action="store_true",
                      default=False,
                      help="don't show 'now' line")
    parser.add_option("-t", "--timeline-on-top", action="store_true",
                      default=False,
                      help="place both timelines at the top")
    parser.add_option("-a", "--align-to-day", action="store_true",
                      default=False,
                      help="align tasks to day boundaries")
    parser.add_option("-W", "--chart-width", type="float",
                      default=40.0,
                      help="chart width in centimeters. Default: %default cm.")
    parser.add_option("-w", "--paper-width", type="float",
                      default=10.0,
                      help="paper width in centimeters. Default: %default cm.")
    parser.add_option("-p", "--poster", action="store_true",
                      default=False,
                      help="segment chart into multiple pages")
    parser.add_option("-f", "--timeline1", type="choice",
                      choices=timeline_choices, default="weeks",
                      help=("first timeline, choices are: %s. "
                            "Default: %%default.") % timeline_txt_choices)
    parser.add_option("-s", "--timeline2", type="choice",
                      choices=timeline_choices, default="months",
                      help=("second timeline, choices are: %s. "
                            "Default: %%default.") % timeline_txt_choices)
    parser.add_option("-c", "--caption-width", type="float",
                      default=0.0,
                      help=("caption width at the start of graph, in "
                            "centimeters. Default: %default cm."))
    parser.add_option("-n", "--scenario", default="plan",
                      help=("scenario to use. Default: %default."))

    options, args = parser.parse_args()
    try:
        infile = args[0]
    except IndexError:
        parser.print_help()
        raise SystemExit("Missing parameter: infile")

    try:
        outfile = args[1]
    except IndexError:
        import os
        outfile = os.path.splitext(infile)[0] + ".pdf"
    print >> sys.stderr, "Writing chart to %s" % outfile

    doc = Document(infile)
    plot = Plotter(doc)
    plot.bar_height = 0.4
    plot.bar_vskip = 0.2
    plot.show_vacation = not options.no_vacation
    plot.show_days = not options.no_day
    plot.show_resources = not options.no_resources
    plot.show_deps = not options.no_deps
    plot.show_now = not options.no_now
    plot.tl1_on_top = options.timeline_on_top
    plot.timelines = Timeline(plot, options.timeline1, options.timeline2)
    plot.caption_width = max(options.caption_width, 0.0)
    plot.align_to_day = options.align_to_day
    plot.page_width = options.chart_width
    plot.process(options.scenario)

    if options.poster:
        if outfile.endswith(".eps"):
            plot.save_poster_eps(outfile, paper_width=options.paper_width)
        elif outfile.endswith(".ps"):
            plot.save_poster_ps(outfile)
        else:
            plot.save_poster_pdf(outfile, paper_width=options.paper_width)
    else:
        if outfile.endswith(".eps"):
            plot.save_eps(outfile)
        elif outfile.endswith(".ps"):
            plot.save_ps(outfile)
        else:
            plot.save_pdf(outfile)
