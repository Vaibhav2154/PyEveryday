# import argparse
# from .service import add_expense, list_expenses, summary

# def main():
#     parser = argparse.ArgumentParser(prog="expense-tracker")
#     sub = parser.add_subparsers(dest="cmd", required=True)

#     p_add = sub.add_parser("add", help="Add an expense")
#     p_add.add_argument("--category", "-c", required=True)
#     p_add.add_argument("--amount", "-a", required=True, type=float)
#     p_add.add_argument("--date", "-d", help="YYYY-MM-DD")
#     p_add.add_argument("--note", "-n")

#     p_list = sub.add_parser("list", help="List expenses")
#     p_list.add_argument("--start")
#     p_list.add_argument("--end")

#     p_sum = sub.add_parser("summary", help="Summarize expenses")
#     p_sum.add_argument("--period", "-p", choices=["day", "week", "month"], required=True)
#     p_sum.add_argument("--ref")

#     args = parser.parse_args()

#     if args.cmd == "add":
#         exp = add_expense(args.category, args.amount, args.date, args.note)
#         print(f"Added: {exp.when} | {exp.category} | {exp.amount:.2f} | {exp.note or ''}")
#     elif args.cmd == "list":
#         for e in list_expenses(args.start, args.end):
#             print(f"{e.when} | {e.category} | {e.amount:.2f} | {e.note or ''}")
#     elif args.cmd == "summary":
#         print(summary(args.period, args.ref))

# if __name__ == "__main__":
#     main()


import argparse
import datetime
from .service import add_expense, list_expenses, summary

def main():
    parser = argparse.ArgumentParser(prog="expense-tracker")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # Add command
    p_add = sub.add_parser("add", help="Add an expense")
    p_add.add_argument("--category", "-c", required=True)
    p_add.add_argument("--amount", "-a", required=True, type=float)
    p_add.add_argument("--date", "-d", help="YYYY-MM-DD")
    p_add.add_argument("--note", "-n")

    # List command
    p_list = sub.add_parser("list", help="List expenses")
    p_list.add_argument("--start")
    p_list.add_argument("--end")

    # Summary command
    p_sum = sub.add_parser("summary", help="Summarize expenses")
    p_sum.add_argument("--period", "-p", choices=["day", "week", "month"], required=True)
    p_sum.add_argument(
        "--ref", "-r",
        help="Reference date in YYYY-MM-DD format (default: today)"
    )

    args = parser.parse_args()

    if args.cmd == "add":
        exp = add_expense(args.category, args.amount, args.date, args.note)
        print(f"Added: {exp.when} | {exp.category} | {exp.amount:.2f} | {exp.note or ''}")

    elif args.cmd == "list":
        for e in list_expenses(args.start, args.end):
            print(f"{e.when} | {e.category} | {e.amount:.2f} | {e.note or ''}")

    elif args.cmd == "summary":
        # Default to today if --ref not given
        ref_date = args.ref or datetime.date.today().isoformat()
        result = summary(args.period, ref_date)
        print(f"Summary ({args.period}) for {ref_date}: {result}")

if __name__ == "__main__":
    main()
