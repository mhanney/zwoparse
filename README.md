# zwoparse

Parse a Zwift Workout XML file and output a text file in plain English (.txt),
comma separated values (.csv) or JavaScript object notation (.json).

## Usage

```
usage: zwoparser.py [-h] [-f FTP] [-k KG] [-t {txt|csv|json}] [-o OUTFILE] file

example: python zwoparser.py JonsMix.zwo -f 266 -k 71 -t txt workout.txt

positional arguments:
  file

optional arguments:
  -h, --help            Show this help message and exit
  -t, --type            The type of file to produce. csv = comma separated values file, txt = plain english, json = javascript object notation
  -f FTP, --ftp FTP     The rider's ftp as an integer, e.g. 266
  -k KG, --kg KG        The rider's weight in kilograms to the nearest
                        integer, e.g. 71
  -v, --verbose         Verbose - also output to stdout
  -o OUTFILE, --outfile OUTFILE
                        The name of the output file, defauts to workout.txt if
                        none given
```

## Plain Text Example

```
python zwoparse.py JonsMix.zwo -f 266 -k 71
```

```
Jon's Mix - 2017-12-11

This workout was often used by the Zwift development team to test features as well as get a solid hour of training in. It starts with a brief warmup and goes straight into short anaerobic bursts, shortly followed by max effort sprint training, only to be finished with 2 10 minute blocks of Sweet Spot Training.

Warm up for 6 mins at 79 W to 186 W (1.1 W/Kg to 2.6 W/Kg) (30% FTP to 70% FTP)
Work Interval for 60 secs at 399 W (5.6 W/Kg) (150% FTP)
Rest Interval for 1 mins 30 secs at 146 W (2.1 W/Kg) (55% FTP)
Work Interval for 60 secs at 399 W (5.6 W/Kg) (150% FTP)
Rest Interval for 1 mins 30 secs at 146 W (2.1 W/Kg) (55% FTP)
Work Interval for 60 secs at 399 W (5.6 W/Kg) (150% FTP)
Rest Interval for 1 mins 30 secs at 146 W (2.1 W/Kg) (55% FTP)
Steady state for 10 secs at 704 W (9.9 W/Kg) (265% FTP)
Steady state for 2 mins at 172 W (2.4 W/Kg) (65% FTP)
Steady state for 10 secs at 704 W (9.9 W/Kg) (265% FTP)
Steady state for 1 mins 30 secs at 146 W (2.1 W/Kg) (55% FTP)
Steady state for 10 secs at 704 W (9.9 W/Kg) (265% FTP)
Steady state for 60 secs at 119 W (1.7 W/Kg) (45% FTP)
Steady state for 10 secs at 704 W (9.9 W/Kg) (265% FTP)
Steady state for 30 secs at 93 W (1.3 W/Kg) (35% FTP)
Steady state for 10 secs at 704 W (9.9 W/Kg) (265% FTP)
Steady state for 5 mins at 159 W (2.2 W/Kg) (60% FTP)
Steady state for 10 mins at 236 W (3.3 W/Kg) (89% FTP)
Steady state for 5 mins at 159 W (2.2 W/Kg) (60% FTP)
Steady state for 10 mins at 236 W (3.3 W/Kg) (89% FTP)
Cool down for 5 mins at 186 W to 79 W (2.6 W/Kg to 1.1 W/Kg) (70% FTP to 30% FTP)
```

## CSV (Comma Separated Values) Example

```
python zwoparse.py JonsMix.zwo -f 266 -k 71 -t csv
```

```
Type, StartTime, EndTime, Duration, Duration Formatted, Min Power (% FTP), Min Power (W), Min Power (W/Kg), Max Power  (% FTP), Min Power (W), Min Power (W/Kg), Tempo, Work
warmup, Warm up, 0, 360, 360, 6 mins, 30, 79, 1.1, 70, 186, 2.6, 0, False
intervalst, Work Interval, 361, 421, 60, 60 secs, 0, 0, 0.0, 150, 399, 5.6, 0, True
intervalst, Rest Interval, 422, 512, 90, 1 mins 30 secs, 0, 0, 0.0, 55, 146, 2.1, 0, False
intervalst, Work Interval, 513, 573, 60, 60 secs, 0, 0, 0.0, 150, 399, 5.6, 0, True
intervalst, Rest Interval, 574, 664, 90, 1 mins 30 secs, 0, 0, 0.0, 55, 146, 2.1, 0, False
intervalst, Work Interval, 665, 725, 60, 60 secs, 0, 0, 0.0, 150, 399, 5.6, 0, True
intervalst, Rest Interval, 726, 816, 90, 1 mins 30 secs, 0, 0, 0.0, 55, 146, 2.1, 0, False
steadystate, Steady state, 817, 827, 10, 10 secs, 0, 0, 0.0, 265, 704, 9.9, 0, False
steadystate, Steady state, 828, 948, 120, 2 mins, 0, 0, 0.0, 65, 172, 2.4, 0, False
steadystate, Steady state, 949, 959, 10, 10 secs, 0, 0, 0.0, 265, 704, 9.9, 0, False
steadystate, Steady state, 960, 1050, 90, 1 mins 30 secs, 0, 0, 0.0, 55, 146, 2.1, 0, False
steadystate, Steady state, 1051, 1061, 10, 10 secs, 0, 0, 0.0, 265, 704, 9.9, 0, False
steadystate, Steady state, 1062, 1122, 60, 60 secs, 0, 0, 0.0, 45, 119, 1.7, 0, False
steadystate, Steady state, 1123, 1133, 10, 10 secs, 0, 0, 0.0, 265, 704, 9.9, 0, False
steadystate, Steady state, 1134, 1164, 30, 30 secs, 0, 0, 0.0, 35, 93, 1.3, 0, False
steadystate, Steady state, 1165, 1175, 10, 10 secs, 0, 0, 0.0, 265, 704, 9.9, 0, False
steadystate, Steady state, 1176, 1476, 300, 5 mins, 0, 0, 0.0, 60, 159, 2.2, 0, False
steadystate, Steady state, 1477, 2077, 600, 10 mins, 0, 0, 0.0, 89, 236, 3.3, 0, False
steadystate, Steady state, 2078, 2378, 300, 5 mins, 0, 0, 0.0, 60, 159, 2.2, 0, False
steadystate, Steady state, 2379, 2979, 600, 10 mins, 0, 0, 0.0, 89, 236, 3.3, 0, False
cooldown, Cool down, 2980, 3280, 300, 5 mins, 70, 186, 2.6, 30, 79, 1.1, 0, False
```

## json (javascript object notation) Example

```
python zwoparse.py JonsMix.zwo -f 266 -k 71 -t json
```

```
{
  "name": "Jon's Mix - 2017-12-11",
  "description":
    "This workout was often used by the Zwift development team to test features as well as get a solid hour of training in. It starts with a brief warmup and goes straight into short anaerobic bursts, shortly followed by max effort sprint training, only to be finished with 2 10 minute blocks of Sweet Spot Training.",
  "segments": [
    {
      "cadence": 0,
      "duration_ms": 360000,
      "end_time": 360,
      "power": {
        "max_intensity": "0.69999999",
        "min_intensity": "0.30000001"
      },
      "segment_type": "warmup",
      "start_time": 0,
      "working": false
    },
    {
      "cadence": 0,
      "duration_ms": 60000,
      "end_time": 421,
      "power": {
        "max_intensity": "1.5",
        "min_intensity": 0
      },
      "segment_type": "intervalst",
      "start_time": 361,
      "working": true
    },
    {
      "cadence": 0,
      "duration_ms": 90000,
      "end_time": 512,
      "power": {
        "max_intensity": "0.55000001",
        "min_intensity": 0
      },
      "segment_type": "intervalst",
      "start_time": 422,
      "working": false
    },
    {
      "cadence": 0,
      "duration_ms": 60000,
      "end_time": 573,
      "power": {
        "max_intensity": "1.5",
        "min_intensity": 0
      },
      "segment_type": "intervalst",
      "start_time": 513,
      "working": true
    },
    {
      "cadence": 0,
      "duration_ms": 90000,
      "end_time": 664,
      "power": {
        "max_intensity": "0.55000001",
        "min_intensity": 0
      },
      "segment_type": "intervalst",
      "start_time": 574,
      "working": false
    },
    {
      "cadence": 0,
      "duration_ms": 60000,
      "end_time": 725,
      "power": {
        "max_intensity": "1.5",
        "min_intensity": 0
      },
      "segment_type": "intervalst",
      "start_time": 665,
      "working": true
    },
    {
      "cadence": 0,
      "duration_ms": 90000,
      "end_time": 816,
      "power": {
        "max_intensity": "0.55000001",
        "min_intensity": 0
      },
      "segment_type": "intervalst",
      "start_time": 726,
      "working": false
    },
    {
      "cadence": 0,
      "duration_ms": 10000,
      "end_time": 827,
      "power": {
        "max_intensity": "2.6500001",
        "min_intensity": 0
      },
      "segment_type": "steadystate",
      "start_time": 817,
      "working": false
    },
    {
      "cadence": 0,
      "duration_ms": 120000,
      "end_time": 948,
      "power": {
        "max_intensity": "0.64999998",
        "min_intensity": 0
      },
      "segment_type": "steadystate",
      "start_time": 828,
      "working": false
    },
    {
      "cadence": 0,
      "duration_ms": 10000,
      "end_time": 959,
      "power": {
        "max_intensity": "2.6500001",
        "min_intensity": 0
      },
      "segment_type": "steadystate",
      "start_time": 949,
      "working": false
    },
    {
      "cadence": 0,
      "duration_ms": 90000,
      "end_time": 1050,
      "power": {
        "max_intensity": "0.55000001",
        "min_intensity": 0
      },
      "segment_type": "steadystate",
      "start_time": 960,
      "working": false
    },
    {
      "cadence": 0,
      "duration_ms": 10000,
      "end_time": 1061,
      "power": {
        "max_intensity": "2.6500001",
        "min_intensity": 0
      },
      "segment_type": "steadystate",
      "start_time": 1051,
      "working": false
    },
    {
      "cadence": 0,
      "duration_ms": 60000,
      "end_time": 1122,
      "power": {
        "max_intensity": "0.44999999",
        "min_intensity": 0
      },
      "segment_type": "steadystate",
      "start_time": 1062,
      "working": false
    },
    {
      "cadence": 0,
      "duration_ms": 10000,
      "end_time": 1133,
      "power": {
        "max_intensity": "2.6500001",
        "min_intensity": 0
      },
      "segment_type": "steadystate",
      "start_time": 1123,
      "working": false
    },
    {
      "cadence": 0,
      "duration_ms": 30000,
      "end_time": 1164,
      "power": {
        "max_intensity": "0.35000002",
        "min_intensity": 0
      },
      "segment_type": "steadystate",
      "start_time": 1134,
      "working": false
    },
    {
      "cadence": 0,
      "duration_ms": 10000,
      "end_time": 1175,
      "power": {
        "max_intensity": "2.6500001",
        "min_intensity": 0
      },
      "segment_type": "steadystate",
      "start_time": 1165,
      "working": false
    },
    {
      "cadence": 0,
      "duration_ms": 300000,
      "end_time": 1476,
      "power": {
        "max_intensity": "0.60000002",
        "min_intensity": 0
      },
      "segment_type": "steadystate",
      "start_time": 1176,
      "working": false
    },
    {
      "cadence": 0,
      "duration_ms": 600000,
      "end_time": 2077,
      "power": {
        "max_intensity": "0.88999999",
        "min_intensity": 0
      },
      "segment_type": "steadystate",
      "start_time": 1477,
      "working": false
    },
    {
      "cadence": 0,
      "duration_ms": 300000,
      "end_time": 2378,
      "power": {
        "max_intensity": "0.60000002",
        "min_intensity": 0
      },
      "segment_type": "steadystate",
      "start_time": 2078,
      "working": false
    },
    {
      "cadence": 0,
      "duration_ms": 600000,
      "end_time": 2979,
      "power": {
        "max_intensity": "0.88999999",
        "min_intensity": 0
      },
      "segment_type": "steadystate",
      "start_time": 2379,
      "working": false
    },
    {
      "cadence": 0,
      "duration_ms": 300000,
      "end_time": 3280,
      "power": {
        "max_intensity": "0.30000001",
        "min_intensity": "0.69999999"
      },
      "segment_type": "cooldown",
      "start_time": 2980,
      "working": false
    }
  ]
}
```
