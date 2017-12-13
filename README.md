# zwoparse

Parse a Zwift Workout XML file and output a text file in plain English (.txt),
comma separated values (.csv) or JavaScript object notation (.json).

## Usage

```
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
```

## Plain text example

```
python zwoparse.py JonsMix.zwo -f 266 -k 71
```

```
Jon's Mix - 2017-12-13

This workout was often used by the Zwift development team to test features as well as get a solid hour of training in. It starts with a brief warmup and goes straight into short anaerobic bursts, shortly followed by max effort sprint training, only to be finished with 2 10 minute blocks of Sweet Spot Training.

Warm up from 30% FTP to 70% FTP (79 W to 186 W, 1.1 W/Kg to 2.6 W/Kg) for 6 mins
Work Interval 150% FTP (399 W, 5.6 W/Kg) for 60 secs
Rest Interval 55% FTP (146 W, 2.1 W/Kg) for 1 mins 30 secs
Work Interval 150% FTP (399 W, 5.6 W/Kg) for 60 secs
Rest Interval 55% FTP (146 W, 2.1 W/Kg) for 1 mins 30 secs
Work Interval 150% FTP (399 W, 5.6 W/Kg) for 60 secs
Rest Interval 55% FTP (146 W, 2.1 W/Kg) for 1 mins 30 secs
Steady state 265% FTP (704 W, 9.9 W/Kg) for 10 secs
Steady state 65% FTP (172 W, 2.4 W/Kg) for 2 mins
Steady state 265% FTP (704 W, 9.9 W/Kg) for 10 secs
Steady state 55% FTP (146 W, 2.1 W/Kg) for 1 mins 30 secs
Steady state 265% FTP (704 W, 9.9 W/Kg) for 10 secs
Steady state 45% FTP (119 W, 1.7 W/Kg) for 60 secs
Steady state 265% FTP (704 W, 9.9 W/Kg) for 10 secs
Steady state 35% FTP (93 W, 1.3 W/Kg) for 30 secs
Steady state 265% FTP (704 W, 9.9 W/Kg) for 10 secs
Steady state 60% FTP (159 W, 2.2 W/Kg) for 5 mins
Steady state 89% FTP (236 W, 3.3 W/Kg) for 10 mins
Steady state 60% FTP (159 W, 2.2 W/Kg) for 5 mins
Steady state 89% FTP (236 W, 3.3 W/Kg) for 10 mins
Cool down from 70% FTP to 30% FTP (186 W to 79 W, 2.6 W/Kg to 1.1 W/Kg) for 5 mins
```

## CSV example

```
python zwoparse.py JonsMix.zwo -f 266 -k 71 -t csv
```

```
Type, StartTime, EndTime, Duration, Duration Formatted, Min Power (% FTP), Min Power (W), Min Power (W/Kg), Max Power  (% FTP), Min Power (W), Min Power (W/Kg), Cadence, Work
Warm up,0,360,360,6 mins,30,79,1.1,70,186,2.6,,False
Work Interval,360,420,60,60 secs,0,0,0.0,150,399,5.6,,True
Rest Interval,420,510,90,1 mins 30 secs,0,0,0.0,55,146,2.1,,False
Work Interval,510,570,60,60 secs,0,0,0.0,150,399,5.6,,True
Rest Interval,570,660,90,1 mins 30 secs,0,0,0.0,55,146,2.1,,False
Work Interval,660,720,60,60 secs,0,0,0.0,150,399,5.6,,True
Rest Interval,720,810,90,1 mins 30 secs,0,0,0.0,55,146,2.1,,False
Steady state,810,820,10,10 secs,0,0,0.0,265,704,9.9,,False
Steady state,820,940,120,2 mins,0,0,0.0,65,172,2.4,,False
Steady state,940,950,10,10 secs,0,0,0.0,265,704,9.9,,False
Steady state,950,1040,90,1 mins 30 secs,0,0,0.0,55,146,2.1,,False
Steady state,1040,1050,10,10 secs,0,0,0.0,265,704,9.9,,False
Steady state,1050,1110,60,60 secs,0,0,0.0,45,119,1.7,,False
Steady state,1110,1120,10,10 secs,0,0,0.0,265,704,9.9,,False
Steady state,1120,1150,30,30 secs,0,0,0.0,35,93,1.3,,False
Steady state,1150,1160,10,10 secs,0,0,0.0,265,704,9.9,,False
Steady state,1160,1460,300,5 mins,0,0,0.0,60,159,2.2,,False
Steady state,1460,2060,600,10 mins,0,0,0.0,89,236,3.3,,False
Steady state,2060,2360,300,5 mins,0,0,0.0,60,159,2.2,,False
Steady state,2360,2960,600,10 mins,0,0,0.0,89,236,3.3,,False
Cool down,2960,3260,300,5 mins,70,186,2.6,30,79,1.1,,False
```

## json example, with minimum duration of work set to 5 mins (300 seconds)

```
python zwoparse.py JonsMix.zwo -f 266 -k 71 -t json -m 300
```

```
{
  "name": "Jon's Mix - 2017-12-13",
  "description":
    "This workout was often used by the Zwift development team to test features as well as get a solid hour of training in. It starts with a brief warmup and goes straight into short anaerobic bursts, shortly followed by max effort sprint training, only to be finished with 2 10 minute blocks of Sweet Spot Training.",
  "segments": [
    {
      "cadence": null,
      "duration_ms": 510000,
      "end_time": 510,
      "power": {
        "max_intensity": "0.69999999",
        "min_intensity": "0.30000001"
      },
      "segment_type": "combined",
      "start_time": 0,
      "textevents": [],
      "working": false
    },
    {
      "cadence": null,
      "duration_ms": 310000,
      "end_time": 820,
      "power": {
        "max_intensity": "2.6500001",
        "min_intensity": 0
      },
      "segment_type": "combined",
      "start_time": 510,
      "textevents": [],
      "working": true
    },
    {
      "cadence": null,
      "duration_ms": 340000,
      "end_time": 1160,
      "power": {
        "max_intensity": "2.6500001",
        "min_intensity": 0
      },
      "segment_type": "combined",
      "start_time": 820,
      "textevents": [],
      "working": false
    },
    {
      "cadence": null,
      "duration_ms": 300000,
      "end_time": 1460,
      "power": {
        "max_intensity": "0.60000002",
        "min_intensity": 0
      },
      "segment_type": "steadystate",
      "start_time": 1160,
      "textevents": [],
      "working": false
    },
    {
      "cadence": null,
      "duration_ms": 600000,
      "end_time": 2060,
      "power": {
        "max_intensity": "0.88999999",
        "min_intensity": 0
      },
      "segment_type": "steadystate",
      "start_time": 1460,
      "textevents": [],
      "working": false
    },
    {
      "cadence": null,
      "duration_ms": 300000,
      "end_time": 2360,
      "power": {
        "max_intensity": "0.60000002",
        "min_intensity": 0
      },
      "segment_type": "steadystate",
      "start_time": 2060,
      "textevents": [],
      "working": false
    },
    {
      "cadence": null,
      "duration_ms": 600000,
      "end_time": 2960,
      "power": {
        "max_intensity": "0.88999999",
        "min_intensity": 0
      },
      "segment_type": "steadystate",
      "start_time": 2360,
      "textevents": [],
      "working": false
    },
    {
      "cadence": null,
      "duration_ms": 300000,
      "end_time": 3260,
      "power": {
        "max_intensity": "0.30000001",
        "min_intensity": "0.69999999"
      },
      "segment_type": "cooldown",
      "start_time": 2960,
      "textevents": [],
      "working": false
    }
  ]
}
```
