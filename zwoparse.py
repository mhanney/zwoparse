# -*- coding: utf-8 -*-
"""
Parse a Zwift Workout XML file and output a plain text file, csv or json describing the workout.

Usage:
======

usage: zwoparse.py [-h] [-f FTP] [-k KG] [-v VERBOSE] [-m MINDURATION]
                   [-t {txt,csv,json}] [-o OUTFILE]
                   file

Converts a Zwift Workout File to csv or plain text file.

positional arguments:
  file

optional arguments:
  -h, --help            show this help message and exit
  -f FTP, --ftp FTP     The rider's ftp as an integer, e.g. 266
  -k KG, --kg KG        The rider's weight in kilograms to the nearest
                        integer, e.g. 71
  -v VERBOSE, --verbose VERBOSE
                        Also output to stdout
  -m MINDURATION, --minduration MINDURATION
                        Minimum duration allowed for a block of work (in
                        seconds). 0 means no minimum. For values above 0 an
                        attempt will be made to combine workout sections
                        together until the minimum duration specified is met.
                        (Useful for fitting music to workout sections)
  -t {txt,csv,json}, --type {txt,csv,json}
                        The type of file to produce. csv = comma separated
                        values file, txt = plain english. json = JavaScript
                        object notation. The default is txt.
  -o OUTFILE, --outfile OUTFILE
                        The name of the output file, defauts to workout.txt if
                        none given

"""
import argparse
import xml.etree.ElementTree as ET
import datetime
import json
import sys


class Power:
    """ A simple class to represent min and max power targets """

    def __init__(self, min_intensity, max_intensity):
        self.min_intensity = min_intensity
        self.max_intensity = max_intensity


class TextEvent:
    """ A simple class to represent a text event with timeoffset and message.
    timeoffset is seconds from the beginning of the workout. 
    timeoffset_relative is seconds form the beginning of the segment in which the 
    textmessage appears (useful for auto-hotkey timings)"""

    def __init__(self, timeoffset, timeoffset_relative, message):
        self.timeoffset = timeoffset
        self.timeoffset_relative = timeoffset_relative
        self.message = message


class Segment:
    """ A simple class to represent a segment of a workout """

    def __init__(self, start_time, end_time, segment_type, power, cadence, working=False):
        self.start_time = start_time
        self.end_time = end_time
        self.segment_type = segment_type
        self.working = working
        self.duration_ms = (end_time - start_time) * 1000
        self.textevents = []
        self.power = power
        self.cadence = cadence

    def duration(self):
        """ returns the duration of the segment of the workout """
        return self.end_time - self.start_time

    def human_duration(self):
        """ takes a floating point number of seconds as a string and returns
        a humanly readable time in minutes and seconds """
        seconds = self.duration()
        if seconds <= 60:
            return "%d secs" % seconds

        mins, secs = divmod(seconds, 60)

        if secs == 0:
            return "%d mins" % mins

        return "%d mins %d secs" % (mins, secs)

    def human_type(self):
        """ returns the segment_type in a more humanly readable format """
        if self.segment_type == "warmup":
            return "Warm up"

        elif self.segment_type == "cooldown":
            return "Cool down"

        elif self.segment_type == "freeride":
            return "Free ride"

        elif self.segment_type == "steadystate":
            return "Steady state"

        elif self.segment_type == "combined":
            return "Combined"

        elif self.segment_type == "intervalst":
            if self.working:
                return "Work Interval"
            else:
                return "Rest Interval"

    def add_text_event(self, timeoffset, message):
        timeoffset_relative = timeoffset - self.start_time
        self.textevents.append(
            TextEvent(timeoffset, timeoffset_relative, message))

    def toJSON(self):
        """ dumps self as json """
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


def round_to_nearest_second(value):
    """ takes a floating point number of seconds as a string and returns
    the number of seconds as an integer """
    return int(round(float(value)))


def round_to_percentage(value):
    """ takes a floating point number between 0 and 1 and returns
    the percentage value as a string """
    return "%d" % round(100 * float(value))


def convert_to_abs_power(value, ftp_watts):
    """ takes a floating point number between 0 and 1
    ftp absolute watts
    and returns the target effort as absolute W as a string """
    return "%s" % int(float(value) * ftp_watts)


def convert_to_watts_per_kilo(value, ftp_watts, kilos):
    """ takes a floating point number between 0 and 1
    ftp absolute watts, and weight in kg
    and returns the target effort as W/kg as a string """
    return "%s" % round(float(value) * ftp_watts / kilos, 1)


def parse_power(node):
    if node.tag == "FreeRide":
        return Power(0, 0)

    target_intensity = node.get("Power")
    min_intensity = node.get("PowerLow")
    max_intensity = node.get("PowerHigh")

    if target_intensity is None:
        target_intensity = 0

    if min_intensity is None:
        min_intensity = 0

    if max_intensity is None:
        max_intensity = target_intensity

    return Power(min_intensity, max_intensity)


def parse_interval_power(node, state):
    target_intensity = node.get(state + "Power")
    min_intensity = node.get("Power" + state + "Low")
    max_intensity = node.get("Power" + state + "High")

    if target_intensity is None:
        target_intensity = 0

    if min_intensity is None:
        min_intensity = 0

    if max_intensity is None:
        max_intensity = target_intensity

    return Power(min_intensity, max_intensity)


def parse_cadence(node, suffix=""):
    if node.tag == "FreeRide":
        return None

    return node.get("Cadence" + suffix)


def parse_textevents(node, segment):
    for textevent in node.iter("textevent"):
        timeoffset = int(textevent.get("timeoffset"))
        message = textevent.get("message")
        segment.add_text_event(timeoffset, message)

    return segment


def parse(xmlstring, minduration=0):
    segments = []
    tree = ET.ElementTree(ET.fromstring(xmlstring))
    root = tree.getroot()

    name = root.find("name").text + ' - ' + \
        datetime.date.today().strftime("%Y-%m-%d")

    description = root.find("description").text

    workout = root.find("workout")

    time = 0

    for node in workout:
        lower_tag = node.tag.lower()
        if lower_tag == "warmup" \
                or lower_tag == "cooldown" \
                or lower_tag == "freeride" \
                or lower_tag == "steadystate":
            duration = node.get("Duration")
            cadence = parse_cadence(node)
            end_time = time + round_to_nearest_second(duration)
            power = parse_power(node)
            segment = Segment(time, end_time, lower_tag,
                              power, cadence)
            time = end_time
            parse_textevents(node, segment)
            segments.append(segment)

        elif lower_tag == "intervalst":
            repeat = int(node.get("Repeat"))
            on_duration = float(node.get("OnDuration"))
            off_duration = float(node.get("OffDuration"))
            on_power = parse_interval_power(node, "On")
            off_power = parse_interval_power(node, "Off")
            cadence_work = parse_cadence(node)
            cadence_rest = parse_cadence(node, "Resting")

            for i in range(0, repeat):
                end_time = time + round_to_nearest_second(on_duration)
                segment = Segment(time, end_time, lower_tag,
                                  on_power, cadence_work, True)
                time = end_time
                parse_textevents(node, segment)
                segments.append(segment)

                end_time = time + round_to_nearest_second(off_duration)
                segment = Segment(time, end_time, lower_tag,
                                  off_power, cadence_rest, False)
                time = end_time
                parse_textevents(node, segment)
                segments.append(segment)

    if minduration:
        # if minduration greater than zero, combine sections before returning segments
        for i in range(len(segments) - 1, 0, -1):
            seg_current = segments[i]
            seg_previous = segments[i - 1]
            if seg_current.duration_ms < minduration * 1000:
                seg_previous.end_time = seg_previous.end_time + \
                    (seg_current.duration_ms / 1000)

                seg_previous.duration_ms = (
                    seg_previous.end_time - seg_previous.start_time) * 1000

                # clear any text events, because they won't make sense
                seg_previous.textevents = []

                if seg_current.power > seg_previous.power:
                    seg_previous.power = seg_current.power

                if seg_current.cadence > seg_previous.cadence:
                    seg_previous.cadence = seg_current.cadence

                seg_previous.segment_type = 'combined'

                segments.pop(i)

    return {'name': name, 'description': description, 'segments': segments}


def main():
    """ run the module """

    ftp = float(266)
    kilos = float(71)
    filetype = "txt"
    filename = "workout"
    verbose = True
    minduration = 0

    parser = argparse.ArgumentParser(description=(
        """Converts a Zwift Workout File to csv or plain text file."""))

    parser.add_argument(
        "-f",
        "--ftp",
        type=int,
        help="The rider's ftp as an integer, e.g. 266")

    parser.add_argument(
        "-k",
        "--kg",
        type=int,
        help="The rider's weight in kilograms to the nearest integer, e.g. 71")

    parser.add_argument(
        "-v",
        "--verbose",
        type=bool,
        help="Also output to stdout")

    parser.add_argument(
        "-m",
        "--minduration",
        type=int,
        help="Minimum duration allowed for a block of work  (in seconds). 0 means no minimum. For values above 0 an attempt will be made to combine workout sections together until the minimum duration specified is met. (Useful for fitting music to workout sections)")

    parser.add_argument(
        "-t",
        "--type",
        choices=['txt', 'csv', 'json'],
        type=str,
        help="The type of file to produce. csv = comma separated values file, txt = plain english. json = JavaScript object notation. The default is txt."
    )

    parser.add_argument(
        "-o",
        "--outfile",
        type=str,
        help="The name of the output file, defauts to workout.txt if none given"
    )

    parser.add_argument("file", type=argparse.FileType('r'))
    args = parser.parse_args()

    if args.ftp != None:
        ftp = args.ftp

    if args.kg != None:
        kilos = args.kg

    if args.verbose != None:
        verbose = args.verbose

    if args.type != None:
        filetype = args.type

    if args.minduration != None:
        minduration = args.minduration

    if args.outfile != None:
        outfile_with_extension = args.outfile
    else:
        outfile_with_extension = "%s.%s" % (filename, filetype)

    lines = []

    with args.file as input_file:
        xmlstring = input_file.read()
        workout = parse(xmlstring, minduration)

        if filetype == "csv":
            lines.append('Type, StartTime, EndTime, Duration, Duration Formatted, Min Power (% FTP), Min Power (W), Min Power (W/Kg), Max Power  (% FTP), Min Power (W), Min Power (W/Kg), Cadence, Work\n')

            for segment in workout['segments']:
                lines.append('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n' % (segment.human_type(), segment.start_time,
                                                                           segment.end_time, segment.duration(), segment.human_duration(),
                                                                           round_to_percentage(
                    segment.power.min_intensity),
                    convert_to_abs_power(
                    segment.power.min_intensity, ftp),
                    convert_to_watts_per_kilo(
                    segment.power.min_intensity, ftp, kilos),
                    round_to_percentage(
                    segment.power.max_intensity),
                    convert_to_abs_power(
                    segment.power.max_intensity, ftp),
                    convert_to_watts_per_kilo(
                    segment.power.max_intensity, ftp, kilos),
                    segment.cadence if segment.cadence else "", segment.working))

                # textevents are not written to csv because csv is not hierarchic

        elif filetype == "json":
            segments_json = ','.join([x.toJSON() for x in workout['segments']])
            lines.append('{"name": %s, "description" : %s, "segments":[%s]}' % (
                json.dumps(workout['name']), json.dumps(workout['description']), segments_json))

        else:
            lines.append("%s\n\n" % workout['name'])

            lines.append("%s\n\n" % workout['description'])

            for segment in workout['segments']:

                cadence_str = ""
                if segment.cadence is not None:
                    cadence_str = cadence_str + "%s RPM " % segment.cadence

                if segment.power.min_intensity:
                    intensity = "from %s%% FTP to %s%% FTP %s(%s W to %s W, %s W/Kg to %s W/Kg)" % (
                        round_to_percentage(segment.power.min_intensity),
                        round_to_percentage(segment.power.max_intensity),
                        cadence_str,
                        convert_to_abs_power(segment.power.min_intensity, ftp),
                        convert_to_abs_power(segment.power.max_intensity, ftp),
                        convert_to_watts_per_kilo(
                            segment.power.min_intensity, ftp, kilos),
                        convert_to_watts_per_kilo(segment.power.max_intensity, ftp, kilos))
                else:
                    intensity = "%s%% FTP %s(%s W, %s W/Kg)" % (round_to_percentage(segment.power.max_intensity),
                                                                cadence_str,
                                                                convert_to_abs_power(
                        segment.power.max_intensity, ftp),
                        convert_to_watts_per_kilo(segment.power.max_intensity, ftp, kilos))
                lines.append("%s %s for %s\n" % (
                    segment.human_type(), intensity, segment.human_duration()))

                for textevent in segment.textevents:
                    lines.append("\t%s\n" % (textevent.message))

        text_file = open(outfile_with_extension, "w")
        for line in lines:
            text_file.write(line)
            if verbose:
                sys.stdout.write(line)


if __name__ == '__main__':
    main()
