import QuantLib as ql
import pandas as pd


class Schedule(pd.DataFrame):
    def __init__(self, input: dict):
        self.schedule = self.init_with_ql(input)

    @staticmethod
    def init_with_ql(input: dict):
        effectiveDate = input.get("effectiveDate")
        tenorYears = int(input.get("tenor").split("Y")[0])
        terminationDate = ql.Date(effectiveDate.dayOfMonth(), effectiveDate.month(), effectiveDate.year() + tenorYears)
        ql_schedule = ql.Schedule(effectiveDate, terminationDate, input.get("frequency"), input.get("calendar"), input.get("holidayConvention"), input.get("terminationDateConvention"), input.get("dateGenerationRule"), input.get("endOfMonthRule"))

        schedule = pd.DataFrame({
            "StartDate": list(ql_schedule)[:-1],
            "EndDate": list(ql_schedule)[1:],
        })

        schedule["MidDate"] = [ql.Date((StartDate.serialNumber() + EndDate.serialNumber()) // 2) for StartDate, EndDate in zip(schedule.StartDate, schedule.EndDate)]
        schedule["DayCountFraction"] = [input.get("dayCountConvention").yearFraction(StartDate, EndDate) for StartDate, EndDate in zip(schedule.StartDate, schedule.EndDate)]
        schedule["DayCountFractionActAct"] = [ql.ActualActual(ql.ActualActual.ISDA).yearFraction(StartDate, EndDate) for StartDate, EndDate in zip(schedule.StartDate, schedule.EndDate)]

        return schedule
    
    # def interpolate()


if __name__ == "__main__":
    input = {
        "effectiveDate": ql.Date("2024-01-01", "%Y-%m-%d"),
        "tenor": "5Y",
        "frequency": ql.Period("3M"),
        "calendar": ql.Germany(ql.Germany.Settlement),
        "holidayConvention": ql.Preceding,
        "terminationDateConvention": ql.Preceding,
        "dateGenerationRule": ql.DateGeneration.Forward,
        "endOfMonthRule": False,
        "dayCountConvention": ql.Actual360(),
    }
    schedule = Schedule.init_with_ql(input=input)
    print(abs(schedule['StartDate'][0] - schedule['EndDate'][0]))
    print(schedule)
