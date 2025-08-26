from datetime import datetime, timedelta

import pandas as pd
import os


class Parser:
    SEPTEMBER_FIRST = datetime(2025, 9, 1)

    def __init__(self):
        if os.path.exists("csvs/distribution.csv"):
            self.df_distribution = pd.read_csv("csvs/distribution.csv")
        else:
            self.df_distribution = pd.read_csv(
                f"https://docs.google.com/spreadsheets/d/{os.getenv('SHEET_ID')}/export?format=csv&gid={os.getenv('SHEET_DISTRIBUTION_GID')}")
        if os.path.exists("csvs/schedule.csv"):
            self.df_schedule = pd.read_csv("csvs/schedule.csv", index_col=0)
        else:
            self.df_schedule = pd.read_csv(
                f"https://docs.google.com/spreadsheets/d/{os.getenv('SHEET_ID')}/export?format=csv&gid={os.getenv('SHEET_SCHEDULE_GID')}",
                index_col=0)
        if os.path.exists("csvs/formating.csv"):
            self.df_formating = pd.read_csv("csvs/formating.csv")
        else:
            self.df_formating = pd.read_csv(
                f"https://docs.google.com/spreadsheets/d/{os.getenv('SHEET_ID')}/export?format=csv&gid={os.getenv('SHEET_FORMATING_GID')}")

    def update_dfs(self):
        self.df_distribution = pd.read_csv(
            f"https://docs.google.com/spreadsheets/d/{os.getenv('SHEET_ID')}/export?format=csv&gid={os.getenv('SHEET_DISTRIBUTION_GID')}")
        self.df_schedule = pd.read_csv(
            f"https://docs.google.com/spreadsheets/d/{os.getenv('SHEET_ID')}/export?format=csv&gid={os.getenv('SHEET_SCHEDULE_GID')}",
            index_col=0)
        self.df_formating = pd.read_csv(
            f"https://docs.google.com/spreadsheets/d/{os.getenv('SHEET_ID')}/export?format=csv&gid={os.getenv('SHEET_FORMATING_GID')}")

    def parse_students_subjects(self, email=None, name=None, surname=None):
        if email is not None:
            try:
                return self.df_distribution[self.df_distribution['Пошта'] == email].iloc[0, 4:].dropna().values.tolist()
            except IndexError:
                return []
        elif name is not None and surname is not None:
            try:
                return self.df_distribution[(self.df_distribution['Прізвище'] == surname) & (self.df_distribution['Ім\'я'] == name)].iloc[0, 4:].dropna().values.tolist()
            except IndexError:
                return []
        return []

    def get_day_subjects(self, week, day, subjects):
        resp = {}
        for ind, row in self.df_schedule.iloc[week * 9:week * 9 + 8, day * 14:day * 14 + 14].iterrows():
            resp[ind] = [subj for subj in row if subj in subjects]
            if not resp[ind]:
                del resp[ind]
        return resp

    def get_week_subjects_from_schedule(self, subjects, week):
        resp = {
        }
        for i, day in enumerate(('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday')):
            resp[day] = self.get_day_subjects(week, i, subjects)
            if not resp[day]:
                del resp[day]
        return resp

    def get_interval_subjects_from_schedule(self, subjects, start_date, end_date):
        day = max((start_date - self.SEPTEMBER_FIRST).days, 0)
        final_days = (end_date - self.SEPTEMBER_FIRST).days
        resp = {}
        while day <= final_days:
            if day % 7 != 6:
                str_day = (self.SEPTEMBER_FIRST+timedelta(days=day)).strftime('%d/%m')
                resp[str_day] = self.get_day_subjects(day//7, day % 7, subjects)
                if not resp[str_day]:
                    del resp[str_day]
            day += 1
        return resp

    def format_subject(self, subject):
        return f'- {self.df_formating[self.df_formating["group"] == subject].iloc[0, 2]} ({("лекція", "практика")["(P)" in subject]}, {subject[-5]} група)'

    def compact_format_subject(self, subject):
        return f'{self.df_formating[self.df_formating["group"] == subject].iloc[0, 2]} ({("L", "P")["(P)" in subject]}, {subject[-5]})'

    def format_schedule(self, schedule):
        return "\n\n".join([
            f"<b>{day}</b>:\n{'\n'.join([
                f'<i>{time}</i>:\n{"\n".join([
                    self.format_subject(subj)
                    for subj in schedule[day][time]
                ])}'
                for time in schedule[day]
            ])}" if schedule[day] else ""
            for day in schedule
        ])

    def compact_format_schedule(self, schedule):
        return "\n\n".join([
            f"<b>{day}</b>:\n{'\n'.join([
                f'<i>{time}</i>: {"; ".join([
                    self.format_subject(subj)
                    for subj in schedule[day][time]
                ])}'
                for time in schedule[day]
            ])}" if schedule[day] else ""
            for day in schedule
        ])

    def dump_dfs(self):
        self.df_distribution.to_csv("csvs/distribution.csv", index=False)
        self.df_schedule.to_csv("csvs/schedule.csv")
        self.df_formating.to_csv("csvs/formating.csv", index=False)
