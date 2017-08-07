#!/usr/bin/env python3
import sys
from datetime import datetime, timedelta
from taskw import TaskWarrior
import argparse


def parse_args():
    now = datetime.now()
    parser = argparse.ArgumentParser(
        description="Add a series of tasks to do promote a module")

    parser.add_argument('module', type=str,
                        help="Name of the module you are going to promote")
    parser.add_argument('-d', '--development-time', default=7,
                        help='Number of days to keep in development')
    parser.add_argument('-t', '--testing-time', default=7,
                        help='Number of days to keep in testing')
    parser.add_argument('-s', '--start-time',
                        default=(now + timedelta(minutes=5)).isoformat(),
                        help='When to put this in development')

    return parser.parse_args()


def cob(full_date, cob_hour=15):
    """
    Given a datetime, return a datetime reprsenting close of business
    """
    return datetime(year=full_date.year, month=full_date.month,
                    day=full_date.day, hour=cob_hour)


def sob(full_date, sob_hour=8):
    """
    Given a datetime, return a datetime reprsenting close of business
    """
    return datetime(year=full_date.year, month=full_date.month,
                    day=full_date.day, hour=sob_hour)


def main():
    args = parse_args()
    now = datetime.now()
    import dateparser

    print("Adding module promotion for %s" % args.module)
    w = TaskWarrior(marshal=True)

    # Determine start and due dates
    development_started_by = cob(dateparser.parse(args.start_time))

    development_completed_by = cob(
        now + timedelta(days=args.development_time))
    testing_completed_by = cob(
        development_completed_by + timedelta(days=args.testing_time))

    dev_task = w.task_add("Put {} module in development".format(args.module),
                          due=development_started_by)

    test_task = w.task_add("Put {} module in testing".format(args.module),
                           due=development_completed_by,
                           wait=sob(development_completed_by),
                           depends=[dev_task['uuid']])
    print(test_task)
    production_task = w.task_add(
        "Put {} module in production".format(args.module),
        due=testing_completed_by, depends=[test_task['uuid']],
        wait=sob(testing_completed_by))
    print(production_task)
    return 0


if __name__ == "__main__":
    sys.exit(main())
