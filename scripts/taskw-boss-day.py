#!/usr/bin/env python3

import sys
from dateparser import parse
from dateutil import tz


def parse_args():
    import argparse
    parser = argparse.ArgumentParser(
        description='Get some friendly reports out of taskwarrior')

    parser.add_argument('-s', '--start', default='1 month ago',
                        help='Start time for query.  Default: %(default)s')
    parser.add_argument('-e', '--end', default='now',
                        help='End time for query.  Default: %(default)s')

    return parser.parse_args()


def filter_tasks(start_date, end_date, task_type='completed'):
    from taskw import TaskWarrior
    w = TaskWarrior(marshal=True)

    settings = {
        'TO_TIMEZONE': 'UTC',
        'TIMEZONE': 'US/Eastern',
        'RETURN_AS_TIMEZONE_AWARE': True
    }

    if start_date:
        start = parse(start_date, settings=settings)
    if end_date:
        end = parse(end_date, settings=settings)

    all_tasks = w.load_tasks()[task_type]
    filtered_tasks = []
    for task in all_tasks:
        if (start_date and end_date):
            if task['modified'] < start or task['modified'] > end:
                continue
            else:
                filtered_tasks.append(task)
        else:
            filtered_tasks.append(task)

    # Sort
    filtered_tasks.sort(key=lambda r: r['modified'])

    return filtered_tasks


def main():

    args = parse_args()
    to_zone = tz.gettz('America/New_York')

    recurring_tasks = {}

    print("# Completed\n")
    for task in filter_tasks(args.start, args.end, task_type='completed'):

        if 'recur' in task.keys():
            if task['description'] not in recurring_tasks:
                recurring_tasks[task['description']] = 0
            recurring_tasks[task['description']] += 1
        else:
            if 'annotations' in task:
                annotation_count = len(task['annotations'])
                print(task['modified'].astimezone(to_zone).strftime("%x"),
                      task['description'], "(%s)" % annotation_count)
            else:
                print(task['modified'].astimezone(to_zone).strftime("%x"),
                      task['description'])
            print()
    print("\n# Recurring Tasks Completed\n")
    for k, v in recurring_tasks.items():
        print("%-4s %s\n" % (v, k))
    print("\n# Pending\n")
    for task in filter_tasks(start_date=None, end_date=None,
                             task_type='pending'):

        print("[%-7s] %s" % (task['status'], task['description']))

        if task['status'] == 'waiting':
            print("         Picking task back up on %s" %
                  task['wait'].astimezone(to_zone).strftime("%x"))
        if 'annotations' in task:
            print("%-9s" % "Notes:")
            for annotation in task['annotations']:
                print(
                    "%-9s %s %s\n" % (
                        "",
                        annotation.entry.astimezone(to_zone).strftime("%x"),
                        annotation
                    )
                )

        print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
