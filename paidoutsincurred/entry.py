from pydantic import BaseModel, root_validator


class Entry(BaseModel):
    paid: float | None
    outstanding: float | None
    incurred: float | None

    @root_validator
    def fill_missing_value_if_possible(cls, values):
        num_values = len(values.keys()) - list(values.values()).count(None)
        if num_values == 2:
            match next(k for (k, v) in values.items() if v is None):
                case "paid":
                    values["paid"] = values["incurred"] - values["outstanding"]
                case "outstanding":
                    values["outstanding"] = values["incurred"] - values["paid"]
                case "incurred":
                    values["incurred"] = values["paid"] + values["outstanding"]
        elif num_values == 3 and values["paid"] + values["outstanding"] != values["incurred"]:
            raise ValueError("paid + outstanding is not equal to incurred")
        return values
